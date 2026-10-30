CONFIG = dict(
    num='LCP 62', title='交通枢纽', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='哈希表统计入度出度',
    code='''
class Solution(object):
    def transportationHub(self, path):

        ind = {}
        oud = {}
        node_set = set()
        for x, y in path:
            ind[y] = ind.get(y, 0) + 1
            oud[x] = oud.get(x, 0) + 1
            node_set.add(x)
            node_set.add(y)
        
        for res in node_set:
            if ind.get(res, 0) == len(node_set) - 1 and res not in oud:
                return res
        
        return -1
''',
    call='Solution().transportationHub([[0,1],[0,3],[1,3],[2,0],[2,3]])',
    expect=3,
    views=[
        dict(type='text', size=28, h=70, fn=lambda S: ('当前边：`' + str(S['x']) + ' → ' + str(S['y']) + '`' if 'y' in S and S.get('_line') in (8, 9, 10, 11, 12) else '边：`0→1  0→3  1→3  2→0  2→3`')),
        dict(type='set', var='node_set', label='node_set', fmt=lambda x: str(x), h=130),
        dict(type='map', var='oud', label='oud（出度，没有出边的点不在表里）', fmt=lambda k, v: f'{k}: {v}', h=150),
        dict(type='map', var='ind', label='ind（入度）', fmt=lambda k, v: f'{k}: {v}', h=150),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green'), ('n', 'len(node_set)', 'orange')],
    captions={
        'ind = {}': '`ind`：每个点的入度',
        'oud = {}': '`oud`：每个点的出度；==出度为 0 的点不会出现在里面==',
        'node_set = set()': '`node_set` 收集所有地点，得到点数 n',
        'for x, y in path': lambda S, B, r: ('专线都处理完了，度数统计完毕' if 'x' in B and B.x == S.x and B.y == S.y else f'取一条专线 `{S.x} → {S.y}`'),
        'ind[y] =': '`{y}` 入度 +1 → `ind[{y}] = {ind[y]}`',
        'oud[x] =': '`{x}` 出度 +1 → `oud[{x}] = {oud[x]}`',
        'node_set.add(x)': '起点 `{x}` 入集合',
        'node_set.add(y)': '终点 `{y}` 入集合',
        'for res in node_set': '候选点 `{res}`',
        'if ind.get': lambda S, B, r: (f'`{S.res}` 入度 `{S.ind.get(S.res, 0)}`，要等于 `n − 1 = {len(S.node_set) - 1}`；' + ('不在 `oud` 里（出度 0）→ ==是枢纽==' if S.ind.get(S.res, 0) == len(S.node_set) - 1 and S.res not in S.oud else '条件不全满足，看下一个')),
        'return res': '`{res}` 满足入度 n−1 且出度 0 → 返回 =={res}==',
        'return -1': '没有满足的点 → 返回 `-1`',
    },
    cards=dict(
        one_liner='找入度 n−1、出度 0 的点：统计度数再逐点核对',
        complexity='时间 `O(m + n)`，空间 `O(n)`',
        problem=['`path[i] = [a, b]` 是 a 到 b 的单向专线',
                 '枢纽：其他点都直接通向它，它自己不通向别人',
                 '示例：`[[0,1],[0,3],[1,3],[2,0],[2,3]]` → `3`'],
        quote='题目给出一张图，要求找出图中入度为n - 1，且出度为0的点。',
        quote_src='—— yiduobo 题解原文',
        idea=['隐藏结论：这样的点==不可能有两个==（一个出度为 0，另一个就收不到它的边）',
              '给的是边列表（邻接表），只能遍历所有边统计度数',
              '再遍历每个点，核对入度 n−1 且出度为 0'],
        summary=['时间 `O(m + n)`，空间 `O(n)`',
                 '用 `ind.get(res, 0)`、`res not in oud` 处理没出现的键',
                 'n 是 `len(node_set)`，点编号不一定连续',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
