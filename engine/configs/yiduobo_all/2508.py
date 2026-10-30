CODE = '''
class Solution(object):
    def isPossible(self, n, edges):

        g = [set() for _ in range(n + 1)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        nodes = []
        for x in range(1, n + 1):
            if len(g[x]) % 2 == 1:
                nodes.append(x)
        
        if len(nodes) == 0:
            return True

        elif len(nodes) == 2:
            if nodes[0] not in g[nodes[1]]:
                return True
            else:
                for x in range(1, n + 1):
                    if len(g[x]) % 2 == 0 and nodes[0] not in g[x] and nodes[1] not in g[x]:
                        return True
                return False

        elif len(nodes) == 4:
            if nodes[0] not in g[nodes[1]] and nodes[2] not in g[nodes[3]]:
                return True
            if nodes[0] not in g[nodes[2]] and nodes[1] not in g[nodes[3]]:
                return True
            if nodes[0] not in g[nodes[3]] and nodes[1] not in g[nodes[2]]:
                return True
            return False
        
        return False
'''
_LN = {t: k for k, t in enumerate(CODE.split('\n')) if 'nodes[0] not in g[nodes[' in t and 'and nodes[' in t}
_PAIRS = {}
for _t, _k in _LN.items():
    pass
_L4 = sorted(_LN.values())
_PAIRS = {_L4[0]: ((0, 1), (2, 3)), _L4[1]: ((0, 2), (1, 3)), _L4[2]: ((0, 3), (1, 2))}


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    n = S['n']
    g = S.get('g')
    nodes = S.get('nodes')
    done = nodes is not None and S.get('_line', 0) > 13
    line = S.get('_line')
    cv.text((x0 + 18, y0 + 4), '图（橙 = 度数为奇数的点；虚线 = 准备添加的边：绿 = 可添加，红 = 已存在不能加）', 22, T['muted'], bold=True)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 14
    R = min((x1 - x0) / 2 - 90, (y1 - y0) / 2 - 62)
    pos = {}
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / n
        pos[k + 1] = (cx + R * math.cos(a), cy + R * math.sin(a))
    for a, b in S['edges']:
        cv.line([pos[a], pos[b]], T['border'], 3)
    if done and g is not None and len(nodes) == 4 and line in _PAIRS:
        for p, q in _PAIRS[line]:
            u, v = nodes[p], nodes[q]
            ok = u not in g[v]
            cv.dashed(pos[u], pos[v], T['green'] if ok else T['red'], 6)
    if done and g is not None and len(nodes) == 2 and line is not None:
        u, v = nodes
        cv.dashed(pos[u], pos[v], T['green'] if u not in g[v] else T['red'], 6)
    for v in range(1, n + 1):
        X, Y = pos[v]
        isodd = nodes is not None and v in nodes
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=T['orange'] if isodd else T['panel2'], outline=T['border'], width=2, r=30)
        cv.text((X, Y), v, 30, T['bg'] if isodd else T['text'], anchor='mm', bold=True)
        if g is not None and nodes is not None and S.get('_line', 0) > 12:
            cv.text((X, Y + 52), f'度 {len(g[v])}', 20, T['orange'] if isodd else T['dim'], anchor='mm', bold=True)


def _txt(S):
    nodes = S.get('nodes')
    if nodes is None or S.get('_line', 0) <= 12:
        return ''
    k = len(nodes)
    return f'度为奇数的点 `nodes = {nodes}`，共 `{k}` 个'


def _pair_cap(S, B, r):
    a, b, c, d = S.nodes
    pr = _PAIRS[S['_line']]
    (p, q), (s, t) = pr
    nd = S.nodes
    e1, e2 = nd[p], nd[q]
    f1, f2 = nd[s], nd[t]
    ok1, ok2 = e1 not in S.g[e2], f1 not in S.g[f2]
    return (f'方案 `({e1}-{e2}, {f1}-{f2})`：`{e1}-{e2}` {"无边" if ok1 else "已有边"}，'
            f'`{f1}-{f2}` {"无边" if ok2 else "已有边"} → {"==两条都能加，True==" if ok1 and ok2 else "不可行，换下一种"}')


CONFIG = dict(
    num=2508, title='添加边使所有节点度数都为偶数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='奇点计数 · 三种连法逐一检验',
    tags=['灵神题单', '难度分 2060'],
    code=CODE,
    call='Solution().isPossible(5, [[1,2],[3,4],[3,5]])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=430),
        dict(type='text', fn=_txt, h=60, size=28),
    ],
    watch=[('x', 'x', 'yellow'), ('nodes', 'nodes', 'orange')],
    captions={
        'g = [set()': '`g[x]` 是点 x 的邻居集合，下标从 1 开始所以开 `n+1` 个',
        'g[x].add(y)': '无向边 `{x}`-`{y}`：两边都记上',
        'nodes = []': '`nodes` 用来收集度为奇数的点',
        'for x in range': lambda S, B, r: ('所有点检查完，循环结束' if getattr(B, 'x', None) == S.x == S.n else f'检查点 `{S.x}`'),
        'if len(g[x]) % 2 == 1': lambda S, B, r: (f'点 `{S.x}` 的度 = `{len(S.g[S.x])}`，' + ('==奇数== → 收进 nodes' if len(S.g[S.x]) % 2 else '偶数 → 不管')),
        'nodes.append(x)': '`nodes` → `{nodes}`',
        'if len(nodes) == 0': lambda S, B, r: (f'奇点个数 `{len(S.nodes)}`：不是 0' if S.nodes else '没有奇点 → 不用加边'),
        'elif len(nodes) == 2': '奇点个数 `{len(nodes)}`：不是 2（两个奇点才能用一条边连起来）',
        'elif len(nodes) == 4': '奇点个数 `{len(nodes)}`：==四个奇点只能内部两两配对==，共三种连法',
        'return False': lambda S, B, r: ('三种连法都不行 → `False`' if len(S.nodes) == 4 else f'奇点 `{len(S.nodes)}` 个，两条边最多修 4 个 → `False`'),
        'return True': '`True`',
        _L4[0]: _pair_cap,
        _L4[1]: _pair_cap,
        _L4[2]: _pair_cap,
    },
    max_steps=80,
    cards=dict(
        one_liner='一条边只能改两个点的奇偶：奇点超过 4 个就没救',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['无向图 `n` 个点，至多添加 2 条边（无重边、无自环）',
                 '能否让==所有点的度数都变成偶数==',
                 '本视频示例：`n=5, edges=[[1,2],[3,4],[3,5]]` → `True`'],
        quote='由于题目最多只能添加两条边，而一条边可以修改两个节点度的奇偶性，那么若度为奇数的节点大于4，答案必然是False。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍求每个点的度，把奇点收进 `nodes`',
              '0 个：直接 `True`；2 个：连它们，已有边就找一个偶点同时连两个奇点',
              '4 个：`(0-1, 2-3)`、`(0-2, 1-3)`、`(0-3, 1-2)` 三种连法，哪种两条边都不存在就行'],
        summary=['时间 `O(n+m)`，空间 `O(n+m)`',
                 '易错：两个奇点已有边时，要找的偶点必须和==两个奇点都没有边==',
                 '四个奇点的三种配对要全部检查，前一种失败还有后两种',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神用 `defaultdict` 存邻接集；yiduobo 用列表 + 直接按奇点个数写 if/elif，思路相同'],
    ),
)
