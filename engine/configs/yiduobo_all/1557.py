import math as _m


def _gdraw(cv, box, T, pos, edges, state, sub=None, hot=None, title='', R=30, fs=26):
    """有向图：pos={名字:(fx,fy)}，edges=[(a,b)]，state={名字:颜色名或None}，sub={名字:下方小字}，hot=高亮边 (a,b)"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    half = {k: max(R, (cv.tlen(k, fs, bold=True) + 30) / 2) for k in pos}
    mx = max(half.values())
    w, h = x1 - x0 - 2 * mx - 40, y1 - y0 - 2 * R - 100
    P = {k: (x0 + 20 + mx + fx * w, y0 + 50 + R + fy * h) for k, (fx, fy) in pos.items()}

    def edge_pt(k, ux, uy, pad):
        a, b = half[k] + pad, R + pad
        t = 1 / _m.sqrt((ux / a) ** 2 + (uy / b) ** 2)
        return t

    for a, b in edges:
        if a not in P or b not in P:
            continue
        (ax, ay), (bx, by) = P[a], P[b]
        d = _m.hypot(bx - ax, by - ay) or 1
        ux, uy = (bx - ax) / d, (by - ay) / d
        ta, tb = edge_pt(a, ux, uy, 3), edge_pt(b, ux, uy, 6)
        on = hot is not None and (a, b) == tuple(hot)
        cv.arrow((ax + ux * ta, ay + uy * ta), (bx - ux * tb, by - uy * tb),
                 T['yellow'] if on else T['dim'], width=6 if on else 3, head=16 if on else 13)
    for k, (cx, cy) in P.items():
        c = state.get(k)
        fill = T[c] if c else T['panel2']
        cv.rect((cx - half[k], cy - R, cx + half[k], cy + R), fill=fill, outline=T['border'], width=3, r=R)
        cv.text((cx, cy), k, fs, T['bg'] if c else T['text'], anchor='mm', bold=True)
        if sub and sub.get(k) not in (None, ''):
            cv.text((cx, cy + R + 6), sub[k], 22, T['muted'], anchor='mt', bold=True)


POS = {0: (0.08, 0.3), 3: (0.08, 0.85), 1: (0.58, 0.05), 2: (0.58, 0.45), 4: (0.3, 0.92), 5: (0.92, 0.45)}
EDGES = [(0, 1), (0, 2), (2, 5), (3, 4), (4, 2)]


def _draw(cv, S, B, box, T):
    ind = S.get('ind')
    res = S.get('res')
    st, sub = {}, {}
    for k in POS:
        if ind is not None:
            sub[k] = f'入度 {ind[k]}'
        if res is not None and k in res:
            st[k] = 'green'
        elif 'index' in S and S['index'] == k:
            st[k] = 'blue'
    hot = (S['x'], S['y']) if 'x' in S and 'index' not in S else None
    _gdraw(cv, box, T, POS, EDGES, st, sub, hot, '有向图（箭头指向的点入度 +1；绿 = 入度为 0 的起点）')


CONFIG = dict(
    num=1557, title='可以到达所有点的最少点数目', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='统计入度 · 选入度为 0 的点',
    tags=['灵神题单', '图论算法'],
    code='''
class Solution(object):
    def findSmallestSetOfVertices(self, n, edges):

        ind = [0] * n
        for x, y in edges:
            ind[y] += 1
        
        res = []
        for index in range(n):
            if ind[index] == 0:
                res.append(index)
        
        return res
''',
    call='Solution().findSmallestSetOfVertices(6, [[0,1],[0,2],[2,5],[3,4],[4,2]])',
    expect=[0, 3],
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='array', var='ind', label='ind（每个点的入度）', pointers={'index': 'blue'}, h=190,
             color=lambda S, i, v: 'green' if 'res' in S and v == 0 and 'index' in S and i <= S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('ind', 'ind', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ind = [0]': '`ind[v]` 记录==指向 v 的边数==，一开始都是 0',
        'for x, y in edges': lambda S, B, r: ('所有边都统计完了，入度数组 `ind` 算好' if B.get('x') == S.x and B.get('y') == S.y and 'ind' in B and B.ind == S.ind
                                              else f'取一条边 `{S.x} → {S.y}`'),
        'ind[y] += 1': '有边 `{x} → {y}`：`{y}` 能被别人到达 → `ind[{y}]` = =={ind[y]}==',
        'res = []': '`res` 用来存必须选的起点',
        'for index in range': lambda S, B, r: ('每个点都检查过了' if B.get('index') == S.index else f'检查点 `{S.index}`'),
        'if ind[index] == 0': lambda S, B, r: (f'`ind[{S.index}] = 0` → 没有任何点能走到它 → ==必须选它==' if S.ind[S.index] == 0
                                               else f'`ind[{S.index}] = {S.ind[S.index]}` ≥ 1 → 一定有别的点能到它，不用选'),
        'res.append': '选入口 `{index}`：`res` = {res}',
        'return res': '这 `{len(res)}` 个入度为 0 的点就是答案：`{res}`',
    },
    cards=dict(
        one_liner='入度为 0 的点谁也到不了它，只能自己当起点',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['有向无环图，`n` 个点、若干条边 `edges[i] = [from, to]`',
                 '选一个最小的点集，使得从这些点出发能走到所有点，返回点集',
                 '本视频：`n=6`，5 条边 → `[0, 3]`'],
        quote='只需要选出所有入度为0的点，就能保证可以从这些点出发到达所有点了。',
        quote_src='—— yiduobo 题解原文',
        idea=['入度为 0：==没有任何点指向它==，只能把它放进答案',
              '入度不为 0：必有另一个点能走到它，顺着往上找，最终会落到某个入度为 0 的点',
              '图无环，所以这条往上找的路一定会停在入度为 0 的点'],
        summary=['时间 `O(n + m)`：数一遍边，再扫一遍点',
                 '答案是==唯一==的最小集合：入度为 0 的点一个都不能少',
                 '前提是有向无环图；有环时要先缩点再数入度',
                 '原文本身是 Python 3 可运行的写法，代码未改动'],
    ),
)
