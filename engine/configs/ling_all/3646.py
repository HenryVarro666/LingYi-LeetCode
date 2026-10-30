def _bits(mask):
    return [x for x in range(1, 10) if mask >> (x - 1) & 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    num = S['num']
    ts = S.get('target_size')
    ans = S.get('ans')
    mask = S.get('mask')
    sz = S.get('sz')
    perm = S.get('perm')
    p = S.get('p')
    pal = S.get('pal')
    odd = S.get('odd')
    v = S.get('v')
    cv.text((x0 + 18, y0 + 4), f'找 > {num} 的最小特殊回文数：长度只可能是 {len(str(num))} 或 {len(str(num)) + 1}', 24, T['muted'], bold=True)
    # 数字集合
    ys = y0 + 60
    cv.text((x0 + 18, ys), '数字集合 mask（亮 = 选中，数字 k 要出现 k 次；奇数至多选一个）', 21, T['muted'], bold=True)
    cell = min(74, (x1 - x0 - 40) / 9)
    sx = x0 + 20
    cy = ys + 38
    on = _bits(mask) if mask is not None else []
    for x in range(1, 10):
        X = sx + (x - 1) * cell
        sel = x in on
        fill = (T['orange'] if x % 2 else T['blue']) if sel else T['panel2']
        cv.rect((X + 4, cy, X + cell - 4, cy + cell - 10), fill=fill, r=10, outline=T['border'])
        cv.text((X + cell / 2, cy + (cell - 10) / 2), x, 34, T['bg'] if sel else T['dim'], anchor='mm', bold=True, mono=True)
    if mask is not None:
        cv.text((x0 + 18, cy + cell + 2), f'mask = {mask:09b}（从右数第 k 位 = 数字 k）　数位总数 sz = {sz}', 22, T['text'], bold=True)
    # 左半 perm
    yp = cy + cell + 56
    cv.text((x0 + 18, yp), '左半部分的数位 perm（每个数字取一半）与当前排列 p', 21, T['muted'], bold=True)
    if perm is not None:
        cw = 58
        for i, d in enumerate(perm):
            X = x0 + 20 + i * (cw + 8)
            cv.rect((X, yp + 36, X + cw, yp + 36 + cw), fill=T['panel2'], r=8, outline=T['border'])
            cv.text((X + cw / 2, yp + 36 + cw / 2), d, 30, T['muted'], anchor='mm', bold=True, mono=True)
        if p is not None:
            xs = x0 + 20 + len(perm) * (cw + 8) + 30
            cv.text((xs - 18, yp + 36 + cw / 2), '→', 30, T['dim'], anchor='mm')
            for i, d in enumerate(p):
                X = xs + i * (cw + 8)
                cv.rect((X, yp + 36, X + cw, yp + 36 + cw), fill=T['pink'], r=8)
                cv.text((X + cw / 2, yp + 36 + cw / 2), d, 30, T['bg'], anchor='mm', bold=True, mono=True)
    # 回文
    yq = yp + 36 + 58 + 40
    cv.text((x0 + 18, yq), '正在拼的回文 pal（左半 + 中心 + 左半的倒序）', 21, T['muted'], bold=True)
    if pal is not None and pal > 0:
        cv.text((x0 + 22, yq + 34), str(pal), 56, T['green'] if (ans is not None and pal == ans) else T['text'], bold=True, mono=True)
    if ans is not None:
        a = '∞' if ans == float('inf') else int(ans)
        cv.text((x0 + 22, yq + 112), f'当前最优 ans = {a}', 30, T['yellow'], bold=True)


def _vals(S):
    return f'`size[mask]` 已预处理好：每个集合的数位总数'


def _mask_cap(S, B, r):
    d = _bits(S.mask)
    return (f'集合 `{d}`，数位总数 `sz = {S.sz}`，等于 {S.target_size} 或 {S.target_size + 1} → ==值得枚举==')


def _prune(S, B, r):
    if S.pal >= S.ans:
        return f'`pal = {S.pal}` ≥ `ans = {S.ans}`：这个集合后面的排列只会更大 → ==最优性剪枝=='
    return f'`pal = {S.pal}` < `ans`：还没剪枝，继续判断'


def _gt(S, B, r):
    if S.pal > S.num:
        return f'`pal = {S.pal} > num = {S.num}` → ==满足要求==。排列从小到大，第一个满足的就是该集合最小的'
    return f'`pal = {S.pal}` 不大于 `num = {S.num}` → 换下一个排列'


CONFIG = dict(
    num=3646, title='下一个特殊回文数', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='枚举子集 + 枚举排列',
    tags=['数学算法', '贪心与思维', '难度分 2445'],
    code='''
ODD_MASK = 0x155
D = 9

# 预处理 size 数组，详细解释见视频讲解
size = [0] * (1 << D)
for mask in range(1, 1 << D):
    t = mask & ODD_MASK
    if t & (t - 1):  # 至少有两个奇数
        continue
    for i in range(D):
        if mask >> i & 1:
            size[mask] += i + 1

class Solution:
    def specialPalindrome(self, num: int) -> int:
        target_size = len(str(num))
        ans = inf
        for mask, sz in enumerate(size):
            if sz != target_size and sz != target_size + 1:
                continue

            # 构造排列 perm
            perm = []
            odd = 0
            for x in range(1, D + 1):
                if mask >> (x - 1) & 1:
                    perm.extend([x] * (x // 2))
                    if x % 2:
                        odd = x

            # 枚举 perm 的所有排列 p，生成对应的回文数
            for p in permutations(perm):
                pal = 0
                for v in p:
                    pal = pal * 10 + v
                v = pal
                if odd:
                    pal = pal * 10 + odd
                # 反转 pal 的左半，拼在 pal 后面
                while v:
                    v, d = divmod(v, 10)
                    pal = pal * 10 + d
                if pal >= ans:  # 最优性剪枝：答案不可能变小
                    break
                if pal > num:  # 满足要求
                    ans = pal
                    break
        return ans
''',
    call='Solution().specialPalindrome(4443)',
    expect=4444,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('num', 'num', 'blue'), ('mask', 'mask', 'cyan'), ('p', 'p', 'pink'), ('pal', 'pal', 'green'), ('ans', 'ans', 'yellow')],
    skip=['for mask, sz in enumerate(size)', 'if sz != target_size', 'continue', 'for x in range(1, D + 1)', 'if mask >> (x - 1) & 1',
          'if x % 2', 'odd = 0', 'break', 'for v in p', 'if odd:', 'while v:', 'v, d = divmod'],
    max_steps=90,
    captions={
        'target_size = len': '`num = {num}` 有 `{target_size}` 位：答案要么 {target_size} 位，要么 {target_size + 1} 位（{target_size + 1} 位一定有解）',
        'ans = inf': '`ans` 记录目前找到的最小特殊数',
        'perm = []': _mask_cap,
        'perm.extend': '数字 `{x}` 要出现 {x} 次：左半放 `{x // 2}` 个（奇数的余下一个放正中间）',
        'odd = x': '`{x}` 是奇数：它出现奇数次，必须有一个放==回文中心==，`odd = {x}`',
        'for p in permutations': '枚举左半的一个排列 `p = {p}`（perm 从小到大，生成的回文也从小到大）',
        'pal = 0': '从空开始拼：先拼左半',
        'pal = pal * 10 + v': '拼上左半的 `{v}` → `pal = {pal}`',
        'v = pal': '先记下左半 `v = {v}`，等会儿倒着接到后面',
        'pal = pal * 10 + odd': '中心放奇数 `{odd}` → `pal = {pal}`',
        'pal = pal * 10 + d': '把左半倒着接上：取出个位 `{d}` → `pal = {pal}`',
        'if pal >= ans': _prune,
        'if pal > num': _gt,
        'ans = pal': '`ans = {ans}`：这个集合里排在最前的合法回文，后面的排列更大，不用再看了（`break`）',
        'return ans': '没有更小的了，答案 `{ans}`',
    },
    cards=dict(
        one_liner='特殊数只有 95 种数字集合，逐个枚举排列即可',
        complexity='时间 `O(K·(m/2)!·m)`，`K=10`，`m = log n`；空间 `O(m)`',
        problem=['回文数，且每个数字 `k` 恰好出现 `k` 次，叫==特殊数==',
                 '给定 `n ≤ 10^15`，返回==严格大于== `n` 的最小特殊数',
                 '示例：`n = 33` → `212`；本视频用 `n = 4443`'],
        quote='回文数由 {2,4,6,8} 加上至多一个奇数组成，有 2^4·6−1 = 95 种非空组合。这就很少了，考虑暴力枚举。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数出现奇数次，只能放正中心 → ==至多一个奇数==',
              '枚举数字集合，再枚举左半的排列（[47. 全排列 II](https://leetcode.cn/problems/permutations-ii/) 的思路）',
              '`n` 有 `m` 位时，只需看长 `m` 或 `m+1` 的特殊数；排列从小到大，第一个 `> n` 的即最小'],
        after=[dict(heading='另一种写法', lines=['写法二：预处理所有长度 ≤ 16 的特殊数（仅 2296 个），排序后二分查找',
                                              '方法二：倒序贪心 + 0-1 背包，思路同 2048 题'])],
        summary=['`size[mask]` 预处理每个集合的数位总数，先过滤长度，再枚举排列',
                 '`pal >= ans` 的剪枝：同一集合后面的排列只会更大',
                 '`perm` 要从小到大排好，才能「第一个满足就 break」',
                 '`permutations` 对重复数字会产生重复排列，不影响正确性，只是多算一点'],
    ),
)
