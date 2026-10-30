C0 = 3
CONN = [[1, 2]]
QS = [[2, 1], [1, 1], [2, 2], [1, 2], [1, 3]]


def _txt(S):
    L = S.get('_line', 0)
    if 'mn' in S and 'ans' in S:
        i = S.get('i')
        if i is not None and 0 <= i < len(QS) and (24 <= L <= 28 or L >= 37):
            return f'倒着处理第 `{i}` 条询问 `{QS[i]}`'
        return '倒序处理：删除变添加，每个电网只记一个最小值 `mn`'
    if 'offline_time' in S:
        return '`offline_time[x]`：电站 x ==最早==离线的询问下标（`inf` = 始终在线）'
    if 'belong' in S:
        return 'DFS 给每个电站标上电网编号 `belong`'
    return ''


def _qtxt(S):
    i = _qptr(S)
    return 'queries = ' + ' '.join(f'==[{t},{x}]==' if k == i else f'`[{t},{x}]`' for k, (t, x) in enumerate(QS))


def _qptr(S):
    i = S.get('i')
    if 'ans' in S and i is not None and (24 <= S.get('_line', 0) <= 28 or S.get('_line', 0) >= 37):
        return i
    return None


CONFIG = dict(
    num=3607, title='电网维护', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='离线 · 倒序处理 + 维护最小值',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1700'],
    setup='import sys; sys.setrecursionlimit(10000)',
    code='''
class Solution:
    def processQueries(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = [[] for _ in range(c + 1)]
        for x, y in connections:
            g[x].append(y)
            g[y].append(x)

        belong = [-1] * (c + 1)
        cc = 0  # 连通块编号

        def dfs(x: int) -> None:
            belong[x] = cc  # 记录节点 x 在哪个连通块
            for y in g[x]:
                if belong[y] < 0:
                    dfs(y)

        for i in range(1, c + 1):
            if belong[i] < 0:
                dfs(i)
                cc += 1

        # 记录每个节点的离线时间，初始为无穷大（始终在线）
        offline_time = [inf] * (c + 1)
        for i in range(len(queries) - 1, -1, -1):
            t, x = queries[i]
            if t == 2:
                offline_time[x] = i  # 记录离线时间

        # 每个连通块中仍在线的电站的最小编号
        mn = [inf] * cc
        for i in range(1, c + 1):
            if offline_time[i] == inf:  # 最终仍在线
                j = belong[i]
                mn[j] = min(mn[j], i)

        ans = []
        for i in range(len(queries) - 1, -1, -1):
            t, x = queries[i]
            j = belong[x]
            if t == 2:
                if offline_time[x] == i:
                    mn[j] = min(mn[j], x)  # 变回在线
            elif i < offline_time[x]:  # 已经在线（写 < 或者 <= 都可以）
                ans.append(x)
            elif mn[j] != inf:
                ans.append(mn[j])
            else:
                ans.append(-1)
        ans.reverse()
        return ans
''',
    call=f'Solution().processQueries({C0}, {CONN}, {QS})',
    expect=[2, -1, 3],
    skip=['g[x].append', 'g[y].append', 'j = belong[x]', 'j = belong[i]', 'ans = []'],
    max_steps=130,
    views=[
        dict(type='text', fn=_txt, size=26, h=40),
        dict(type='text', fn=_qtxt, size=28, h=70),
        dict(type='array', var='belong', label='belong[x]：电站 x 所在电网（下标 0 不用）', cell=70, h=140,
             color=lambda S, i, v: ['cyan', 'orange', 'purple', 'green', 'pink'][v % 5] if isinstance(v, int) and v >= 0 and i > 0 else None),
        dict(type='array', var='offline_time', label='offline_time[x]', cell=70, h=135,
             color=lambda S, i, v: 'red' if isinstance(v, int) else None),
        dict(type='array', var='mn', label='mn[电网]：在线电站的最小编号', cell=70, h=135,
             color=lambda S, i, v: 'green' if isinstance(v, int) else None),
        dict(type='array', var='ans', label='ans（倒序追加，最后 reverse）', cell=56, h=105, min_slots=5),
    ],
    watch=['x', 't', ('i', 'i', 'blue'), ('j', 'j', 'orange'), ('cc', 'cc', 'purple')],
    captions={
        'g = [[] for': '先把 `connections` 建成邻接表',
        'belong = [-1]': '`belong[x]` 记录电站 x 在哪个电网，`-1` 表示还没访问',
        'cc = 0': '`cc` 是电网编号，从 0 开始',
        'belong[x] = cc': '电站 `{x}` 属于电网 `{cc}`',
        'for y in g[x]': '看电站 `{x}` 的邻居（`g[{x}] = {g[x]}`）',
        'if belong[y] < 0': lambda S, B, r: (f'邻居 `{S.y}` 还没有编号 → 继续 DFS' if S.belong[S.y] < 0
                                             else f'邻居 `{S.y}` 已经属于电网 `{S.belong[S.y]}` → 跳过'),
        'if belong[i] < 0': lambda S, B, r: (f'电站 `{S.i}` 还没分配电网 → ==新电网==，从它开始 DFS' if S.belong[S.i] < 0
                                             else f'电站 `{S.i}` 已被 DFS 访问过，跳过'),
        'cc += 1': 'DFS 结束，整个电网都标好了 → 下一个电网编号 `{cc}`',
        'offline_time = [inf]': '`offline_time[x]` 初始为 `inf`：假设电站始终在线',
        'for i in range(len(queries) - 1, -1, -1):': lambda S, B, r: (
            f'==倒序==扫询问，当前下标 `{S.i}`' if 'i' in S and S.get('i', -1) >= 0 and S.get('i') != B.get('i')
            else '倒序扫描结束'),
        'offline_time[x] = i': '倒着扫，==最后覆盖的就是最早的==离线时间：`offline_time[{x}] = {i}`（同一电站多次离线，只有最早那次算数）',
        'if offline_time[i] == inf': lambda S, B, r: (f'电站 `{S.i}` 从不离线 → 最终在线' if S.offline_time[S.i] == inf
                                                      else f'电站 `{S.i}` 会在询问 `{S.offline_time[S.i]}` 离线 → 先不算'),
        'mn[j] = min(mn[j], i)': '电站 `{i}` 属于电网 `{j}`：电网 `{j}` 的最小在线编号 `mn[{j}] = {mn[j]}`',
        'mn = [inf] * cc': '`mn[j]`：电网 j 中==仍在线==的最小编号，先全设为 `inf`；倒序处理从「时间轴末尾」开始，只有从不离线的电站在线',
        't, x = queries[i]': '第 `{i}` 条询问：类型 `{t}`，电站 `{x}`',
        'if t == 2': lambda S, B, r: (('类型 2：倒着看，这是电站 `%d` 「变回在线」的时刻' % S.x if S.t == 2 else '类型 1：查询') if S._line > 30
                                      else ('类型 2：电站 `%d` 在这条询问离线' % S.x if S.t == 2 else '类型 1 是查询，这一遍不用管')),
        'if offline_time[x] == i': lambda S, B, r: (f'`offline_time[{S.x}] = {S.i}`：正是它==最早==离线的这一刻，倒着看就是此刻上线' if S.offline_time[S.x] == S.i
                                                    else f'`offline_time[{S.x}] = {S.offline_time[S.x]}` ≠ {S.i}：这不是最早的离线，==早就该在线了=='),
        'mn[j] = min(mn[j], x)': '电站 `{x}` 回到电网 `{j}`：最小在线编号 `mn[{j}] = {mn[j]}`',
        'elif i < offline_time[x]': lambda S, B, r: (f'`{S.i} < offline_time[{S.x}] = {S.offline_time[S.x]}`：询问发生时电站 `{S.x}` 还没离线 → 直接答 `{S.x}`' if S.i < S.offline_time[S.x]
                                                     else f'`{S.i} ≥ offline_time[{S.x}] = {S.offline_time[S.x]}`：询问时电站 `{S.x}` 已离线 → 找电网最小值'),
        'ans.append(x)': '答案 `{x}`',
        'elif mn[j] != inf': lambda S, B, r: (f'电网 `{S.j}` 的最小在线编号 `mn[{S.j}] = {S.mn[S.j]}`，存在' if S.mn[S.j] != inf
                                              else f'电网 `{S.j}` 此刻没有在线电站（`mn = inf`）'),
        'ans.append(mn[j])': '电网里最小在线电站是 `{mn[j]}` → 答案',
        'ans.append(-1)': '整个电网都不在线 → 答案 `-1`',
        'ans.reverse()': '倒序追加的答案，翻回原顺序：`{ans}`',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='倒着看：离线变上线，每个电网只需记一个最小值',
        complexity='时间 `O(c + n + q)`，空间 `O(c + n)`',
        problem=['`c` 个电站，`connections` 把它们连成若干电网',
                 '`[2,x]`：x 离线；`[1,x]`：x 在线答 x，否则答同电网编号最小的在线电站，没有则 `-1`',
                 '本视频：`c = 3`，边 `[1,2]`，5 条询问'],
        quote='倒序处理询问，==离线变成在线，删除变成添加==，每个连通块只需要一个 int 变量就可以维护最小值。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先 DFS 给每个电站标上电网编号 `belong`',
              '记录电站最早离线的询问下标 `offline_time`；倒着走到那一刻，电站才「上线」',
              '`mn[j]` 只增不减地取 `min`，无需堆，不用删除'],
        summary=['时间 `O(c + n + q)`，空间 `O(c + n)`',
                 '易错：同一电站可能多次离线，==必须取最早==那次（倒序扫时后写覆盖即可）',
                 '倒序时「变回在线」只在 `offline_time[x] == i` 发生一次',
                 '方法一：每个电网一个最小堆 + 懒删除，堆顶离线才弹出，`O(q log c)`'],
    ),
)
