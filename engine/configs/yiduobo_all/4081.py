N, SUM = 5, 7


def _cell(S, i, j, v):
    if 'index' not in S or 'x' not in S:
        return None
    if (i, j) == (S['index'], S['x']):
        return 'yellow'
    if 'v' in S and i == S['index'] - 1 and j == S['x'] - S['v'] and j >= 0:
        return 'blue'
    if i == S['index'] - 1 and j == S['x']:
        return 'cyan'
    return None


def _ucell(S, i, j, v):
    if 'index' not in S or 'x' not in S:
        return None
    if (i, j) == (S['index'], S['x']):
        return 'yellow'
    if v and v > 0:
        return 'green'
    return None


def _cond(S, B, r):
    v, x, idx = S.v, S.x, S.index
    if x < v:
        return f'`x = {x} < v = {v}`：装不下这个质数 → 只能沿用上一轮'
    p = S.f[idx - 1][x - v]
    if p == -1:
        return f'`f[{idx-1}][{x-v}] = -1`：和 {x-v} 凑不出来 → 不能用 `{v}`'
    cur = S.f[idx][x]
    if cur == -1:
        return f'不用 `{v}` 凑不出 {x}，用了需 `{p+1}` 个 → ==采用 {v}=='
    if cur >= p + 1:
        return f'`{cur} ≥ {p}+1`：用 `{v}` 个数不更多 → ==采用 {v}==（后遍历的更小，覆盖大的，保字典序最小）'
    return f'`{cur} < {p}+1`：不用 `{v}` 个数更少 → 不采用'


CONFIG = dict(
    num=4081, title='选择质数子集II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='背包 · 记录方案 · 质数倒序保字典序',
    code='''
class Solution(object):
    def maxPrimeSubset(self, n, s):
        
        g = [True] * (n + 1)
        x = 2
        p = []
        while x <= n:
            if g[x]:
                p.append(x)
                for v in range(x + x, n + 1, x):
                    g[v] = False
            x += 1
        
        m = len(p)
        f = [[-1] * (s + 1) for _ in range(m + 1)]
        f[0][0] = 0
        use = [[None] * (s + 1) for _ in range(m + 1)]
        for index, v in enumerate(p[::-1], 1):
            for x in range(s + 1):
                f[index][x] = f[index - 1][x]
                use[index][x] = 0
                if x >= v and f[index - 1][x - v] != -1 and (f[index][x] == -1 or f[index][x] >= f[index - 1][x - v] + 1):
                    f[index][x] = f[index - 1][x - v] + 1
                    use[index][x] = v

        x = s
        res = []
        while x > 0 and f[-1][x] == -1:
            x -= 1

        index = m
        while x > 0:
            if use[index][x] > 0:
                res.append(use[index][x])
            x -= use[index][x]
            index -= 1
        
        return res
''',
    call=f'Solution().maxPrimeSubset({N}, {SUM})',
    expect=[2, 5],
    skip=['g = [True]', 'x = 2', 'while x <= n', 'if g[x]', 'for v in range(x + x', 'g[v] = False', 'x += 1',
          'for x in range(s + 1)', 'f[index][x] = f[index - 1][x]', 'use[index][x] = 0', 'use = [[None]',
          'f = [[-1]', 'f[0][0] = 0', 'm = len(p)', 'for index, v in'],
    views=[
        dict(type='array', var='p', label='p（筛出的质数）', cell=70, h=150,
             color=lambda S, i, v: 'yellow' if S.get('v') == v and 'use' in S else None),
        dict(type='table', var='f', label='f[index][x]：凑出和 x 最少用几个质数（-1 = 凑不出）', h=330, cell=64,
             rows=lambda S: ['0'] + [f'+{q}' for q in S.get('p', [])[::-1]], cols=list(range(SUM + 1)), color=_cell),
        dict(type='table', var='use', label='use[index][x]：这一格是否用了该质数（0 = 没用，绿 = 用了 v）', h=330, cell=64,
             rows=lambda S: ['0'] + [f'+{q}' for q in S.get('p', [])[::-1]], cols=list(range(SUM + 1)), color=_ucell),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('x', 'x', 'yellow'), ('res', 'res', 'green')],
    captions={
        'p.append(x)': '`{x}` 是质数 → 加入 `p`',
        'for index, v in': '第 `{index}` 轮：考虑质数 `v = {v}`（从大到小）',
        'if x >= v and': _cond,
        'f[index][x] = f[index - 1][x] + 1': '`f[{index}][{x}] = {f[index][x]}`',
        'f[index][x] = f[index - 1][x - v] + 1': '`f[{index}][{x}]` = 上一轮 `f[{index-1}][{x-v}]` + 1 = =={f[index][x]}==',
        'use[index][x] = v': '`use[{index}][{x}] = {v}`：记下这一格是用 `{v}` 转移来的',
        'x = s': '开始倒推方案：从和 `s = {s}` 出发',
        'while x > 0 and f[-1][x] == -1': lambda S, B, r: (f'`f[-1][{S.x}] = -1`：凑不出 {S.x} → 和减 1 再试'
                                                         if S.f[-1][S.x] == -1
                                                         else f'`f[-1][{S.x}] = {S.f[-1][S.x]}`：能凑出，最大和就是 =={S.x}=='),
        'x -= 1': '`x` → {x}',
        'index = m': '从最后一轮 `index = {index}` 往回追',
        'while x > 0:': lambda S, B, r: (f'`x = {S.x} > 0`：还没追完' if S.x > 0 else '`x = 0`：追溯完成'),
        'if use[index][x] > 0': lambda S, B, r: (f'`use[{S.index}][{S.x}] = {S.use[S.index][S.x]}` > 0：用了这个质数' if S.use[S.index][S.x] > 0
                                                 else f'`use[{S.index}][{S.x}] = 0`：这一轮没用质数'),
        'res.append': '方案里收集 `{use[index][x]}` → `res = {res}`',
        'x -= use[index][x]': '和扣掉用过的质数 → `x = {x}`',
        'index -= 1': '回到上一轮 `index = {index}`',
        'return res': '方案 `{res}`（已是递增：大质数后更新、先追到的是小的）',
    },
    cards=dict(
        one_liner='先求能凑的最大和，再用 use 数组倒推出具体方案',
        complexity='时间 `O(m·s)`，空间 `O(m·s)`（m 为质数个数）',
        problem=['给 `n`、`s`（都 ≤ 1000）。从 `≤ n` 的质数里选子集，每个只能用一次',
                 '和不超过 `s` 且尽量大；和相同时质数个数尽量少；再相同时字典序最小',
                 '返回递增的质数数组',
                 '本视频：`n = 5, s = 7` → `[2, 5]`'],
        quote='在这里选择从大到小的遍历顺序就可以保证最终方案的字典序最小，其原理和基数排序相同，越后更新状态的元素，其可能覆盖前面元素的决策',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[index][x]`：用前 `index` 个质数凑出和 `x` 的最少个数',
              '质数从大到小处理，个数相同时 `>=` 让后来的小质数覆盖大的',
              '`use` 记录每格是否用了当前质数，最后从 `(m, x)` 倒推方案'],
        summary=['时间 `O(m·s)`，空间 `O(m·s)`',
                 '不能滚动成一维：倒推方案要原汁原味的 `f[index-1]`',
                 '`>=` 而不是 `>`：个数相同也要覆盖，才能偏向小质数',
                 '最大和 `x` 要从 `s` 往下找第一个 `f[-1][x] != -1`',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
