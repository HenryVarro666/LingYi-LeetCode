CONFIG = dict(
    num=2285, title='道路的最大总重要性', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='度数 + 排序不等式',
    tags=['灵神题单', '难度分 1496'],
    code='''
class Solution:
    def maximumImportance(self, n: int, roads: List[List[int]]) -> int:
        deg = [0] * n
        for x, y in roads:
            deg[x] += 1
            deg[y] += 1
        deg.sort()
        return sum(d * i for i, d in enumerate(deg, 1))
''',
    call='Solution().maximumImportance(5, [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]])',
    expect=43,
    views=[
        dict(type='array', var='roads', label='roads（每条路连接两座城市）', h=230, cell=150, index=False),
        dict(type='array', var='deg', label='deg[i]：城市 i 的度数（排序后按从小到大）', h=200),
        dict(type='text', size=34, fn=lambda S: (
            '最大化 `Σ deg[i] × p[i]`，度数大的城市配大数字' if 'deg' not in S or S['deg'] != sorted(S['deg']) or S['_line'] < 8 else
            '`' + ' + '.join(f'{d}×{i}' for i, d in enumerate(S['deg'], 1)) + '` = ==' + str(sum(d * i for i, d in enumerate(S['deg'], 1))) + '==')),
    ],
    watch=['x', 'y', 'deg'],
    captions={
        'deg = [0]': '`deg[i]` 记录城市 `i` 的度数（连了几条路）',
        'deg[x] += 1': '路 `({x}, {y})`：城市 `{x}` 度数 +1 → {deg}',
        'deg[y] += 1': '城市 `{y}` 度数 +1 → {deg}',
        'deg.sort()': '==从小到大排序==：度数最小的分到 1，次小的分到 2……',
        'return sum': '每条路的重要性之和 = `Σ deg × 数值`，排序后配对最大 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='度数越大的城市，分配的数字越大',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 座城市，每座分配 `1..n` 中互不相同的数', '每条路的重要性 = 两端数字之和，求总和最大值',
                 '示例：`n = 5`，6 条路 → `43`'],
        quote='设点 i 的度数为 deg[i]，点 i 被安排的整数值为 p[i]，问题即最大化 Σ deg[i]·p[i]。根据排序不等式可知，deg 最小的安排 1，次小的安排 2，依此类推。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每条路把两端点的值各算一次 → 城市的值被计入 ==deg 次==',
              '总和 = `Σ deg[i] × p[i]`，排序不等式：==同序相乘和最大==',
              '度数排序后，第 `i` 小配数字 `i`，累加即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`enumerate(deg, 1)`：数字从 1 开始，不是 0',
                 '同类思路：把求和式换成「系数 × 值」，再用排序不等式配对'],
    ),
)
