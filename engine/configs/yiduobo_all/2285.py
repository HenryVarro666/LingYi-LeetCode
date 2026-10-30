CONFIG = dict(
    num=2285, title='道路的最大总重要性', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='统计度 + 从小到大分配',
    tags=['灵神题单', '难度分 1496'],
    code='''
class Solution(object):
    def maximumImportance(self, n, roads):

        tot_d = [0] * n
        for x, y in roads:
            tot_d[x] += 1
            tot_d[y] += 1

        res = 0
        for index, d in enumerate(sorted(tot_d)):
            res += (index + 1) * d
        
        return res
''',
    call='Solution().maximumImportance(5, [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]])',
    expect=43,
    views=[
        dict(type='array', var='roads', label='roads', h=200, cell=150, index=False),
        dict(type='array', var='tot_d', label='tot_d[i]：城市 i 的度', h=170),
        dict(type='array', var='sorted(tot_d)', label='sorted(tot_d)：从小到大，下标 + 1 就是分到的数字', h=190, pointers={'index': 'blue'}),
        dict(type='text', size=34, fn=lambda S: f"已累计 `res` = =={S['res']}==" if 'res' in S else '先数每个城市的度'),
    ],
    watch=['x', 'y', 'index', 'd', ('res', 'res', 'green')],
    captions={
        'tot_d = [0]': '`tot_d[i]`：城市 `i` 的度（连了几条边）',
        'tot_d[x] += 1': '边 `({x}, {y})`：`x` 的度 +1 → {tot_d}',
        'tot_d[y] += 1': '`y` 的度 +1 → {tot_d}',
        'res = 0': '`res` 累计总重要性',
        'for index, d in': lambda S, B, r: ('遍历结束，数字 1..n 都分完了' if B.get('index') == S.get('index') and 'index' in B else f'度从小到大排好，第 `{S.index}` 个度是 `{S.d}`，分到数字 `{S.index + 1}`'),
        'res += (index + 1) * d': '度 `{d}` 的城市分到 `{index + 1}`：贡献 `{index + 1} × {d}` → `res` = =={res}=='.replace('=={res}==', '=={res}=='),
        'return res': '最大总重要性 =={res}==',
    },
    cards=dict(
        one_liner='一个点的度是多少，它的数字就被计算多少次',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 座城市分配 `1..n`，每个数只用一次', '道路重要性 = 两端数字之和，求总和最大', '示例：`n = 5` → `43`'],
        quote='一个节点的度是多少，该节点的重要性就会被计算多少次。因此可以先遍历每条边，计算每个点的度。接下来从小到大进行排序，按顺序将重要性分配给排序后的节点即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先遍历每条边，给两个端点的度各加 1', '度大的点被算的次数多 → 给它大数字', '度排序后，从小到大依次给 `1, 2, …, n`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`', '`index + 1`：数字从 1 开始', '本题不需要知道哪个城市拿到哪个数，只看度的排序'],
    ),
)
