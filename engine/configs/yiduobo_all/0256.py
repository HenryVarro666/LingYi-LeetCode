def _cc(S, r, c, v):
    i = S.get('index')
    if i is None:
        return None
    return 'yellow' if r == i else None


CONFIG = dict(
    num=256, title='粉刷房子', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='线性 DP · 滚动数组',
    tags=['线性DP'],
    code='''
class Solution(object):
    def minCost(self, costs):

        n = len(costs)
        f = costs[0][:]

        for index in range(1, n):
            g = f[:]
            f[0] = min(g[1], g[2]) + costs[index][0]
            f[1] = min(g[0], g[2]) + costs[index][1]
            f[2] = min(g[0], g[1]) + costs[index][2]

        return min(f)
''',
    call='Solution().minCost([[17,2,17],[16,16,5],[14,3,19]])',
    expect=10,
    views=[
        dict(type='table', var='costs', rows=['房0', '房1', '房2'], cols=['红', '蓝', '绿'], color=_cc, h=230),
        dict(type='array', var='g', label='g：上一栋房子刷完各颜色的最小代价', h=150),
        dict(type='array', var='f', label='f：当前这栋房子刷完各颜色的最小代价', h=150),
    ],
    watch=['index', ('f', 'f', 'green'), ('g', 'g', 'cyan')],
    captions={
        'n = len': '`n = {n}` 栋房子，颜色 0、1、2 = 红、蓝、绿',
        'f = costs[0][:]': '第 0 栋没有前一栋限制：`f` = 它自己的三种代价 `{f}`',
        'for index': lambda S, B, r: (f'处理第 `{S.index}` 栋房子' if S.index != B.get('index') else '所有房子都处理完了'),
        'g = f[:]': '备份上一栋的结果到 `g`，因为下面要边改 `f` 边读旧值：`g = {g}`',
        'f[0] =': '刷红色：上一栋只能是蓝或绿 → `min({g[1]}, {g[2]}) + {costs[index][0]}` = =={f[0]}==',
        'f[1] =': '刷蓝色：上一栋只能是红或绿 → `min({g[0]}, {g[2]}) + {costs[index][1]}` = =={f[1]}==',
        'f[2] =': '刷绿色：上一栋只能是红或蓝 → `min({g[0]}, {g[1]}) + {costs[index][2]}` = =={f[2]}==',
        'return min': '最后一栋刷哪种颜色都行，取最小：`min({f})` = =={ret}==',
    },
    cards=dict(
        one_liner='相邻两栋颜色不同：当前颜色只能从上一栋的另外两种转移',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`n` 栋房子排成一排，每栋可刷红、蓝、绿，`costs[i][j]` 是第 `i` 栋刷颜色 `j` 的花费',
                 '==相邻两栋颜色不能相同==，求刷完所有房子的最小总花费',
                 '示例：`[[17,2,17],[16,16,5],[14,3,19]]` → `10`（蓝、绿、蓝）'],
        quote='对于f[i][j]而言，其上一栋房子的颜色不能为j。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：前 `i` 栋刷完且第 `i` 栋是颜色 `j` 的最小代价',
              '`f[i][0] = f[i-1][1] 与 f[i-1][2] 的较小者 + cost[i][0]`，另外两色同理',
              '每轮只依赖上一轮 → 用 `g` 备份上一轮，滚掉 `i` 这一维'],
        summary=['时间 `O(n)`，空间 `O(1)`（只存 3 个数）',
                 '易错点：必须先 `g = f[:]` 拷贝，直接引用会让 `f[1]` 读到刚改过的 `f[0]`',
                 '最后一栋颜色不限，答案是 `min(f)`',
                 '推广：颜色数变成 k，见第 265 题'],
    ),
)
