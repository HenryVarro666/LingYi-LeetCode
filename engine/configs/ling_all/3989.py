G0 = [[1, 4, 2, 5, 3, 6], [0, 0, 1, 1, 2, 2]]
LIM = 2


def _cons(S):
    return all(abs(r[S['i']] - r[S['j']]) <= S['limit'] for r in S['grid'])


def _col(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or S.get('_line') in (None, 3, 4):
        return None
    if c == i:
        return 'blue'
    if j is not None and c == j and S.get('_line') in (6, 7, 8):
        return 'pink'
    return None


def _cap_if(S, B, ret):
    i, j, mx, f = S.i, S.j, S.mx, S.f
    if not f[j] > mx:
        return f'`f[{j}] = {f[j]} ≤ mx = {mx}`：选 j 也不会让 `f[i]` 更大 → ==最优性优化==，跳过一致性检查'
    diffs = '，'.join(f'行{k}: |{r[i]}−{r[j]}|={abs(r[i]-r[j])}' for k, r in enumerate(S.grid))
    ok = _cons(S)
    return f'`f[{j}] = {f[j]} > mx = {mx}`，才值得检查一致性：{diffs}，limit = {S.limit} → ' + ('==每行都满足，一致==' if ok else '==有行超过 limit，不一致==')


def _formula(S):
    if 'i' not in S or 'j' not in S or S.get('_line') not in (6, 7, 8):
        return '`f[i]`：列 `i` 一定保留时，`[0,i]` 列最多保留几列'
    return f'列 `{S["i"]}` 的上一个保留列候选 `j = {S["j"]}`，当前最优 `mx = {S["mx"]}`，`f[{S["i"]}] = mx + 1`'


CONFIG = dict(
    num=3989, title='网格中保持一致的最大列数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='相邻相关型 DP + 最优性优化',
    tags=['灵神题单·动态规划', '难度分 1800'],
    code='''
class Solution:
    def maxConsistentColumns(self, grid: list[list[int]], limit: int) -> int:
        n = len(grid[0])
        f = [0] * n
        for i in range(n):
            mx = 0
            for j in range(i - 1, -1, -1):  # 枚举上一个保留的列
                if f[j] > mx and all(abs(row[i] - row[j]) <= limit for row in grid):
                    mx = f[j]
            f[i] = mx + 1
        return max(f)
''',
    call=f'Solution().maxConsistentColumns({G0!r}, {LIM})',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='table', var='grid', label='grid（蓝列 = i，粉列 = j）', h=250, cell=80,
             rows=lambda S: [f'行{k}' for k in range(len(S['grid']))], cols=lambda S: [f'列{k}' for k in range(len(S['grid'][0]))],
             color=_col),
        dict(type='text', fn=_formula, size=26, h=70),
        dict(type='array', var='f', label='f（f[i]：列 i 保留时的最大列数）', h=250, cell=80, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('mx', 'mx', 'yellow'), ('ans', 'max(f)', 'green')],
    captions={
        'n = len(grid[0])': '`n = {n}` 列；把「保留的列」看成一条子序列，求最长的一致子序列',
        'f = [0] * n': '`f[i]` 表示在 `[0,i]` 列中最多保留几列，且==列 i 一定保留==',
        'for i in range': lambda S, B, r: (f'计算 `f[{S.i}]`：列 `{S.i}` 要接在哪个列后面？' if S.get('i') != B.get('i') else '所有列都算完了，`f` 填满'),
        'mx = 0': '`mx` 记录目前找到的最大 `f[j]`，先设为 0（表示 i 单独保留）',
        'if f[j] > mx and all': _cap_if,
        'mx = f[j]': '列 `{i}` 能接在列 `{j}` 后面 → `mx` 更新为 `f[{j}]` = =={mx}==',
        'f[i] = mx + 1': '`f[{i}] = mx + 1 = {mx} + 1` = =={f[i]}==（`mx = 0` 时就是只保留自己，值为 1）',
        'return max(f)': '答案是所有列里最大的 `f`：`max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='相邻相关型 DP：枚举上一个保留的列',
        complexity='时间 `O(mn^2)`，空间 `O(n)`',
        problem=['`m×n` 的网格，可以删掉若干列（至少留一列），相对顺序不变',
                 '剩下相邻两列，每一行的差的绝对值都 `≤ limit`，就称网格一致',
                 '求最多能保留几列。示例：`[[-2,0,3]]`，`limit = 2` → `2`'],
        quote='本题属于相邻相关型 DP，代表题目为 300. 最长递增子序列。本题相当于选一个「最长一致子序列」。……如果 f[j]+1 ≤ f[i]，那么 f[i] 不会变大，无需判断一致性。',
        quote_src='—— 灵茶山艾府题解',
        idea=['定义 `f[i]`：`[0,i]` 列中最多保留几列，==列 i 一定保留==',
              '「枚举选哪个」：枚举上一个保留的列 `j`，一致就用 `f[j]+1` 更新',
              '优化：`j` 从大到小枚举，`f[j] ≤ mx` 时不必检查一致性（`all` 最费时间）'],
        summary=['时间 `O(mn^2)`：`n^2` 对列，每对最多检查 `m` 行',
                 '易错：初始 `f[i] = 1`（可以只留自己）；这份写法用 `mx = 0` 再 `+1`，等价',
                 '优化前的写法是 `f=[1]*n`，对每个 `j` 都检查一致性；这里先判断 `f[j] > mx` 再检查',
                 '同类题：300. 最长递增子序列'],
    ),
)
