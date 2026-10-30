K = 1


def _rows(S):
    k = S['k']
    j0 = max(k - 1, 0).bit_length()
    cur = S.get('j', j0)
    return j0, cur


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    k = S['k']
    j0, cur = _rows(S)
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), f'枚举 j = 操作二的次数（k = {k}）：m = 2^j − k 是需要插入的操作一的个数', 24, T['muted'], bold=True)
    cols = ['j', '2^j', 'm = 2^j − k', '空隙数 j+1', 'C(j+1, m)', '累计 ans']
    W = x1 - x0 - 40
    cw = [0.08, 0.12, 0.24, 0.18, 0.2, 0.18]
    xs = []
    acc = x0 + 20
    for w in cw:
        xs.append(acc)
        acc += w * W
    hy = y0 + 70
    for c, x, w in zip(cols, xs, cw):
        cv.text((x + w * W / 2, hy), c, 24, T['blue'], anchor='mm', bold=True)
    cv.line([(x0 + 20, hy + 26), (x1 - 20, hy + 26)], T['border'], 2)
    rh = 78
    total = 0
    last = cur if 'm' in S else cur - 1
    for r, j in enumerate(range(j0, j0 + 5)):
        y = hy + 56 + r * rh
        m = (1 << j) - k
        showrow = j <= cur and (j < cur or 'm' in S)
        if not showrow:
            break
        stop = m > j + 1
        active = (j == cur)
        if active:
            cv.rect((x0 + 14, y - 8, x1 - 14, y + rh - 6), fill=T["yellow"], alpha=40, r=10)
        vals = [str(j), str(1 << j), str(m), str(j + 1), '—' if stop else str(comb(j + 1, m)), '']
        for v, x, w in zip(vals, xs, cw):
            cv.text((x + w * W / 2, y + 20), v, 32, T['red'] if (stop and v == str(m)) else T['text'], anchor='mm', bold=True, mono=True)
        done = (not stop) and (j < cur or line in (8, 9))
        if done:
            tot = sum(comb(jj + 1, (1 << jj) - k) for jj in range(j0, j + 1))
            cv.text((xs[5] + cw[5] * W / 2, y + 20), str(tot), 32, T['green'], anchor='mm', bold=True, mono=True)
        if stop:
            cv.text((xs[4] + cw[4] * W / 2, y + 48), 'm > j+1：塞不下，停止', 22, T['red'], anchor='mm', bold=True)


def _cap_for(S, B, ret):
    if 'j' not in B:
        j0 = S.j
        if j0 == 0:
            return '`j` 从 `max(k-1, 0).bit_length() = 0` 开始枚举操作二的次数'
        return f'`j` 从 `max(k-1, 0).bit_length() = {j0}` 开始：更小的 j 满足不了 `2^j >= k`，==直接跳过=='
    return f'`j` 加 1 → {S.j}：再多跳一次操作二'


CONFIG = dict(
    num=3154, title='到达第 K 级台阶的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='组合数学：枚举操作二次数 j',
    tags=['数学算法', '难度分 2071'],
    setup='count = itertools.count',
    code='''
class Solution:
    def waysToReachStair(self, k: int) -> int:
        ans = 0
        for j in count(max(k - 1, 0).bit_length()):
            m = (1 << j) - k
            if m > j + 1:
                break
            ans += comb(j + 1, m)
        return ans
''',
    call=f'Solution().waysToReachStair({K})',
    expect=4,
    views=[
        dict(type='text', size=28, h=70, fn=lambda S: (
            f"从 1 出发，用 `j` 次操作二、`m` 次操作一：`1 + (2^j − 1) − m = {S['k']}`" if 'm' not in S
            else f"`1 + (2^{S['j']} − 1) − m = {S['k']}` → `m = {1 << S['j']} − {S['k']} = {S['m']}`，要放进 `{S['j'] + 1}` 个空隙")),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('k', 'k', 'blue'), ('j', 'j', 'pink'), ('m', 'm', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累加每个 j 对应的方案数',
        'for j in count': _cap_for,
        'm = (1 << j) - k': '`m = 2^{j} − {k} = {m}`：用 {j} 次操作二上到 `2^{j}`，要刚好落在 `k`，必须下走 `m` 次',
        'if m > j + 1': lambda S, B, r: (f'`m = {S.m} > j + 1 = {S.j + 1}`：操作一不能连续，{S.j} 次操作二至多隔出 {S.j + 1} 个空隙 → ==塞不下，之后只会更大，停止=='
                                         if S.m > S.j + 1 else f'`m = {S.m} ≤ j + 1 = {S.j + 1}`：放得下，继续计数'),
        'break': '后面 j 更大时 `2^j − k` 增长得比 `j + 1` 快，不可能再有方案 → 跳出循环',
        'ans += comb': '在 `{j + 1}` 个空隙里选 `{m}` 个放操作一：`C({j + 1}, {m})` = =={ans - B.ans}== → `ans = {ans}`',
        'return ans': '各 j 的方案数相加：==`{ret}`== 种（和题目示例 2 一致）',
    },
    cards=dict(
        one_liner='枚举操作二的次数 j，用组合数把下走的操作一插进空隙',
        complexity='时间 `O(1)`（循环至多 3 次），空间 `O(1)`',
        problem=['无限台阶，从第 `1` 级出发，目标第 `k` 级',
                 '操作一：下走一级，不能连续用，也不能在第 0 级用',
                 '操作二：上走 `2^jump` 级，然后 `jump + 1`；求到达 `k` 的方案数',
                 '示例：`k = 1` → `4`'],
        quote='假设使用了 m 次操作一，j 次操作二，那么有 1 + 2^0 + 2^1 + … + 2^(j-1) − m = k，即 m = 2^j − k。',
        quote_src='—— 灵茶山艾府题解（方法二：组合数学）',
        idea=['`j` 次操作二一共上走 `2^j − 1` 级，所以下走次数 `m = 2^j − k` 由 `j` 唯一确定',
              '操作一不能连续：只能插进 `j` 次操作二前后及中间的 `j + 1` 个空隙，方案数 `C(j+1, m)`',
              '优化：`j` 从 `max(k-1,0).bit_length()` 起，`m > j+1` 就停'],
        summary=['`O(1)`：几乎所有 k 都直接返回 0，最多循环 3 次',
                 '易错：到达 k 后还能继续走再回来，所以==每个满足条件的 j 都要累加==',
                 '方法一是 `dfs(i, j, pre_down)` 记忆化搜索，状态数 `O(log^2 k)`；另一种写法给 `comb` 加缓存',
                 '原题解用 `itertools.count`，这里在 setup 里取别名 `count`'],
    ),
)
