G0 = [[1, 4, 2, 5, 3, 6], [0, 0, 1, 1, 2, 2]]
LIM = 2


def _col(S, r, c, v):
    f, p = S.get('f'), S.get('pre')
    if not f:
        return None
    if c == len(f) - 1:
        return 'blue'
    if p is not None and c == p and S.get('_line') in (9, 10, 11, 12, 18, 19):
        return 'pink'
    return None


CONFIG = dict(
    num=3989, title='网格中保持一致的最大列数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='以某列结尾的最长一致子序列 DP',
    tags=['灵神题单·动态规划', '难度分 1800'],
    code='''
class Solution(object):
    def maxConsistentColumns(self, grid, limit):
        
        m = len(grid)
        n = len(grid[0])
        f = []

        def check(x, y):
            for index in range(m):
                if abs(grid[index][x] - grid[index][y]) > limit:
                    return False
            return True

        res = 0
        for index in range(n):
            f.append(1)
            for pre in range(index):
                if check(index, pre):
                    f[-1] = max(f[-1], f[pre] + 1)
            
        return max(f)
''',
    call=f'Solution().maxConsistentColumns({G0!r}, {LIM})',
    expect=3,
    max_steps=100,
    skip=['if abs(grid[index][x]', 'for pre in range', 'for index in range(m)', 'res = 0'],
    views=[
        dict(type='table', var='grid', label='grid（蓝列 = index，粉列 = pre）', h=250, cell=80,
             rows=lambda S: [f'行{k}' for k in range(len(S['grid']))], cols=lambda S: [f'列{k}' for k in range(len(S['grid'][0]))],
             color=_col),
        dict(type='array', var='f', label='f（f[index]：保留 index 这一列时的最大列数）', h=260, cell=80,
             pointers={'pre': 'pink'},
             color=lambda S, k, v: 'blue' if k == len(S['f']) - 1 else None),
    ],
    watch=[('index（当前列）', 'len(f) - 1', 'blue'), ('pre', 'pre', 'pink'), ('f[-1]', 'f[-1] if f else 0', 'green')],
    captions={
        'm = len(grid)': '`m = {m}` 行；`check` 要逐行检查两列的差',
        'n = len(grid[0])': '`n = {n}` 列',
        'f = []': '`f[index]`：下标 0 到 index 中，==保留 index 这一列==时最多能留几列',
        'if abs(grid[index][x]': '行 `{index}`：`|grid[{index}][{x}] − grid[{index}][{y}]| = {abs(grid[index][x]-grid[index][y])}` {">" if abs(grid[index][x]-grid[index][y]) > limit else "≤"} `limit = {limit}`',
        'return False': '行 `{index}`：`|{grid[index][x]} − {grid[index][y]}| = {abs(grid[index][x]-grid[index][y])}` > `limit = {limit}`，这一行差超过 `limit` → 两列不能相邻保留，==check 返回 False==',
        'return True': '每一行都满足 → 两列兼容，==check 返回 True==',
        'for index in range(n)': lambda S, B, r: (f'处理第 `{S.index}` 列：只看它和「上一个保留列」是否兼容' if S.get('index') != B.get('index') else '所有列处理完毕'),
        'f.append(1)': '先假设只保留这一列：`f[{index}] = 1`',
        'if check(index, pre)': lambda S, B, r: f'`check({S.index}, {S.pre})`：列 `{S.pre}` 能当列 `{S.index}` 前面的最后一列吗？ → ' + ('==兼容==' if all(abs(rw[S.index] - rw[S.pre]) <= S.limit for rw in S.grid) else '==不兼容=='),
        'f[-1] = max': '`f[{index}] = max(旧值, f[{pre}] + 1)` = =={f[-1]}==',
        'return max(f)': '保留哪一列结尾都可以，取最大：`max(f)` = =={ret}==',
    },
    cards=dict(
        one_liner='一致只看相邻两列，所以只需记住最后保留的那一列',
        complexity='时间 `O(m·n^2)`，空间 `O(n)`',
        problem=['`m×n` 的网格，删掉若干列（至少留一列），保持相对顺序',
                 '剩下的相邻两列每一行差的绝对值都 `≤ limit` 才算一致',
                 '求最多保留几列。示例：`[[-2,0,3]]`，`limit = 2` → `2`'],
        quote='由于一致的检测只发生在相邻列之间，这也就意味着某一列是否可以选用，只取决于之前操作后剩下的最后一列。',
        quote_src='—— yiduobo 题解',
        idea=['`f[index]`：保留 `index` 这一列、前面 0..index 里最多留几列',
              '初值 1（只留自己）；枚举前一个保留列 `pre`，兼容就取 `f[pre] + 1`',
              '`check(x, y)` 逐行比较两列，任何一行差过大就不兼容'],
        summary=['时间 `O(m·n^2)`：`n^2` 对列 × 每对 `m` 行检查',
                 '易错：答案是 `max(f)`，不是 `f[-1]`，因为最后一列不一定保留',
                 '原文是 Python 2 风格，但代码无需改动即可在 Python 3 运行（`res = 0` 为原文遗留变量）',
                 '没有灵神的 `f[j] > mx` 剪枝：每对列都完整 check'],
    ),
)
