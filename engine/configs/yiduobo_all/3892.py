NUMS, K = [2, 1, 2], 1


def _show(v):
    return [['-' if x is None else x for x in row] for row in v]


def _cell(S, r, c, v):
    i, p = S.get('index'), S.get('p')
    if i is None or p is None or S.get('_line', 0) < 19:
        return None
    if (r, c) == (i, p):
        return 'yellow'
    if (r, c) == (i - 1, p):
        return 'blue'
    if (r, c) == (i - 2, p - 1):
        return 'pink'
    return None


def _txt(S):
    i, p = S.get('index'), S.get('p')
    if i is None or p is None:
        return '`f` = 让 0 成为峰值，`g` = 不让 0 成为峰值；`[index][p]` = 前 index 个下标里至少 p 个峰值的最少操作，`-` = 不可能'
    return f'`index = {i}`：能否把 `nums[{i - 1}]` 变峰值（代价 `cost[{i - 1}] = {S["cost"][i - 1]}`），要从 `[{i - 2}][{p - 1}]` 转移' if p > 0 else '`p = 0`：不需要峰值，操作数为 0'


CONFIG = dict(
    num=3892, title='产生至少 K 个峰值的最少操作次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='分类讨论 0 号位 + 两张 DP 表 f / g',
    tags=['动态规划', '难度分 2280'],
    code='''
class Solution(object):
    def minOperations(self, nums, k):
        
        if k == 0:
            return 0

        n = len(nums)
        if k > n // 2:
            return -1
        
        f = [[None] * (k + 1) for _ in range(n + 1)]
        g = [[None] * (k + 1) for _ in range(n + 1)]

        cost = [max(max(nums[(index - 1 + n) % n], nums[(index + 1) % n]) + 1 - nums[index], 0) for index in range(n)]
        f[0][0] = 0
        g[0][0] = 0
        f[1][0] = 0
        f[1][1] = cost[0]
        g[1][0] = 0

        for index in range(2, n + 1):
            for p in range(k + 1):
                if p == 0:
                    f[index][p] = 0
                    g[index][p] = 0
                else:
                    f[index][p] = f[index - 1][p]
                    g[index][p] = g[index - 1][p]

                    if g[index - 2][p - 1] is not None and (g[index][p] is None or g[index][p] > g[index - 2][p - 1] + cost[index - 1]):
                        g[index][p] = g[index - 2][p - 1] + cost[index - 1]
                    if index != n and index != 2 and f[index - 2][p - 1] is not None and (f[index][p] is None or f[index][p] > f[index - 2][p - 1] + cost[index - 1]):
                        f[index][p] = f[index - 2][p - 1] + cost[index - 1]
        
        return min(f[-1][k], g[-1][k])
''',
    call=f'Solution().minOperations({NUMS!r}, {K})',
    expect=1,
    skip=['f = [[None]', 'g = [[None]', 'f[0][0] = 0', 'g[0][0] = 0', 'f[1][0] = 0', 'g[1][0] = 0', 'for p in range', 'for index in range(2', 'n = len(nums)'],
    max_steps=70,
    views=[
        dict(type='array', var='nums', label='nums（循环数组）', h=120, cell=70),
        dict(type='text', fn=_txt, size=22, h=80),
        dict(type='table', var=lambda S: _show(S['f']) if 'f' in S else [[0]], label='f[index][p]：0 号位要成为峰值（黄 = 在算，蓝 = 不选，粉 = 选）',
             h=290, cell=80, rows=lambda S: [str(t) for t in range(len(S['f']))] if 'f' in S else [''], cols=lambda S: [f'p={t}' for t in range(S['k'] + 1)] if 'f' in S else [''],
             color=_cell),
        dict(type='table', var=lambda S: _show(S['g']) if 'g' in S else [[0]], label='g[index][p]：0 号位不是峰值',
             h=290, cell=80, rows=lambda S: [str(t) for t in range(len(S['g']))] if 'g' in S else [''], cols=lambda S: [f'p={t}' for t in range(S['k'] + 1)] if 'g' in S else [''],
             color=_cell),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('cost', 'cost', 'yellow')],
    captions={
        'if k == 0': '`k = 0`：不需要峰值，答案必然是 `0`（`k = {k}`）',
        'if k > n // 2': '循环数组峰值至多 `n // 2 = {n // 2}` 个，`k = {k}` 没超过，继续',
        'cost = [': '`cost[index]` = 把 `nums[index]` 抬成峰值的代价（下标取模处理循环）：`cost = {cost}`',
        'f[1][1] = cost[0]': '`f[1][1] = cost[0] = {cost[0]}`：让 `nums[0]` 成为峰值只能算在 `f` 里',
        'if p == 0': lambda S, B, r: (f'`index = {S.index}, p = {S.p}`：不需要峰值，`f`、`g` 都是 `0`' if S.p == 0 else f'`index = {S.index}, p = {S.p}`：至少要 `{S.p}` 个峰值，分情况'),
        'f[index][p] = f[index - 1][p]': '先继承：不操作 `nums[{index-1}]`，`f` 和 `g` 都等于 `index-1` 行：`f = {f[index][p]}`，`g = {g[index][p]}`',
        'g[index][p] = g[index - 1][p]': '`g` 也先继承上一行：`g[{index}][{p}] = {g[index][p]}`（`None` = 暂时不可能）',
        'if g[index - 2][p - 1] is not None': lambda S, B, r: (f'把 `nums[{S.index - 1}]` 变峰值，则 `nums[{S.index - 2}]` 不能动，从 `g[{S.index - 2}][{S.p - 1}] = {S.g[S.index - 2][S.p - 1]}` 转移，代价 `cost[{S.index - 1}] = {S.cost[S.index - 1]}`；'
                                                              + ('只有它存在且更小才更新' if S.g[S.index - 2][S.p - 1] is not None else '它是 `None`（不可能）→ 不能转移')),
        'g[index][p] = g[index - 2]': lambda S, B, r: f'更小，更新：`g[{S.index}][{S.p}] = {S.g[S.index][S.p]}`',
        'index != n and index != 2': lambda S, B, r: (f'`f` 里下标 `1` 和 `n-1` 不能操作（0 号已是峰值，邻居不能是峰值）：`index = {S.index}` ' + ('==被禁止== → 跳过' if S.index in (2, S.n) else '可以转移')
                                                    ),
        'return min(': lambda S, B, r: (f'`min(f[-1][k], g[-1][k])`，`None` 表示不可能 → =={r}==' if r is not None else '取两种情况更小者'),
    },
    cards=dict(
        one_liner='0 号位成不成峰值，分成 f、g 两张表',
        complexity='时间 `O(nk)`，空间 `O(nk)`',
        problem=['循环数组 `nums`，值 ==严格大于两个相邻元素==（首尾相邻）的下标是峰值',
                 '每次操作可让某个数 `+1`，求至少 `k` 个峰值的==最少操作数==，不可能返回 `-1`',
                 '示例：`nums=[2,1,2], k=1` → `1`'],
        quote='本题中需要计算的是至少k个峰值，而不是峰值尽量多，因此不能再使用贪心的做法，必须使用动态规划进行求解。',
        quote_src='—— yiduobo 题解',
        idea=['`cost[index]` 沿用上一题：`max(两边最大值 + 1 - nums[index], 0)`，下标取模',
              '边界：`k = 0` 答案 0；`k > n // 2` 答案 -1',
              '选了 0 号位就不能选 `n-1`：用 `f`（0 是峰值）和 `g`（0 不是峰值）两张表分别 DP，最后取小'],
        summary=['时间、空间 `O(nk)`；`None` 表示不可能，比较前要先判空',
                 '易错：`f` 里 `index == 2` 和 `index == n` 不能转移（相邻峰值冲突）',
                 '选 `nums[index-1]` 当峰值，必须从 `index-2` 转移，和打家劫舍同构',
                 '本例 `k=1`：`g` 可选 `nums[2]` 代价 1，答案 1'],
    ),
)
