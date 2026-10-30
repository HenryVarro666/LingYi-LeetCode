CONFIG = dict(
    num=1791, title='找出星型图的中心节点', difficulty='Easy', category='图论算法',
    author='灵茶山艾府', technique='前两条边的公共点',
    code='''
class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        return edges[0][0] if edges[0][0] in edges[1] else edges[0][1]
''',
    call='Solution().findCenter([[1,2],[5,1],[1,3],[1,4]])',
    expect=1,
    views=[
        dict(type='grid', var='edges', h=240, label='edges（前两行是关键）', cell=60,
             color=lambda S, i, j, v: 'yellow' if i < 2 else None),
        dict(type='text', size=34, h=120, fn=lambda S: f"前两条边：`{S['edges'][0]}` 和 `{S['edges'][1]}`"),
        dict(type='text', size=34, h=120, fn=lambda S: f"`{S['edges'][0][0]}` 在 `{S['edges'][1]}` 里吗？ ==" + ('在，它就是中心' if S['edges'][0][0] in S['edges'][1] else '不在，中心是另一端') + '=='),
    ],
    watch=[],
    captions={
        'return edges': '`edges[0][0] = {edges[0][0]}` ' + '在 `edges[1] = {edges[1]}` 中吗？ 中心与每条边都相连，==必在前两条边里同时出现==，所以公共端点就是中心：`{ret}`',
    },
    cards=dict(
        one_liner='中心必然同时在前两条边里，找公共端点即可',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['星型图：一个中心节点，与其余 `n-1` 个节点各连一条边',
                 '给边列表 `edges`，返回中心节点',
                 '示例：`[[1,2],[5,1],[1,3],[1,4]]` → `1`'],
        quote='找都在前两条边的节点即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每条边都包含中心，所以前两条边都含有中心',
              '两条不同的边最多共享一个端点，这个端点就是中心',
              '`edges[0][0]` 在 `edges[1]` 里就是它，否则是 `edges[0][1]`'],
        before=[dict(heading='星型图长什么样', lines=['中心连着所有其他节点，每条边都有一个端点是中心', '所以任取两条边，它们的公共端点只能是中心', '不用统计度数，也不用建图', '这是一道脑筋急转弯式的 `O(1)` 题'])],
        after=[dict(heading='为什么够用', lines=['`n >= 3`，所以至少有两条边', '两条边的另一端点各不相同（否则出现重边）', '公共点只有一个：`edges[0][0]` 或 `edges[0][1]`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '不需要遍历全部边，也不需要统计度数',
                 '易错：要在 `edges[1]` 里判断，不是和 `edges[0]` 自己比'],
    ),
)
