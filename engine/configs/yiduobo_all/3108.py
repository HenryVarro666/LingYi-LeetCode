N0 = 5
E0 = [[0, 1, 7], [1, 2, 1], [3, 4, 6]]
Q0 = [[0, 2], [2, 3]]
POS = {0: (0.08, 0.25), 1: (0.32, 0.55), 2: (0.12, 0.88), 3: (0.68, 0.25), 4: (0.92, 0.75)}
COLS = ['blue', 'orange', 'green', 'purple']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    bel = S.get('belong')
    line = S.get('_line', 0)
    cur = S.get('index') if line in (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24) else None
    hot = None
    if 'x' in S and 'y' in S and 'w' in S and line in (29, 30, 31, 32):
        hot = {S['x'], S['y']}
    elif 'x' in S and 'y' in S and line in (19, 20, 21, 22, 23) and 'head' in S:
        hot = {S['x'], S['y']}
    W, H = x1 - x0 - 80, y1 - y0 - 110
    P = {k: (x0 + 40 + v[0] * W, y0 + 60 + v[1] * H) for k, v in POS.items()}
    cv.text((x0 + 18, y0 + 4), '带权无向图（颜色 = 所属连通子图，黄边 = 正在处理的边）', 22, T['muted'], bold=True)
    for u, v, w in E0:
        h = hot is not None and hot == {u, v}
        cv.line([P[u], P[v]], T['yellow'] if h else T['border'], 6 if h else 3)
        mx, my = (P[u][0] + P[v][0]) / 2, (P[u][1] + P[v][1]) / 2
        cv.rect((mx - 20, my - 16, mx + 20, my + 16), fill=T['panel2'], r=8)
        cv.text((mx, my), w, 24, T['yellow'] if h else T['text'], anchor='mm', bold=True, mono=True)
    for k, (px, py) in P.items():
        cid = bel[k] if bel is not None else None
        fill = T[COLS[cid % 4]] if cid is not None else T['panel2']
        if k == cur:
            cv.rect((px - 40, py - 40, px + 40, py + 40), outline=T['yellow'], width=5, r=40)
        cv.rect((px - 32, py - 32, px + 32, py + 32), fill=fill, outline=T['border'], r=32)
        cv.text((px, py), k, 32, T['bg'] if cid is not None else T['muted'], anchor='mm', bold=True, mono=True)


def _val(S):
    v = S.get('val')
    if v is None:
        return ''
    return '各连通子图的 AND（`val`）：' + '，'.join(f'子图 {i} = {x}' for i, x in enumerate(v))


CONFIG = dict(
    num=3108, title='带权图里旅途的最小代价', difficulty='Hard', category='位运算',
    author='yiduobo', technique='BFS 划分连通子图 + 边权 AND',
    tags=['灵神题单·位运算', '灵神题单·图论算法', '难度分 2109'],
    code='''
class Solution(object):
    def minimumCost(self, n, edges, query):

        g = [set() for index in range(n)]
        for x, y, w in edges:
            g[x].add(y)
            g[y].add(x)
        
        belong = [None] * n
        tot = 0
        for index in range(n):
            if belong[index] is None:
                belong[index] = tot
                q = [index]
                head, tail = 0, 1
                while head < tail:
                    for x in q[head : tail]:
                        for y in g[x]:
                            if belong[y] is None:
                                belong[y] = tot
                                q.append(y)

                    head, tail = tail, len(q)
                
                tot += 1
        
        val = [None] * tot
        for x, y, w in edges:
            if val[belong[x]] is None:
                val[belong[x]] = w
            else:
                val[belong[x]] &= w
        
        res = []
        for x, y in query:
            if belong[x] != belong[y]:
                res.append(-1)
            else:
                res.append(val[belong[x]])
        
        return res
''',
    call=f'Solution().minimumCost({N0}, {E0}, {Q0})',
    expect=[1, -1],
    skip=['g[x].add', 'g[y].add', 'for x, y, w in edges', 'g = [set()', 'for index in range(n)', 'for x in q[head', 'for y in g[x]',
          'head, tail = 0, 1', 'q = [index]'],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=300),
        dict(type='array', var='belong', label='belong（每个点属于哪个连通子图）', h=150, cell=70),
        dict(type='text', fn=_val, size=26, h=60),
    ],
    watch=[('index', 'index', 'blue'), ('tot', 'tot', 'pink'), ('q', 'q', 'orange'), ('val', 'val', 'green')],
    captions={
        'belong = [None]': '`belong[i]` 记录点 `i` 属于哪个连通子图，`None` 表示还没访问',
        'tot = 0': '`tot` 是连通子图的个数，也是下一个子图的编号',
        'if belong[index] is None': lambda S, B, r: (f'点 `{S.index}` 还没归属 → 从它开始 BFS，找出整个连通子图' if S.belong[S.index] is None
                                                     else f'点 `{S.index}` 已经属于子图 `{S.belong[S.index]}` → 跳过'),
        'belong[index] = tot': '起点 `{index}` 归入子图 `{tot}`',
        'while head < tail': lambda S, B, r: (f'这一层还有 `{S.tail - S.head}` 个点要展开，继续 BFS' if S.head < S.tail
                                             else '没有新点了：这个连通子图找完'),
        'if belong[y] is None': lambda S, B, r: (f'邻居 `{S.y}` 没访问过 → 归入同一个子图' if S.belong[S.y] is None
                                                else f'邻居 `{S.y}` 已经访问过 → 不重复加入'),
        'belong[y] = tot': '点 `{y}` 归入子图 `{tot}`，随后加进队列 `q`',
        'head, tail = tail': '这层展开完，下一层范围：`head={head}, tail={tail}`',
        'tot += 1': '一个子图找完，子图个数 `tot` → {tot}',
        'val = [None]': '`val[k]` 存放子图 `k` 的边权 AND，先全是 `None`',
        'if val[belong[x]] is None': lambda S, B, r: (f'边 `({S.x},{S.y},{S.w})` 属于子图 `{S.belong[S.x]}`：' + ('还没有值，先放入边权' if S.val[S.belong[S.x]] is None else '已有值，继续做 AND')),
        'val[belong[x]] = w': '子图 `{belong[x]}` 的 `val` = `{w}`',
        'val[belong[x]] &= w': '边必须走：子图 `{belong[x]}` 的 AND → =={val[belong[x]]}==（越与越小）',
        'res = []': '依次回答每个查询',
        'if belong[x] != belong[y]': lambda S, B, r: (f'查询 `({S.x},{S.y})`：属于子图 `{S.belong[S.x]}` 和 `{S.belong[S.y]}`，' + ('不同 → 不连通' if S.belong[S.x] != S.belong[S.y] else '同一个 → 连通')),
        'res.append(-1)': '不连通 → 答案 `-1`',
        'res.append(val': '连通 → 答案是该子图的 AND = =={res[-1]}==',
        'return res': '全部答案：`{res}`',
    },
    cards=dict(
        one_liner='边越多 AND 越小：连通就把整个子图的边走遍',
        complexity='时间 `O(n+m+q)`，空间 `O(n+m)`',
        problem=['带权无向图，旅途代价 = 所经边权的按位与，点和边可重复走',
                 '每个查询求 `s` 到 `t` 的最小代价，不连通为 `-1`',
                 '本视频：`n=5`，边 `[[0,1,7],[1,2,1],[3,4,6]]`，查询 `[[0,2],[2,3]]`'],
        quote='如果询问中的两点属于同一个连通子图，那么就应该走遍这张子图中的所有边，这样一来才能使得路径的代价最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['按位与要最小，经过的边==越多越好==',
              '先遍历所有点，用 BFS 划分连通子图',
              '再遍历所有边，把边权 AND 进它所属子图',
              '查询：不在同一子图 `-1`，否则取子图的值'],
        summary=['时间 `O(n+m+q)`，空间 `O(n+m)`',
                 '用 `None` 表示子图还没有值，第一条边直接赋值，避免初值问题',
                 '用一个列表 + `head/tail` 做分层 BFS',
                 '对比灵神：灵神 DFS 里顺手算 AND（初值 -1）；这里先分子图再单独遍历边'],
    ),
)
