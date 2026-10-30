def _rows(S):
    """当前这一轮 (target) 下，每个数的 (x, j, ops)"""
    t = S['target']
    out = []
    for x in S['nums']:
        j = (t & ~x).bit_length()
        mask = (1 << j) - 1
        out.append((x, j, (t & mask) - (x & mask)))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums, k, m = S['nums'], S['k'], S['m']
    n = len(nums)
    W = (nums[-1] + k // m).bit_length()
    cv.text((x0 + 18, y0 + 4), '把每个数的某些位补成 target 的 1：橙 = 缺的位，红框 = 最高缺失位 j-1', 22, T['muted'], bold=True)
    cell = 70
    sx = x0 + 150
    ys = y0 + 70
    ans = S.get('ans', 0)
    if 'target' not in S:
        for t, x in enumerate(nums):
            for b in range(W):
                X = sx + b * cell
                cv.rect((X + 3, ys + 20 + t * 90, X + cell - 3, ys + 20 + t * 90 + 70), fill=T['panel2'], r=8)
                cv.text((X + cell / 2, ys + 55 + t * 90), (x >> (W - 1 - b)) & 1, 34, T['text'], anchor='mm', bold=True, mono=True)
            cv.text((sx - 14, ys + 55 + t * 90), x, 30, T['text'], anchor='rm', bold=True, mono=True)
        return
    target = S['target']
    line = S['_line']
    i = S.get('i', -1)
    done_all = 'ops' in S and line >= S.get('_sortline', 99)
    for b in range(W):
        X = sx + b * cell
        bit = W - 1 - b
        c = T['yellow'] if (target >> bit) & 1 else T['panel2']
        cv.rect((X + 3, ys - 4, X + cell - 3, ys + 56), fill=c, r=8, alpha=255 if (target >> bit) & 1 else 120)
        cv.text((X + cell / 2, ys + 26), (target >> bit) & 1, 34, T['bg'] if (target >> bit) & 1 else T['dim'], anchor='mm', bold=True, mono=True)
        cv.text((X + cell / 2, ys - 12), f'2^{bit}', 16, T['dim'], anchor='mb', mono=True)
    cv.text((sx - 14, ys + 26), f'target={target}', 26, T['yellow'], anchor='rm', bold=True, mono=True)
    cv.text((sx + W * cell + 24, ys + 26), '← ans 已填好的高位 + 这一轮想试的位', 20, T['muted'], anchor='lm')
    rows = _rows(S)
    show = n if line >= S['_after'] else (i + 1 if i >= 0 and line >= S['_ford'] else 0)
    best = sorted(r[2] for r in rows)[:m] if show == n else []
    for t, (x, j, ops) in enumerate(rows):
        y = ys + 90 + t * 96
        active = (t == i and line < S['_after'])
        for b in range(W):
            bit = W - 1 - b
            xb = (x >> bit) & 1
            tb = (target >> bit) & 1
            X = sx + b * cell
            fill = T['panel2']
            if tb and xb:
                fill = T['green']
            elif tb and not xb and t < show:
                fill = T['orange']
            elif tb and not xb:
                fill = T['panel']
            cv.rect((X + 3, y, X + cell - 3, y + 62), fill=fill, r=8, alpha=255,
                    outline=T['red'] if (t < show and j and bit == j - 1) else (T['border']), width=5 if (t < show and j and bit == j - 1) else 1)
            cv.text((X + cell / 2, y + 31), xb, 32, T['bg'] if fill in (T['green'], T['orange']) else T['text'], anchor='mm', bold=True, mono=True)
        cv.text((sx - 14, y + 31), f'x={x}', 26, T['blue'] if active else T['text'], anchor='rm', bold=True, mono=True)
        if t < show:
            chosen = show == n and ops in best and (best.count(ops) and True)
            cv.text((sx + W * cell + 24, y + 31), f'+{ops}', 30, T['green'] if chosen else T['dim'], anchor='lm', bold=True, mono=True)
            if j:
                cv.text((sx + W * cell + 130, y + 31), f'低 {j} 位补成 target 的低 {j} 位', 20, T['muted'], anchor='lm')
            else:
                cv.text((sx + W * cell + 130, y + 31), 'target 的 1 已全满足', 20, T['muted'], anchor='lm')
    if show == n:
        sm = sum(sorted(r[2] for r in rows)[:m])
        cv.text((x0 + 18, ys + 90 + n * 96 + 4), f'前 {m} 小的操作次数之和 = {sm}  {"≤" if sm <= k else ">"}  k = {k}', 28, T['green'] if sm <= k else T['orange'], bold=True)


_CODE = '''
class Solution:
    def maximumAND(self, nums: List[int], k: int, m: int) -> int:
        nums.sort()
        max_ans = nums[-1] + k // m
        if nums[-m] == nums[-1]:  # 最大的 m 个数都相等
            return max_ans

        ops = [0] * len(nums)  # 每个数的操作次数
        ans = 0
        max_width = max_ans.bit_length()
        for bit in range(max_width - 1, -1, -1):
            target = ans | (1 << bit)  # 注意 target 要带着 ans 已经填好的 1
            for i, x in enumerate(nums):
                j = (target & ~x).bit_length()
                # j-1 是从高到低第一个 target 是 1 且 x 是 0 的比特位
                # target = 10110
                #      x = 11010
                #            ^
                #           j-1
                # x 二进制中的高于 j-1 的位不变，其余位增大到和 target 一样
                # 上面的例子要把 010 变成 110
                mask = (1 << j) - 1
                ops[i] = (target & mask) - (x & mask)

            # 贪心，取前 m 小的操作次数
            ops.sort()
            if sum(ops[:m]) <= k:
                ans = target  # 答案的 bit 位可以填 1
        return ans
'''
_L = _CODE.lstrip('\n').split('\n')
_FORD = next(n for n, s in enumerate(_L, 1) if 'for i, x in enumerate' in s)
_SORT = next(n for n, s in enumerate(_L, 1) if 'ops.sort()' in s)

CONFIG = dict(
    num=3806, title='增加操作后最大按位与的结果', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='试填法 · 从高到低逐位试探',
    tags=['灵神题单·位运算', '难度分 2259'],
    code=_CODE,
    call='Solution().maximumAND([3,1,2], 8, 2)',
    expect=6,
    setup='',
    skip=['j = (target', 'mask = (1 << j)', 'ops = [0]'],
    max_steps=70,
    views=[
        dict(type='custom', draw=lambda cv, S, B, box, T: _draw(cv, dict(S, _ford=_FORD, _sortline=_SORT, _after=_SORT), B, box, T), h=560),
    ],
    watch=[('bit', 'bit', 'purple'), ('target', 'target', 'yellow'), ('ans', 'ans', 'green'), ('k', 'k'), ('m', 'm')],
    captions={
        'nums.sort()': '先排序：`nums = {nums}`，最大的几个数在末尾',
        'max_ans = ': '答案的理论上界：把最大的数加上 `k // m`：`max_ans = {nums[-1]} + {k} // {m} = {max_ans}`',
        'if nums[-m] == nums[-1]': lambda S, B, r: (f'最大的 `{S.m}` 个数不全相等（`{S.nums[-S.m]} ≠ {S.nums[-1]}`）→ 不能直接取上界，要逐位试'
                                                      if S.nums[-S.m] != S.nums[-1] else '最大的 m 个数都相等 → 直接返回上界'),
        'max_width = ': '答案最多 `{max_width}` 位二进制：从最高位 `{max_width - 1}` 往下试',
        'for bit in range': lambda S, B, r: ('所有位都试完了' if B.get('bit') == S.bit and 'bit' in B else
                                            f'试第 `{S.bit}` 位（权值 `{1 << S.bit}`）'),
        'target = ans': '`target = ans | (1 << {bit}) = {ans} | {1 << bit} = {target}`：试探“答案这一位填 1”，已填好的高位要带着',
        'for i, x in enumerate': lambda S, B, r: ('所有数的代价都算完了' if B.get('i') == S.i and 'i' in B else f'看 `x = {S.x}`'),
        'ans = 0': '`ans` 从 0 开始，逐位把能填 1 的位填上',
        'ops[i] = ': lambda S, B, r: (
            f'`x={S.x}` 要补成 `target={S.target}`：最高缺失位 `j-1 = {S.j - 1}` → 低 `{S.j}` 位补成 target 的低位：`({S.target & S.mask}) − ({S.x & S.mask})` = =={S.ops[S.i]}=='
            if S.j else f'`x={S.x}` 已经包含 target 的所有 1 → 不用操作，`ops[{S.i}] = 0`'),
        'ops.sort()': '贪心：只取操作次数最少的 `m` 个数 → 排序：`ops = {ops}`',
        'if sum(ops[:m]) <= k': lambda S, B, r: (
            f'前 `{S.m}` 小的和 = `{sum(S.ops[:S.m])}` ≤ `k = {S.k}`：钱够 → ==这一位填 1=='
            if sum(S.ops[:S.m]) <= S.k else f'前 `{S.m}` 小的和 = `{sum(S.ops[:S.m])}` > `k = {S.k}`：钱不够 → ==这一位只能填 0=='),
        'ans = target': '`ans = {ans}`（二进制 `{bin(ans)[2:]}`）：这一位确认为 1，后面的位继续带着它',
        'return ans': '每一位都试完：最大的按位与结果是 `{ans}`',
    },
    cards=dict(
        one_liner='从高位到低位试填：这一位填 1 的总代价够不够',
        complexity='时间 `O(n log n log U)`，空间 `O(n)`',
        problem=['最多 `k` 次操作，每次把某个 `nums[i]` 加 1；选出 `m` 个数，求它们按位与的最大值',
                 '示例：`[3,1,2]`，`k=8`，`m=2` → 把 3 和 2 都加到 6，答案 `6`'],
        quote='从高到低构建答案的每一位是 1 还是 0。遍历 nums，计算把 nums[i] 的某些比特位都变成 1 的最小操作次数。计算前 m 小的操作次数之和 s。如果 s≤k，那么答案这一位是 1，否则是 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`target` = 已填好的高位 + 当前想试的位；每个数变成 `target` 的超集所需的最少操作 = 补低位',
              '找 `x` 的最高缺失位 `j-1`：高位不动，低 `j` 位直接加到等于 `target` 的低位',
              '代价取前 `m` 小之和 `≤ k` 就填 1；每一轮都不修改 `nums`，所以无需考虑选的数是否一致'],
        summary=['时间 `O(n log n log U)`，瓶颈是每轮排序；快速选择可做到 `O(n log U)`',
                 '`target` 一定要带着 `ans` 已经填好的 1；位宽从 `(max + k // m)` 的二进制长度开始',
                 '先判断“最大的 m 个数相同”可直接返回上界，是优化写法；本视频演示这个优化版本',
                 '灵神思考题：把 AND 改成 OR 怎么做？'],
    ),
)
