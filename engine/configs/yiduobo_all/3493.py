import math

PAL = ['cyan', 'pink', 'green', 'purple', 'orange', 'yellow']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    sets = S.get('num_set')
    fa = S.get('fa')
    if not sets or len(fa) < len(sets) or 'res' not in S:
        return
    n, k = len(sets), S['k']
    line = S['_line']
    i, j = S.get('i'), S.get('j')
    if i is None:
        pairs, cur = [], None
    elif j is None or line == 17:
        pairs, cur = [(a, b) for a in range(i) for b in range(a)], None
    else:
        pairs = [(a, b) for a in range(i) for b in range(a + 1, n) if len(sets[a] & sets[b]) >= k] + \
                [(i, b) for b in range(i + 1, j) if len(sets[i] & sets[b]) >= k]
        cur = (i, j) if j > i else None
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 5
    Rx, Ry = (x1 - x0 - 300) / 2, (y1 - y0 - 230) / 2
    pos = [(cx + Rx * math.sin(2 * math.pi * t / n), cy - Ry * math.cos(2 * math.pi * t / n)) for t in range(n)]
    cv.text((x0 + 18, y0 + 4), '图：节点 = 下标，颜色 = 并查集中的连通块，线 = 交集 >= k 的边', 22, T['muted'], bold=True)
    for a, b in pairs:
        if len(sets[a] & sets[b]) >= k:
            cv.line([pos[a], pos[b]], T['green'], 4)
    if cur is not None:
        a, b = cur
        ok = len(sets[a] & sets[b]) >= k
        cv.line([pos[a], pos[b]], T['yellow'] if ok else T['pink'], 6 if ok else 3)
    for t in range(n):
        px, py = pos[t]
        r = _root(fa, t)
        col = T[PAL[r % len(PAL)]]
        ring = T['yellow'] if cur and t in cur else None
        cv.rect((px - 36, py - 36, px + 36, py + 36), fill=col, outline=ring, width=5, r=36)
        cv.text((px, py), t, 34, T['bg'], anchor='mm', bold=True)
        dx, dy = px - cx, py - cy
        d = math.hypot(dx, dy) or 1
        ox, oy = px + dx / d * 80, py + dy / d * 58
        cv.text((ox, oy), '{' + ','.join(map(str, sorted(sets[t]))) + '}', 26, T['text'], anchor='mm', mono=True)
    if cur is not None:
        a, b = cur
        inter = sorted(sets[a] & sets[b])
        cv.text((x0 + 18, y0 + 40), f'sets[{a}] & sets[{b}]', 22, T['muted'])
        cv.text((x0 + 18, y0 + 70), '{' + ','.join(map(str, inter)) + f'}} : {len(inter)} vs k={k}', 28,
                T['yellow'] if len(inter) >= k else T['pink'], bold=True, mono=True)


_seen = []


def _cap_j(S, B, r):
    key = (S.i, S.j)
    if key == (0, 1) and key in _seen:
        _seen.clear()
    if S.j <= S.i or key in _seen:
        return f'`i = {S.i}` 后面的点都配完了，换下一个 i'
    _seen.append(key)
    return f'配对 `(i, j) = ({S.i}, {S.j})`：数 `num_set[{S.i}]` 里有几个也在 `num_set[{S.j}]` 里'


CONFIG = dict(
    num=3493, title='属性图', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='暴力枚举点对 + 并查集',
    tags=['灵神题单', '难度分 1565'],
    code='''
class Solution(object):
    def numberOfComponents(self, properties, k):
        
        n = len(properties)
        num_set = []
        fa = []
        for index in range(n):
            num_set.append(set(properties[index]))
            fa.append(index)

        def find(x, fa):
            if fa[x] != x:
                fa[x] = find(fa[x], fa)
            return fa[x]

        res = n
        for i in range(n):
            for j in range(i + 1, n):
                same = 0
                for v in num_set[i]:
                    if v in num_set[j]:
                        same += 1
                
                if same >= k:
                    fa_i = find(i, fa)
                    fa_j = find(j, fa)
                    if fa_i != fa_j:
                        fa[fa_i] = fa_j
                        res -= 1
        
        return res
''',
    call='Solution().numberOfComponents([[1,2],[1,3],[1,4],[7,7]], 1)',
    expect=2,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='array', var='fa', label='fa（并查集：fa[x] 是 x 的父亲）',
             pointers={'i': 'blue', 'j': 'pink'}, cell=90, h=170),
    ],
    max_steps=130,
    skip=['fa.append', 'num_set = []', 'fa = []', 'for index', 'num_set.append', 'for v in', 'same = 0', 'n = len'],
    watch=['i', 'j', 'same', ('res', 'res', 'green')],
    captions={
        'fa[x] != x': lambda S, B, r: (f'`fa[{S.x}] != {S.x}`：x 不是根，向上找根并压缩路径' if S.fa[S.x] != S.x else f'`fa[{S.x}] == {S.x}`：x 就是根'),
        'res = n': '`num_set` 是每个节点的集合，`fa[x] = x`：各自成块。答案先设为 `n = {res}`，每成功合并一次减 1',
        'for i in range': lambda S, B, r: ('所有节点都枚举完了' if B.get('i') == S.i else f'取节点 `i = {S.i}`，和它后面的 `j > i` 逐个配对'),
        'for j in range': _cap_j,
        'if v in num_set[j]': lambda S, B, r: (f'`{S.v}` 在 `num_set[{S.j}]` 里吗？' + ('==在==' if S.v in S.num_set[S.j] else '不在')),
        'same += 1': '共同元素 +1：`same = {same}`',
        'if same >= k': lambda S, B, r: (f'`same = {S.same}` ' + ('>=' if S.same >= S.k else '<') + f' `k = {S.k}` → ' + ('==有边==，要看两点是否已连通' if S.same >= S.k else '没边，跳过')),
        'fa_i = find': '找 `i = {i}` 的根：沿 `fa` 往上走，顺手做路径压缩',
        'fa_j = find': '找 `j = {j}` 的根，`fa_i = {fa_i}`',
        'if fa_i != fa_j': lambda S, B, r: (f'根不同（`{S.fa_i}` != `{S.fa_j}`）：属于不同连通块 → 合并' if S.fa_i != S.fa_j else f'根相同（`{S.fa_i}`）：已经连通，答案不变'),
        'fa[fa_i] = fa_j': '把 `{fa_i}` 的根挂到 `{fa_j}` 下：`fa[{fa_i}] = {fa_j}`',
        'res -= 1': '少了一个连通块：`res = {res}`',
        'return res': '剩下 `{res}` 个连通分量',
    },
    cards=dict(
        one_liner='枚举点对数相同元素，够 k 个就合并，答案从 n 往下减',
        complexity='时间 `O(n^2 m)`，空间 `O(nm)`',
        problem=['`properties[i]` 是节点 i 的属性；共同的不同整数 `>= k` 就连边',
                 '求图的连通分量个数',
                 '本视频：`[[1,2],[1,3],[1,4],[7,7]]`，`k = 1` → `2`'],
        quote='若出现的相同元素数量same大于等于k……就通过并查集合并i和j的祖先，并将答案减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n, m <= 100`，直接枚举所有 `(i, j)`，用集合检查 `properties[i]` 的每个元素是否出现在 `properties[j]` 里',
              '数出的 `same >= k` 就连边；并查集记录谁和谁已经连通',
              '答案初值 `n`，只有「根不同」的合并才减 1，重复的边不能多减'],
        summary=['时间 `O(n^2 m)`，空间 `O(nm)`',
                 '`find` 带路径压缩；合并时合并的是两个点的==根==，不是 i 和 j 本身',
                 '易错：根相同时不能减 1，否则会多减',
                 '对比灵神：灵神把并查集封装成类并直接用 `a & b` 求交集；本文手写 `find` 并用循环数 same'],
    ),
)
