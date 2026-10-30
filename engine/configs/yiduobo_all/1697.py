def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    se = S.get('sorted_edge')
    if se is None:
        cv.text((x0 + 18, y0 + 4), '边按长度排序后，一条条加入并查集（绿 = 已加入）', 24, T['muted'], bold=True)
        return
    pos = S.get('pos', 0)
    lim = S.get('l')
    inn = S.get('_inner', {})
    cv.text((x0 + 18, y0 + 4), '排序后的边（绿 = 已并入；黄 = 下一条；数字黄 = 长度 >= limit，本次用不上）', 24, T['muted'], bold=True)
    n = len(se)
    cw = min(150, (x1 - x0 - 40) / n)
    sx = x0 + 20
    for i, (a, b, d) in enumerate(se):
        cx = sx + i * cw
        if i < pos:
            fill, ol = (30, 70, 40), T['green']
        elif i == pos:
            fill, ol = T['panel2'], T['yellow']
        else:
            fill, ol = T['panel2'], T['border']
        cv.rect((cx + 4, y0 + 50, cx + cw - 4, y0 + 130), fill=fill, outline=ol, width=3, r=10)
        cv.text((cx + cw / 2, y0 + 78), f'{a}-{b}', 28, T['text'], anchor='mm', bold=True)
        cv.text((cx + cw / 2, y0 + 110), f'长 {d}', 22, T['yellow'] if (lim is not None and d >= lim) else T['muted'], anchor='mm')
    qs = S.get('queries')
    if 'q_ind' in S or 'x' in S and 'q_ind' in inn:
        cv.text((x0 + 18, y0 + 160), '按 limit 排序后的询问（蓝 = 当前；绿/红 = 已回答 True/False）', 24, T['muted'], bold=True)
        order = sorted(range(len(qs)), key=lambda k: qs[k][2])
        qw = min(190, (x1 - x0 - 40) / len(qs))
        res = S.get('res') or []
        cur = S.get('q_ind')
        done = S.get('_done', set())
        for j, k in enumerate(order):
            p, q, L = qs[k][:3]
            cx = sx + j * qw
            curpos = order.index(cur) if cur in order else -1
            answered = j < curpos or (j == curpos and S['_line'] >= 29)
            ol = T['blue'] if k == cur else (T['green'] if answered and res[k] else T['red'] if answered else T['border'])
            cv.rect((cx + 4, y0 + 200, cx + qw - 4, y0 + 280), fill=T['panel2'], outline=ol, width=4 if (k == cur or answered) else 2, r=10)
            cv.text((cx + qw / 2, y0 + 226), f'{p} → {q}', 26, T['text'], anchor='mm', bold=True)
            cv.text((cx + qw / 2, y0 + 258), f'limit {L}', 22, T['muted'], anchor='mm')


CONFIG = dict(
    num=1697, title='检查边长度限制的路径是否存在', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='离线询问 + 排序 + 并查集',
    tags=['灵神题单·图论算法', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def distanceLimitedPathsExist(self, n, edgeList, queries):

        sorted_edge = sorted(edgeList, key=lambda d:d[2])
        m = len(sorted_edge)
        pos = 0
        f = list(range(n))

        q = len(queries)
        for index in range(q):
            queries[index].append(index)
        res = [False] * q
        
        for x, y, l, q_ind in sorted(queries, key=lambda d:d[2]):
            while pos < m and sorted_edge[pos][2] < l:
                fa_p = self.find(sorted_edge[pos][0], f)
                fa_q = self.find(sorted_edge[pos][1], f)
                if fa_p != fa_q:
                    if fa_p < fa_q:
                        f[fa_p] = fa_q
                    else:
                        f[fa_q] = fa_p

                pos += 1
            
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            res[q_ind] = fa_x == fa_y
        
        return res
    
    def find(self, x, f):
        if f[x] != x:
            f[x] = self.find(f[x], f)
        
        return f[x]
''',
    call='Solution().distanceLimitedPathsExist(5, [[0, 1, 2], [1, 2, 4], [2, 3, 6], [3, 4, 3]], [[0, 2, 5], [0, 3, 5], [0, 4, 7], [1, 4, 4]])',
    expect=[True, False, True, False],
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='f', label='f（并查集：f[i] = i 的父节点）', cell=80, h=140,
             color=lambda S, i, v: 'green' if v == i else None),
        dict(type='array', var='res', label='res（每个询问的答案，按原顺序）', cell=80, h=130,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('pos', 'pos', 'yellow'), ('limit', lambda S: S.get('l'), 'blue'), ('q_ind', 'q_ind', 'pink')],
    skip=['m = len(sorted_edge)', 'pos = 0', 'q = len(queries)', 'for index in range', 'if f[x] != x', 'f[x] = self.find',
          'return f[x]', 'fa_p = self.find', 'fa_q = self.find', 'if fa_p < fa_q', 'fa_x = self.find', 'fa_y = self.find'],
    captions={
        'sorted_edge = sorted': '先把所有边按长度从小到大排序：`{[e[2] for e in sorted_edge]}`',
        'f = list(range(n))': '并查集初始化：每个点自己是一个集合，`f[i] = i`',
        'queries[index].append': '给询问 {index} 记下原始下标 `{index}`（马上要重新排序）',
        'res = [False]': '`res` 先全是 False，按原下标填答案',
        'for x, y, l, q_ind in sorted': '==离线==：按 limit 从小到大处理询问 → 当前询问 `{x} → {y}`，`limit = {l}`',
        'while pos < m and': lambda S, B, r: (
            f'下一条边长 `{S.sorted_edge[S.pos][2]}` < limit `{S.l}` → 加入图' if S.pos < S.m and S.sorted_edge[S.pos][2] < S.l
            else f'没有更多长度 < `{S.l}` 的边了（limit 只增不减，之前加的边都还有效）'),
        'if fa_p != fa_q': lambda S, B, r: (
            f'两端根节点 `{S.fa_p}` 和 `{S.fa_q}` 不同 → 合并两个集合' if S.fa_p != S.fa_q
            else f'两端根节点都是 `{S.fa_p}`，早已连通，什么都不用做'),
        'f[fa_p] = fa_q': '合并：编号小的根挂到大的根下，`f[{fa_p}] = {fa_q}`',
        'f[fa_q] = fa_p': '合并：`f[{fa_q}] = {fa_p}`',
        'pos += 1': '这条边处理完，`pos` → {pos}',
        'res[q_ind] =': lambda S, B, r: (
            f'`{S.x}` 的根 `{S.fa_x}`，`{S.y}` 的根 `{S.fa_y}`：' + ('==相同== → 只用 < limit 的边就能连通，True'
                                                                if S.fa_x == S.fa_y else '不同 → 不连通，False')
            + f'；写入 `res[{S.q_ind}]`'),
        'return res': '全部询问处理完，答案 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='把询问按 limit 排序，边也排序，边加边答',
        complexity='时间 `O((m+q) log)`，空间 `O(n+q)`',
        problem=['无向图 `n` 个点，`edgeList[i] = [u, v, 长度]`；每个询问 `[p, q, limit]`',
                 '问：`p` 到 `q` 有没有一条路，路上==每条边长度都严格小于 limit==',
                 '示例：`n=5` 小图，4 条边、4 个询问 → `[True, False, True, False]`'],
        quote='如果询问中的limit是按照大小顺序从小到大排列好的话，那么后一次询问就可以在前一次询问已经建好的图的基础上添加部分边然后求解。',
        quote_src='—— yiduobo 题解',
        idea=['每个询问都重新建图再 bfs，复杂度 `O((n+m)q)`，太慢',
              '==离线==：先收集所有询问，按 limit 排序，后一个询问沿用前一个建好的图，只补加新边',
              '连通性用并查集维护：加边 = 合并集合，回答 = 比较两点的根'],
        result='4 个询问全部答完 ✓',
        summary=['时间 `O(m log m + q log q + (m+q)α)`，空间 `O(n+q)`',
                 '边的条件是 ==`< limit`==，严格小于，所以 while 里用 `<`',
                 '询问排序后要记下原下标 `q_ind`，答案才能放回原位置',
                 '原文为 Python 2 写法，`f = range(n)` 已改为 `f = list(range(n))`（Python 3 的 range 不能赋值）',
                 '同类题：1724、2092 等离线 + 并查集'],
    ),
)
