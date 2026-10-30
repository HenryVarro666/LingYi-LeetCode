C = [[0, 1, -1], [1, -2, 3], [2, -3, 4]]


def _ri(S):
    for i, r in enumerate(S['coins']):
        if r is S.get('row'):
            return i
    return None


def _fT(S):
    f = S.get('f')
    if f is None:
        return None
    return [[f[j][k] for j in range(len(f))] for k in range(3)]


def _cell(S, k, c, v):
    j = S.get('j')
    if j is None or S.get('_line', 0) < 8:
        return None
    if c == j + 1:
        return 'yellow'
    if c == j:
        return 'blue'
    return None


def _formula(S):
    j, x = S.get('j'), S.get('x')
    if j is None:
        return '`f[j][k]`：走到当前行第 `j-1` 格，==最多感化 k 次==的最大金币'
    f = S['f']
    L = S['_line']
    if L == 8:
        return f'`k=2`：选 `max(f[{j}][2], f[{j + 1}][2]) + {x}`，或不选（感化）`max(f[{j}][1], f[{j + 1}][1])`'
    if L == 9:
        return f'`k=1`：选 `max(f[{j}][1], f[{j + 1}][1]) + {x}`，或不选 `max(f[{j}][0], f[{j + 1}][0])`'
    if L == 10:
        return f'`k=0`：不能感化，只能选 `max(f[{j}][0], f[{j + 1}][0]) + {x}`'
    return '`f[j]` 同时存着「上一行的 j 位」和「本行的 j-1 位」，这就是空间优化'


def fmt(v):
    return '-inf' if v == float('-inf') else str(v)


def _cap(S, B, k):
    j, x, f0 = S['j'], S['x'], B['f']
    pick = max(f0[j][k], f0[j + 1][k]) + x
    skip = max(f0[j][k - 1], f0[j + 1][k - 1])
    new = S['f'][j + 1][k]
    why = ('感化更划算（躲掉 ' + str(-x) + ' 的损失）' if skip > pick else
           '直接拿更划算' + ('（这格不是强盗，没必要感化）' if x >= 0 else '')) if pick != skip else '两种一样'
    return (f"`k={k}`：选 = `max({fmt(f0[j][k])}, {fmt(f0[j + 1][k])}) + {x}` = {fmt(pick)}；"
            f"不选（感化，用掉 1 次）= `max({fmt(f0[j][k - 1])}, {fmt(f0[j + 1][k - 1])})` = {fmt(skip)} → =={fmt(new)}==，{why}")


CONFIG = dict(
    num=3418, title='机器人可以获得的最大金币数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格图 DP + 感化次数一维（空间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1798'],
    code='''
class Solution:
    def maximumAmount(self, coins: List[List[int]]) -> int:
        n = len(coins[0])
        f = [[-inf] * 3 for _ in range(n + 1)]
        f[1] = [0] * 3
        for row in coins:
            for j, x in enumerate(row):
                f[j + 1][2] = max(f[j][2] + x, f[j + 1][2] + x, f[j][1], f[j + 1][1])
                f[j + 1][1] = max(f[j][1] + x, f[j + 1][1] + x, f[j][0], f[j + 1][0])
                f[j + 1][0] = max(f[j][0], f[j + 1][0]) + x
        return f[n][2]
''',
    call=f'Solution().maximumAmount({C})',
    expect=8,
    skip=['for j, x in enumerate'],
    views=[
        dict(type='grid', var='coins', label='coins（黄 = 当前格；负数 = 强盗）', cell=76, h=250,
             color=lambda S, i, j, v: 'yellow' if (i, j) == (_ri(S), S.get('j')) else ('pink' if v < 0 else None),
             cursors=[(_ri, 'j', 'yellow')]),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var=_fT, label='f[j][k] 转置：行 = 最多感化 k 次，列 = j（黄 = 正在算的 f[j+1]，蓝 = 它依赖的 f[j]）', cell=84, h=250,
             rows=['k=0', 'k=1', 'k=2'], cols=lambda S: list(range(len(S['f']))) if 'f' in S else [],
             color=_cell),
    ],
    watch=[('row', 'row', 'cyan'), ('j', 'j', 'blue'), ('x', 'x', 'pink')],
    captions={
        'n = len': '`n = {n}`：每行 `n` 个格子',
        'f = [[-inf]': '`f[j]` 有 3 个数：==最多感化 0/1/2 次==；`-inf` 表示不合法',
        'f[1] = [0] * 3': '`f[1]` 初始化成 0：这样第一个格子也能套同一个转移，不用特判',
        'for row in coins': '开始处理新的一行，`f[j+1]` 还保留着上一行同列的值（即「从上面来」）',
        'f[j + 1][2] =': lambda S, B, r: _cap(S, B, 2),
        'f[j + 1][1] =': lambda S, B, r: _cap(S, B, 1),
        'f[j + 1][0] =': lambda S, B, r: (f"`k=0`：没有感化次数，只能拿 `{S['x']}`：`max({fmt(B['f'][S['j']][0])}, {fmt(B['f'][S['j'] + 1][0])}) + {S['x']}` = =={fmt(S['f'][S['j'] + 1][0])}=="),
        'return f[n][2]': '终点最多感化 2 次的最大金币 =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='多一个约束，就多一个参数：k 次感化机会',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['`m × n` 网格，机器人从左上走到右下，只能向右或向下',
                 '格子 `>= 0` 得金币，`< 0` 被抢；==最多感化 2 个强盗==免于被抢',
                 '示例：`[[0,1,-1],[1,-2,3],[2,-3,4]]` → `8`'],
        quote='多一个约束，就多一个参数。额外增加一个参数 k，定义 dfs(i,j,k) 表示从 (0,0) 走到 (i,j)，在可用感化次数为 k 的情况下，可以获得的最大金币数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个格子「选或不选」：选 = 拿 `x`；不选 = 感化，用掉一次',
              '记忆化搜索 → 1:1 递推 → 去掉行维度，只剩 `f[j][k]`',
              '正序遍历 `j`，每格内 `k` 从大到小算（`k` 依赖更小的 `k`，要先算大的）'],
        after=[dict(heading='另外两种写法', lines=['灵神还给了记忆化搜索 `dfs(i, j, k)` 和三维递推 `f[i][j][k]`',
                                                    '本视频展示的是空间优化后的写法，状态含义完全相同'])],
        summary=['时间 `O(mn)`，空间 `O(n)`',
                 '易错：答案可能是负数，不合法状态要用 `-inf`，不能用 0 或 -1',
                 '易错：`k` 的三行必须 ==先算 k=2，再 k=1，最后 k=0==，否则覆盖掉还要用的旧值',
                 '`f[1] = [0] * 3` 让起点无需特判',
                 '同类题：64. 最小路径和（无感化版本）'],
    ),
)
