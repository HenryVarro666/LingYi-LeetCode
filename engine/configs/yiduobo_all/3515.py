CONFIG = dict(
    num=3515, title='带权树中的最短路径', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='dfs 序 + 线段树区间修改单点查询',
    tags=['线段树', 'DFS 序', '难度分 2312'],
    code='''
class Solution(object):
    def treeQueries(self, n, edges, queries):
        
        g = {x : {} for x in range(1, n + 1)}
        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w

        pos = {}
        order = []
        length = {}
        cover = {}

        def dfs(pre, now, s, pos, order, length, cover):
            order.append(now)
            pos[now] = len(order) - 1
            length[now] = s

            for nxt in g[now]:
                if nxt == pre:
                    continue
                dfs(now, nxt, s + g[now][nxt], pos, order, length, cover)
            
            cover[now] = len(order) - pos[now]
        
        dfs(0, 1, 0, pos, order, length, cover)
        
        def update(now, left, right, start, end, v):
            if left == start and right == end:
                delta[now] += v
                return
            
            mid = (left + right) // 2
            if end <= mid:
                update(now + now + 1, left, mid, start, end, v)
            elif start > mid:
                update(now + now + 2, mid + 1, right, start, end, v)
            else:
                update(now + now + 1, left, mid, start, mid, v)
                update(now + now + 2, mid + 1, right, mid + 1, end, v)
        
        def get(now, left, right, p):
            if left == right:
                return delta[now]
            
            mid = (left + right) // 2
            if p <= mid:
                return delta[now] + get(now + now + 1, left, mid, p)
            else:
                return delta[now] + get(now + now + 2, mid + 1, right, p)

        n = len(order)
        delta = [0] * (n * 4)
        res = []
        for q in queries:
            if q[0] == 1:
                x, y, w = q[1:]
                if pos[x] < pos[y]:
                    p = y
                else:
                    p = x

                update(0, 0, n - 1, pos[p], pos[p] + cover[p] - 1, w - g[x][y])
                g[x][y] = w
                g[y][x] = w
            else:
                res.append(length[q[1]] + get(0, 0, n - 1, pos[q[1]]))
        
        return res
''',
    call='Solution().treeQueries(4, [[1,2,3],[2,3,1],[1,4,2]], [[2,3],[1,1,2,5],[2,3]])',
    expect=[4, 6],
    views=[
        dict(type='array', var='order', label='order：dfs 访问顺序（下标 = 时间戳）', h=150,
             color=lambda S, i, v: 'yellow' if S.get('p') is not None and S.get('pos') and i in range(S['pos'].get(S['p'], 99), S['pos'].get(S['p'], 99) + S.get('cover', {}).get(S['p'], 0)) and S.get('_line', 0) >= 54 else None),
        dict(type='map', var='length', label='length[x]：初始到根距离', h=130, font=22),
        dict(type='map', var='cover', label='cover[x]：x 管辖 order 里的几个点', h=130, font=22),
        dict(type='array', var='delta', label='delta：线段树，区间修改打在节点上（单点查询时沿路累加）', h=150, cell=60),
        dict(type='calls', h=130, hide=('pos', 'order', 'length', 'cover')),
    ],
    watch=['p', 'v', ('res', 'res', 'green')],
    captions={
        'g = {x : {}': '邻接表：`g[x][y] = 边权`，方便之后查到、改掉边权',
        'order.append(now)': '访问 `{now}`：加入 order → 它的时间戳 = 下标 `{len(order)-1}`',
        'pos[now] = len(order) - 1': '`pos[{now}] = {pos[now]}`',
        'length[now] = s': '`length[{now}] = {s}`：根到 {now} 的初始距离',
        'cover[now] = len(order) - pos[now]': '子树遍历完：`cover[{now}] = {cover[now]}`，它的子树就是 order 里 `[{pos[now]}, {pos[now]+cover[now]-1}]`',
        'dfs(now, nxt': '递归进入孩子 `{nxt}`',
        'n = len(order)': '线段树建在 order 上：区间长度 `{n}`',
        'delta = [0]': '线段树全 0，`delta[node]` 记录整段区间要加的值',
        'if pos[x] < pos[y]': '`pos[{x}]={pos[x]}` 与 `pos[{y}]={pos[y]}` 比较：先访问的是父亲 → ==后访问的是孩子 p==',
        'update(0, 0, n - 1': '把子树 `p={p}` 对应区间 `[{pos[p]}, {pos[p]+cover[p]-1}]` 整体加 `{w - g[x][y]}`（新权 − 旧权）',
        'res.append': '查询节点 `{q[1]}`：`length[{q[1]}]` + 线段树在 `pos` 处的单点值（沿路径累加 delta）',
        'if left == start and right == end': lambda S, B, r: ('区间正好吻合 → 这个节点 `delta` 加 `v`，不再往下' if S.left == S.start and S.right == S.end else '区间没吻合，继续拆分'),
        'delta[now] += v': '`delta[{now}] += {v}`',
        'return delta[now] + get(now + now + 1': '`p={p} <= mid={mid}`：往左走，累加这一层的 `delta[{now}]={delta[now]}`',
        'return delta[now] + get(now + now + 2': '`p={p} > mid={mid}`：往右走，累加 `delta[{now}]={delta[now]}`',
        'return delta[now]': '到叶子：返回路径上的 delta 之和',
        'return res': '所有查询结果 `{res}`',
    },
    skip=['dfs(0, 1', 'order = []', 'pos = {}', 'length = {}', 'cover = {}', 'def ', 'mid = ', 'g[y][x] = w', 'g[x][y] = w', 'for nxt in g', 'if left == right', 'if p <= mid', 'x, y, w = q[1:]', 'continue', 'for x, y, w in edges', 'else:', 'res = []'],
    max_steps=95,
    cards=dict(
        one_liner='子树 = dfs 序里的一段区间：改边权就是区间整体加',
        complexity='时间 `O((n+q) log n)`，空间 `O(n)`',
        problem=['以 1 为根的无向带权树，`[1,u,v,w]` 改边权，`[2,x]` 查根到 x 的距离',
                 '返回所有查询的答案',
                 '本视频：`edges=[[1,2,3],[2,3,1],[1,4,2]]`，结果 `[4,6]`'],
        quote='对于这类修改子树中所有节点值的问题，一种常见的处理方法是通过dfs，将树的问题转化为区间的问题，然后使用可以处理区间问题的方法，例如线段树来进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['dfs 时用 `order` 记访问顺序、`pos` 记下标、`cover[now]` 记子树管多少个点',
              '改孩子 `p` 的边权：子树区间 `[pos[p], pos[p]+cover[p]-1]` 整体加 `w−旧权`',
              '查询 = 初始距离 `length[x]` + 线段树在 `pos[x]` 处的单点值（沿根到叶的路径累加 `delta`）'],
        summary=['时间 `O((n+q) log n)`，空间 `O(n)`',
                 '要先判断 x、y 谁是孩子：`pos` 小的是父亲',
                 '区间修改不下推：整段吻合就记在该节点，查询时沿路求和',
                 '改完要同步更新 `g[x][y]`，下次才能算出增量',
                 '对比灵神：灵神用差分树状数组，区间加变两次单点更新',
                 '原文代码无需改动即可在 Python 3 运行'],
    ),
)
