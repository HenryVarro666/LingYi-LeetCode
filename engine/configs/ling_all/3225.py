G0 = [[1, 0, 4, 0], [0, 5, 2, 3], [3, 0, 0, 4], [2, 6, 1, 0]]


def _gcolor(S, r, c, v):
    j = S.get('j')
    if j is None:
        return None
    if c == j:
        return 'blue'
    if c == j + 1:
        return 'pink'
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    n = len(f)
    j = S.get('j')
    ln = S.get('_line', 0)
    pre = S.get('pre')
    cw = min(110, (x1 - x0 - 230) / (n + 1))
    sx = x0 + 200
    rh = min(40, (y1 - y0 - 62 - 24) / 8)
    cv.text((x0 + 10, y0 + 2), 'f[层][pre][dec]：粉色层 = 正在填的第 j+1 层，蓝色层 = 用到的第 j 层', 22, T['muted'], bold=True)
    for p in range(n + 1):
        cv.text((sx + p * cw + cw / 2, y0 + 44), f'pre={p}', 19, T['dim'], anchor='mm', mono=True)
    for L in range(n):
        for d in range(2):
            y = y0 + 62 + (L * 2 + d) * rh + L * 8
            active = j is not None and L == j + 1
            src = j is not None and L == j
            lab = f'f[{L}][·][{d}]'
            cv.text((x0 + 14, y + rh / 2 - 2), lab, 20, T['pink'] if active else (T['blue'] if src else T['muted']), anchor='lm', bold=True, mono=True)
            for p in range(n + 1):
                v = f[L][p][d]
                X = sx + p * cw
                hot = active and (
                    (pre == p and ln in (11, 12, 17, 18)) or (p == 0 and ln in (21, 22) and (ln == 21 or d == 1)))
                fill = T['yellow'] if hot else ((54, 62, 78) if active else (48, 54, 64) if src else (36, 40, 48))
                fg = T['bg'] if hot else (T['text'] if (active or src) else T['muted'])
                cv.rect((X + 2, y + 2, X + cw - 2, y + rh - 2), fill=fill, r=6)
                cv.text((X + cw / 2, y + rh / 2), v, 22, fg, anchor='mm', bold=True, mono=True)


def _info(S):
    j = S.get('j')
    if j is None:
        return '`col_sum[j][i]` = 第 j 列前 i 个格子之和；`f[j+1][pre][dec]` = 前 j+1 列的最大分数'
    parts = [f'`j` = {j}：第 {j} 列（蓝）与第 {j + 1} 列（粉）']
    if 'pre_max' in S:
        parts.append(f'`pre_max={S["pre_max"]}`')
    if 'suf_max' in S:
        parts.append(f'`suf_max={S["suf_max"]}`')
    return '，'.join(parts)


CONFIG = dict(
    num=3225, title='网格图操作后的最大分数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='列 DP + 前后缀最大值优化到 O(n²)',
    tags=['其他线性 DP', '多维 DP', '难度分 3028'],
    code='''
class Solution:
    def maximumScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        col_sum = [list(accumulate(col, initial=0)) for col in zip(*grid)]

        f = [[[0, 0] for _ in range(n + 1)] for _ in range(n)]
        for j in range(n - 1):
            # 用前缀最大值优化
            pre_max = f[j][0][1] - col_sum[j][0]
            for pre in range(1, n + 1):
                f[j + 1][pre][0] = f[j + 1][pre][1] = max(f[j][pre][0], pre_max + col_sum[j][pre])
                pre_max = max(pre_max, f[j][pre][1] - col_sum[j][pre])

            # 用后缀最大值优化
            suf_max = f[j][n][0] + col_sum[j + 1][n]
            for pre in range(n - 1, 0, -1):
                f[j + 1][pre][0] = max(f[j + 1][pre][0], suf_max - col_sum[j + 1][pre])
                suf_max = max(suf_max, f[j][pre][0] + col_sum[j + 1][pre])

            # 单独计算 pre=0 的状态
            f[j + 1][0][0] = suf_max  # 无需考虑 f[j][0][0]，因为不能连续三列全白
            f[j + 1][0][1] = max(f[j][0][0], f[j][n][0])  # 第 j 列要么全白，要么全黑

        return max(f[-1][i][0] for i in range(n + 1))
''',
    call=f'Solution().maximumScore({G0!r})',
    expect=19,
    views=[
        dict(type='grid', var='grid', h=210, cell=70, color=_gcolor, label='grid'),
        dict(type='text', fn=_info, size=24, h=50),
        dict(type='custom', draw=_draw, h=400),
    ],
    watch=[('j', lambda S: S.get('j', ''), 'blue'), ('pre', lambda S: S.get('pre', ''), 'pink'),
           ('pre_max', lambda S: S.get('pre_max', ''), 'cyan'), ('suf_max', lambda S: S.get('suf_max', ''), 'orange')],
    captions={
        'col_sum =': '每列做前缀和：`col_sum[j][i]` = 第 j 列前 i 个格子之和，区间和 `O(1)` 取',
        'f = [[[0, 0]': '`f[j+1][pre][dec]`：前 j+1 列，第 j+1 列有 pre 个黑格；`dec=1` 表示 pre 比再右一列的黑格少',
        'pre_max = f[j][0][1]': '开始算第 `{j + 1}` 层。前缀最大值起点：`cur=0` 的 `f[j][0][1] - col_sum[j][0]` = =={pre_max}==',
        'f[j + 1][pre][0] = f[j + 1][pre][1]': lambda S, B, r: (
            f'`pre={S.pre}`：取 情况一 `f[j][pre][0]={S.f[S.j][S.pre][0]}` 与 情况二 `pre_max + col_sum = {S.pre_max} + {S.col_sum[S.j][S.pre]}` 的较大者 → =={S.f[S.j + 1][S.pre][0]}==；随后 `pre_max` 并入 `cur={S.pre}`'),
        'pre_max = max(pre_max': '把 `cur={pre}` 也并进前缀最大值：`pre_max = {pre_max}`',
        'suf_max = f[j][n][0]': '后缀最大值起点：`cur = n` → `suf_max = f[j][n][0] + col_sum[j+1][n] = {suf_max}`',
        'f[j + 1][pre][0] = max(f[j + 1][pre][0], suf_max': lambda S, B, r: (
            f'情况三：`suf_max - col_sum[j+1][pre] = {S.suf_max} - {S.col_sum[S.j + 1][S.pre]}`，和已有值取大 → =={S.f[S.j + 1][S.pre][0]}==；随后 `suf_max` 并入 `cur={S.pre}`'),
        'suf_max = max(suf_max': '把 `cur={pre}` 并进后缀最大值：`suf_max = {suf_max}`',
        'f[j + 1][0][0] = suf_max': '`pre=0, dec=0`：只剩情况三，正是 `suf_max` = =={suf_max}==（不可能连续三列全白）',
        'f[j + 1][0][1] = max': '`pre=0, dec=1`：第 j 列要么全白要么全黑 → `max({f[j][0][0]}, {f[j][n][0]})` = =={f[j + 1][0][1]}==',
        'return max': '答案：最后一层 `dec=0` 里取最大 = =={ret}==',
    },
    skip=['for pre in range', 12, 18],
    max_steps=80,
    cards=dict(
        one_liner='按列 DP：只看相邻两列谁的黑格多，再用前后缀最大值去掉枚举',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['选一个格子，把它所在列从最上面到这一行都染黑，可以操作任意次',
                 '白格且左右至少一个黑格，才计入分数，求最大总分',
                 '示例：4×4 网格 `[[1,0,4,0],[0,5,2,3],[3,0,0,4],[2,6,1,0]]` → `19`'],
        quote='我们的原则是，在从右往左递归的过程中，只把第 j 列或者第 j+1 列的格子计入总分，不考虑第 j-1 列的格子。',
        quote_src='—— 灵茶山艾府题解（二、记忆化搜索）',
        idea=['每列黑格是从顶部连续的一段，只需记录个数 `pre`，相邻列黑格数的大小关系决定谁的格子得分',
              '`dec` 记录「第 j+1 列比第 j+2 列少」，用来不重不漏地数四种情况',
              '转移里 `cur` 的枚举拆成前缀最大值 `pre_max` 与后缀最大值 `suf_max`，`O(n³)` 降到 `O(n²)`'],
        summary=['时间 `O(n²)`，空间 `O(n²)`，滚动数组可到 `O(n)`',
                 '先 `O(n⁴)` 超时 → 记忆化 `O(n³)` → 前后缀最大值 `O(n²)`；这里演示最后一版',
                 '`pre=0` 的状态要单独算：不能连续三列全白，`dec=1` 时第 j 列只看全白或全黑',
                 '`col_sum` 带 `initial=0`，下标是「前几个」'],
    ),
)
