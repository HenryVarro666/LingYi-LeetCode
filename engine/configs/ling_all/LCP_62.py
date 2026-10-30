CONFIG = dict(
    num='LCP 62', title='交通枢纽', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='统计入度与出度',
    code='''
class Solution:
    def transportationHub(self, path: List[List[int]]) -> int:
        nodes = set()
        out_deg = Counter()
        in_deg = Counter()
        for x, y in path:
            nodes.add(x)
            nodes.add(y)
            out_deg[x] += 1
            in_deg[y] += 1
        for x in nodes:
            if out_deg[x] == 0 and in_deg[x] == len(nodes) - 1:
                return x
        return -1
''',
    call='Solution().transportationHub([[0,1],[0,3],[1,3],[2,0],[2,3]])',
    expect=3,
    views=[
        dict(type='text', size=28, h=70, fn=lambda S: ('当前边：`' + str(S['x']) + ' → ' + str(S['y']) + '`' if 'y' in S and S.get('_line') in (7, 8, 9, 10, 11) else '边：`0→1  0→3  1→3  2→0  2→3`')),
        dict(type='set', var='nodes', label='nodes（出现过的地点）', fmt=lambda x: str(x), h=130),
        dict(type='map', var='out_deg', label='out_deg（出度）', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='map', var='in_deg', label='in_deg（入度）', fmt=lambda k, v: f'{k}: {v}', h=150),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('点数', 'len(nodes)', 'orange')],
    captions={
        'nodes = set()': '`nodes` 收集所有出现过的地点，用来知道一共有 n 个点',
        'out_deg = Counter()': '`out_deg[x]`：从 x 出发的专线数（出度）',
        'in_deg = Counter()': '`in_deg[y]`：通往 y 的专线数（入度）',
        'for x, y in path': lambda S, B, r: ('专线都处理完了，度数统计完毕' if 'x' in B and B.x == S.x and B.y == S.y else f'取一条专线 `{S.x} → {S.y}`'),
        'nodes.add(x)': '起点 `{x}` 记入 nodes',
        'nodes.add(y)': '终点 `{y}` 记入 nodes',
        'out_deg[x] += 1': '`{x}` 多一条出边，`out_deg[{x}] = {out_deg[x]}`',
        'in_deg[y] += 1': '`{y}` 多一条入边，`in_deg[{y}] = {in_deg[y]}`',
        'for x in nodes': '逐个检查地点 `{x}` 是不是枢纽',
        'if out_deg': lambda S, B, r: (f'`out_deg[{S.x}] = {S.out_deg[S.x]}`，`in_deg[{S.x}] = {S.in_deg[S.x]}`，需要出度 0 且入度 `{len(S.nodes)} − 1 = {len(S.nodes) - 1}` → ' + ('==满足，是枢纽==' if S.out_deg[S.x] == 0 and S.in_deg[S.x] == len(S.nodes) - 1 else '不满足，换下一个')),
        'return x': '`{x}` 无出边，其余每个点都有边直达它 → 返回 =={x}==',
        'return -1': '没有地点同时满足两个条件 → 返回 `-1`',
    },
    cards=dict(
        one_liner='枢纽 = 出度 0 且入度 n−1，数一遍度数就够',
        complexity='时间 `O(m + n)`，空间 `O(n)`（m 为专线数）',
        problem=['`path[i] = [a, b]` 是 a 到 b 的单向专线',
                 '枢纽：其余所有点都直接通向它，且它不通向别人',
                 '示例：`[[0,1],[0,3],[1,3],[2,0],[2,3]]` → `3`'],
        quote='`out_deg[x] == 0 and in_deg[x] == len(nodes) - 1`',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['先扫一遍边：把点收进 `nodes`，同时累计出度、入度',
              '点数 n 要等扫完才知道，所以再遍历一次 `nodes` 检查',
              '`Counter` 里没出现的点度数自动是 0'],
        summary=['时间 `O(m + n)`，空间 `O(n)`',
                 '点编号不连续，所以用 `nodes` 集合数点，不能用 `max+1`',
                 '入度要等于 `len(nodes) - 1`，不是 `len(nodes)`',
                 '这样的点至多一个，找到就可以直接返回'],
    ),
)
