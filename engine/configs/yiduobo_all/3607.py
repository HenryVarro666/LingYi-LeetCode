C0 = 3
CONN = [[1, 2]]
QS = [[2, 1], [1, 1], [2, 2], [1, 2]]


def _txt(S):
    q = S.get('q')
    if q is not None and 'online' in S:
        return 'queries = ' + ' '.join(f'==[{a},{b}]==' if [a, b] == q else f'`[{a},{b}]`' for a, b in QS)
    if 'network' in S:
        return '`network[根]`：该电网所有电站组成的最小堆'
    return '并查集 `fa[x]`：电站 x 的父亲，同一电网根相同'


CONFIG = dict(
    num=3607, title='电网维护', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='并查集分电网 + 每网一个最小堆（懒删除）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1700'],
    code='''
class Solution(object):
    def processQueries(self, c, connections, queries):
        
        fa = [x for x in range(c + 1)]
        network = {}

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y in connections:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y

        for x in range(1, c + 1):
            fa_x = find(fa, x)
            if fa_x not in network:
                network[fa_x] = []
            network[fa_x].append(x)
        
        for fa_x in network:
            heapq.heapify(network[fa_x])
        
        res = []
        online = [True] * (c + 1)
        for q in queries:
            if q[0] == 1:
                if online[q[1]]:
                    res.append(q[1])
                else:
                    fa_q = find(fa, q[1])
                    while network[fa_q] and not online[network[fa_q][0]]:
                        heapq.heappop(network[fa_q])
                    
                    if network[fa_q]:
                        res.append(network[fa_q][0])
                    else:
                        res.append(-1)
            
            else:
                online[q[1]] = False
        
        return res
''',
    call=f'Solution().processQueries({C0}, {CONN}, {QS})',
    expect=[2, -1],
    skip=['fa_y = find(fa, y)', 'if fa_x not in network', 'network[fa_x] = []', 'if fa[x] != x', 'fa[x] = find(fa, fa[x])', 'return fa[x]'],
    max_steps=130,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='fa', label='fa[x]：并查集父亲（下标 0 不用）', cell=70, h=140,
             color=lambda S, i, v: 'cyan' if i > 0 and v == i else None),
        dict(type='map', var='network', label='network：根 → 电网中的电站（堆）', fmt=lambda k, v: f'{k}: {v}', h=140, font=30),
        dict(type='array', var='online', label='online[x]（红 = 离线）', cell=70, h=140,
             color=lambda S, i, v: 'red' if i > 0 and v is False else ('green' if i > 0 else None)),
        dict(type='array', var='res', label='res', cell=60, h=110, min_slots=5),
    ],
    watch=[('q', 'q', 'blue'), ('fa_q', 'fa_q', 'orange'), ('x', 'x'), ('y', 'y')],
    captions={
        'fa = [x for x': '并查集：每个电站先是自己的根：`fa = {fa}`',
        'network = {}': '`network` 稍后存放：电网的根 → 电网内电站组成的堆',
        'for x, y in connections': lambda S, B, r: (f'`connections` 里的边 `({S.x}, {S.y})`：合并两个电站所在的电网' if 'fa_x' not in S or S.get('_line') == 12 and S.x != B.get('x') or 'x' not in B else '所有边都合并完了'),
        'fa[fa_x] = fa_y': '两个根不同 → 把 `{fa_x}` 挂到 `{fa_y}` 下，==两个电网合并==：`fa = {fa}`',
        'if fa_x != fa_y': lambda S, B, r: (f'两端的根 `{S.fa_x}` ≠ `{S.fa_y}`：还不是同一电网' if S.fa_x != S.fa_y else f'根都是 `{S.fa_x}`：已在同一电网，跳过'),
        'for x in range(1, c + 1)': lambda S, B, r: ('逐个电站找到它的电网根，再分组' if 'x' not in B or S.x <= B.get('x', 0) else f'电站 `{S.x}`：找它的电网根'),
        'fa_x = find(fa, x)': lambda S, B, r: (f'`find` 找到电站 `{S.x}` 的根（带路径压缩）' if S._line == 13 else f'`find` 找到电站 `{S.x}` 的根 `{S.find(S.fa, S.x)}`，按根分电网'),
        'network[fa_x].append(x)': '电站 `{x}` 加入电网 `{fa_x}`：`network[{fa_x}] = {network[fa_x]}`',
        'for fa_x in network': '每个电网各建一个最小堆',
        'heapq.heapify': '`network[{fa_x}]` 堆化：堆顶 `{network[fa_x][0]}` 是电网最小编号',
        'res = []': '`res` 保存所有 `[1, x]` 的答案',
        'online = [True]': '`online[x]` 记录电站是否在线，开始全部在线（下标 0 不用）',
        'for q in queries': lambda S, B, r: (f'处理询问 `q = {S.q}`' if S.q != B.get('q') or B.get('res') is None or S._line != 29 else '全部询问处理完毕'),
        'if q[0] == 1': lambda S, B, r: ('类型 1：维护检查电站 `%d`' % S.q[1] if S.q[0] == 1 else '类型 2：电站 `%d` 离线' % S.q[1]),
        'if online[q[1]]': lambda S, B, r: (f'电站 `{S.q[1]}` 在线 → 自己解决' if S.online[S.q[1]]
                                            else f'电站 `{S.q[1]}` ==已离线== → 要找同电网最小的在线电站'),
        'res.append(q[1])': '答案就是它自己 `{q[1]}`',
        'fa_q = find(fa, q[1])': '用并查集找到电站 `{q[1]}` 所在电网（根 `{fa_q}`），堆 = `{network[fa_q]}`',
        'while network[fa_q]': lambda S, B, r: ((f'堆顶 `{S.network[S.fa_q][0]}` 已离线 → 懒删除：弹出' if not S.online[S.network[S.fa_q][0]]
                                                 else f'堆顶 `{S.network[S.fa_q][0]}` 在线 → 它就是最小的在线电站，停止弹出') if S.network[S.fa_q]
                                                else '堆已空：电网里没有任何在线电站'),
        'heapq.heappop': '弹出离线的堆顶 → `network[{fa_q}] = {network[fa_q]}`（弹出的不会再回来，离线不可逆）',
        'if network[fa_q]': lambda S, B, r: ('堆非空：堆顶就是答案' if S.network[S.fa_q] else '堆空：没有在线电站'),
        'res.append(network[fa_q][0])': '最小在线电站是 `{network[fa_q][0]}` → 答案',
        'res.append(-1)': '整个电网都离线 → 答案 `-1`',
        'online[q[1]] = False': '电站 `{q[1]}` 标记离线（==只改 online，不动堆==）',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='并查集分电网，每个电网一个最小堆，查询时才弹出离线堆顶',
        complexity='时间 `O((c + n) α + c log c + q log c)`，空间 `O(c)`',
        problem=['`c` 个电站，`connections` 连成若干电网（连通分量）',
                 '`[2,x]`：x 离线；`[1,x]`：x 在线答 x，否则答同电网编号最小的在线电站，没有则 `-1`',
                 '本视频：`c = 3`，边 `[1,2]`，4 条询问'],
        quote='这里可以先对图中的边进行一趟遍历，利用并查集获取每个电网的具体信息……对于每个电网，都使用一个堆来维护该电网中所有在线的电站。',
        quote_src='—— yiduobo 题解原文',
        idea=['一个电网就是无向图的一个连通分量 → 并查集合并边',
              '每个电网存一个最小堆，堆顶就是编号最小的电站',
              '离线时只改 `online`；查询时堆顶离线才弹出：==懒删除=='],
        summary=['时间约 `O((c + n)α + c log c + q log c)`，空间 `O(c)`',
                 '易错：离线==不改变电网结构==，所以电站仍留在 `network` 里',
                 '懒删除：弹出的电站永远离线，不会再上线，所以弹出是安全的',
                 '原文代码已是 Python 3 写法，未做修改（`heapq` 由平台预置）',
                 '对比灵神：他用 DFS 分电网，另有倒序 + 只记最小值的 `O(c+n+q)` 写法'],
    ),
)
