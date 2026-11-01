def _cant(S):
    c = S.get('cant')
    if c is None:
        return None
    return {i: sorted(d) for i, d in enumerate(c) if d}


def _groups(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    n = len(fa)

    def root(x):
        while fa[x] != x:
            x = fa[x]
        return x
    g = {}
    for i in range(n):
        g.setdefault(root(i), []).append(i)
    return '朋友圈：' + '　'.join('{' + ','.join(map(str, v)) + '}' for v in g.values())


def _req(S):
    i = S.get('i')
    rs = S.get('requests')
    if i is None or rs is None or S.get('_line', 0) < 22:
        return _groups(S)
    return f"请求 {i}：`{rs[i][0]} — {rs[i][1]}`　　" + _groups(S)


CONFIG = dict(
    num=2076, title='处理含限制条件的好友请求', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='并查集 + 代表元上记录限制，启发式合并（Go 原文转写）',
    tags=['常用数据结构', '难度分 2131'],
    code='''
class Solution:
    def friendRequests(self, n: int, restrictions: List[List[int]], requests: List[List[int]]) -> List[bool]:
        fa = list(range(n))  # 初始化并查集

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        cant = [{} for _ in range(n)]
        for r in restrictions:  # 初始化无法成为朋友的用户
            v, w = r[0], r[1]
            cant[v][w] = True
            cant[w][v] = True  # 双向

        ans = [False] * len(requests)
        for i, r in enumerate(requests):
            v, w = find(r[0]), find(r[1])
            if v == w:  # 已经是朋友（直接或间接）
                ans[i] = True
                continue
            if cant[v].get(w):  # 无法成为朋友
                continue
            ans[i] = True
            if len(cant[v]) > len(cant[w]):  # 启发式合并：总是从小的集合合并到大的集合上
                v, w = w, v
            for x in cant[v]:  # 将 cant[v] 中的代表元合并到 cant[w] 上
                x = find(x)
                cant[w][x] = True
                cant[x][w] = True  # 双向
            fa[v] = w
        return ans
''',
    call='Solution().friendRequests(5, [[0,1],[1,2],[2,3]], [[0,4],[1,2],[3,1],[3,4]])',
    expect=[True, False, True, False],
    skip=['def find', 'v, w = r[0], r[1]', 'cant[w][v] = True'],
    views=[
        dict(type='text', fn=_req, size=24, h=60),
        dict(type='array', var='fa', label='fa 并查集（fa[i] = i 的是代表元）', cell=80, h=150,
             color=lambda S, i, v: 'blue' if S['fa'][i] == i else None,
             pointers={}),
        dict(type='map', var=_cant, label='cant[代表元] = 不能成为朋友的用户', fmt=lambda k, v: f'{k} 不能加 {v}', h=200),
        dict(type='array', var='ans', label='ans（True = 请求成功）', cell=80, h=140,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('i', 'i', 'blue'), ('v', 'v', 'pink'), ('w', 'w', 'yellow')],
    captions={
        'fa = list': '并查集：每个用户一开始自成一个朋友圈',
        'cant = [{}': '每个用户一份「不能成为朋友」名单；最终只在代表元上维护',
        'cant[v][w] = True': '限制 `{v}` 与 `{w}`：名单里互相登记（双向）',
        'for i, r in enumerate': lambda S, B, r: ('所有请求都处理完了' if B.get('i') == S.get('i') else f'处理请求 {S.i}：用户 `{S.requests[S.i][0]}` 和 `{S.requests[S.i][1]}`'),
        'v, w = find': '用 `find` 找出两个用户所在朋友圈的代表元，记为 `v`、`w`',
        'if v == w': lambda S, B, r: (f'`{S.v} == {S.w}`：已经在同一个朋友圈 → ==请求成功==' if S.v == S.w else f'`{S.v} != {S.w}`：不在同一圈，要看有没有限制'),
        'if cant[v].get(w)': lambda S, B, r: (f'`cant[{S.v}]` 里有 `{S.w}`：合并会让受限制的两人变朋友 → ==请求失败==' if S.cant[S.v].get(S.w)
                                               else f'`cant[{S.v}]` 里没有 `{S.w}`：合并安全 → ==请求成功，合并两个圈=='),
        'if len(cant[v]) > len(cant[w])': lambda S, B, r: (f'`{len(S.cant[S.v])} > {len(S.cant[S.w])}`：`v` 的名单更长 → 交换，==总是小的合并到大的上==' if len(S.cant[S.v]) > len(S.cant[S.w])
                                                          else f'`{len(S.cant[S.v])} <= {len(S.cant[S.w])}`：`v` 名单不比 `w` 长，不用交换'),
        'for x in cant[v]': '逐个把 `v` 名单上的人转移到 `w` 的名单上（名单走完则结束）',
        'x = find(x)': '名单里的人换成他所在圈的代表元 `x`',
        'cant[w][x] = True': '`w` 的名单加上这个代表元',
        'cant[x][w] = True': '这个代表元的名单也加上 `w`（双向）',
        'fa[v] = w': '`fa[{v}] = {w}`：圈 `{v}` 并入圈 `{w}`',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='在并查集的代表元上，记下这个朋友圈「不能加谁」',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`restrictions[i]=[x,y]`：用户 x、y 不能成为朋友（直接或间接）',
                 '按顺序处理 `requests`：不违反任何限制才成功，成功后成为直接朋友',
                 '示例：`n=5`，限制 `[[0,1],[1,2],[2,3]]`，请求 `[[0,4],[1,2],[3,1],[3,4]]` → `[true,false,true,false]`'],
        quote='用并查集维护朋友关系。同时我们还要处理哪些用户不能成为朋友，这可以用哈希表来维护。更具体地，我们可以在并查集的代表元上记录当前集合与哪些用户不能成为朋友。',
        quote_src='—— 灵茶山艾府题解',
        idea=['请求 `(u, v)`：先 `find` 出代表元；同圈直接成功',
              '不同圈：看代表元的「不能」名单里有没有对方 → 有就失败',
              '合并时==小名单并入大名单==（启发式合并），名单里的人要换成代表元'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]bool` 用 dict；判断 `cant[v][w]` 用 `.get`，缺键相当于 false）',
                 '时间 `O(n log n)`（启发式合并），空间 `O(n)`',
                 '易错点：名单里存的必须是代表元，合并后要用 `find` 重新归一',
                 '请求已经是朋友（同圈）时依然成功'],
    ),
)
