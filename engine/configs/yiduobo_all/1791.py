CONFIG = dict(
    num=1791, title='找出星型图的中心节点', difficulty='Easy', category='图论算法',
    author='yiduobo', technique='统计度数',
    code='''
class Solution(object):
    def findCenter(self, edges):

        d = {}
        for x, y in edges:
            d[x] = d.get(x, 0) + 1
            d[y] = d.get(y, 0) + 1
        
        for x in d:
            if d[x] == len(d) - 1:
                return x
''',
    call='Solution().findCenter([[1,2],[5,1],[1,3],[1,4]])',
    expect=1,
    views=[
        dict(type='grid', var='edges', h=220, label='edges（每行一条边）', cell=60),
        dict(type='map', var='d', h=300, label='d：节点 → 度数', fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=32, h=100, fn=lambda S: f"节点数 `len(d) = {len(S['d'])}`，中心的度数应为 `{len(S['d']) - 1}`" if 'd' in S and 'x' in S and S.get('d') else ''),
    ],
    watch=['x', 'y'],
    captions={
        'd = {}': '`d` 用来统计每个节点的度数',
        'for x, y in edges': '取一条边 `{x}-{y}`',
        'd[x] = d.get': '节点 `{x}` 多一条边：度数 → =={d[x]}==',
        'd[y] = d.get': '节点 `{y}` 多一条边：度数 → =={d[y]}==',
        'for x in d': '检查节点 `{x}`（度数 `{d[x]}`）',
        'if d[x] == len(d)': lambda S, B, r: (f'`d[{S.x}] = {S.d[S.x]}` 对 `n-1 = {len(S.d)-1}`：' + ('相等 → 与所有节点相连，是中心' if S.d[S.x] == len(S.d) - 1 else '不等，不是中心')),
        'return x': '节点 `{x}` 的度数是 `n-1`，它就是中心：`{ret}`',
    },
    cards=dict(
        one_liner='中心节点的度数是 n - 1，数一数度数就行',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['星型图有一个中心节点，与其余每个节点都有一条边',
                 '给边列表 `edges`，返回中心节点',
                 '示例：`[[1,2],[5,1],[1,3],[1,4]]` → `1`'],
        quote='题目中定义的中心节点度数为n - 1，那么只需要统计每个节点的度数，然后一趟遍历找出其中度数为n - 1的节点即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历边，两端点的度数各加一，存进字典 `d`',
              '字典的大小就是节点数 `n`',
              '再扫一遍字典，度数等于 `n-1` 的就是中心'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`len(d)` 就是节点数，不必另外传入 `n`',
                 '对比灵神：只看前两条边的公共端点，`O(1)`'],
    ),
)
