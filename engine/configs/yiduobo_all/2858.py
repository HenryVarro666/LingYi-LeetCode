# 示例 1：n=4, edges=[[2,0],[2,1],[1,3]] -> [1,1,0,2]
POS_ = {2: (0.5, 0.14), 0: (0.2, 0.50), 1: (0.8, 0.50), 3: (0.8, 0.88)}
ORIG_ = [(2, 0), (2, 1), (1, 3)]

CODE = '''
class Solution(object):
    def minEdgeReversals(self, n, edges):

        g = {i : {} for i in range(n)}
        for x, y in edges:
            g[x][y] = 1
            g[y][x] = -1
        
        vis = set([0])
        q = [0]
        head, tail = 0, 1
        res = [0] * n
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(nxt)
                    tail += 1
                    if g[now][nxt] == -1:
                        res[0] += 1
        
        vis = set([0])
        q = [0]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    q.append(nxt)
                    tail += 1
                    res[nxt] = res[now]
                    if g[now][nxt] == 1:
                        res[nxt] += 1
                    else:
                        res[nxt] -= 1
        
        return res
'''
PH2 = [i for i, l in enumerate(CODE.split('\n'), 1) if 'vis = set([0])' in l][1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    W, H = x1 - x0 - 160, y1 - y0 - 110
    P = {k: (x0 + 80 + v[0] * W, y0 + 55 + v[1] * H) for k, v in POS_.items()}
    cx, cy = S.get('now'), S.get('nxt')
    ph2 = S.get('_line', 0) >= PH2
    vis = S.get('vis') or set()
    cv.text((x0 + 18, y0 + 4), '有向边（箭头方向）；黄框 = now，粉框 = nxt', 22, T['muted'], bold=True)
    for a, b in ORIG_:
        hot = (cx, cy) in ((a, b), (b, a))
        col = T['dim'] if not hot else (T['green'] if (cx, cy) == (a, b) else T['pink'])
        (ax, ay), (bx, by) = P[a], P[b]
        d = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        ux, uy = (bx - ax) / d, (by - ay) / d
        cv.arrow((ax + ux * 36, ay + uy * 36), (bx - ux * 36, by - uy * 36), col, 7 if hot else 4, 16)
        if hot:
            s = '+1' if (cx, cy) == (a, b) else '−1'
            mx, my = (ax + bx) / 2, (ay + by) / 2
            cv.text((mx + (30 if bx >= ax else -30), my), 'g[now][nxt]=' + s, 24, col, anchor='lm' if bx >= ax else 'rm', bold=True)
    res = S.get('res')
    for k, (px, py) in P.items():
        seen = k in vis
        cv.rect((px - 28, py - 28, px + 28, py + 28), fill=T['panel2'], outline=T['green'] if seen else T['blue'], width=4 if seen else 3, r=28)
        if k == cx:
            cv.rect((px - 36, py - 36, px + 36, py + 36), outline=T['yellow'], width=5, r=36)
        if k == cy:
            cv.rect((px - 36, py - 36, px + 36, py + 36), outline=T['pink'], width=5, r=36)
        cv.text((px, py), k, 30, T['text'], anchor='mm', bold=True)
        if ph2 and res is not None and seen:
            lf = k == 0
            cv.text((px - 44 if lf else px + 44, py - 4), 'res=%d' % res[k], 26, T['orange'], anchor='rm' if lf else 'lm', bold=True, mono=True)
    if not ph2 and res is not None:
        cv.text((x0 + 18, y1 - 40), f'第一遍 BFS：从 0 出发要反转的边数 res[0] = {res[0]}', 28, T['orange'], bold=True)
    else:
        cv.text((x0 + 18, y1 - 40), '绿框 = 已入队（vis）', 24, T['green'], bold=True)


def c_cnt(S, B, ret):
    d = S.g[S.now][S.nxt]
    if d == -1:
        return f'`g[{S.now}][{S.nxt}] = -1`：原边是 `{S.nxt}→{S.now}`，从 0 往下走要==反转== → `res[0]` = =={S.res[0]}=='
    return f'`g[{S.now}][{S.nxt}] = 1`：原边就是 `{S.now}→{S.nxt}`，==无需反转==，`res[0]` 不变'


def c_up(S, B, ret):
    return f'`g[{S.now}][{S.nxt}] = 1`：原边是 `{S.now}→{S.nxt}`；从 {S.nxt} 出发这条边反了 → `res[{S.nxt}]` 加 1 = =={S.res[S.nxt]}=='


def c_dn(S, B, ret):
    return f'`g[{S.now}][{S.nxt}] = -1`：原边是 `{S.nxt}→{S.now}`；从 {S.now} 出发它要反转，从 {S.nxt} 出发不用 → `res[{S.nxt}]` 减 1 = =={S.res[S.nxt]}=='


CONFIG = dict(
    num=2858, title='可以到达每一个节点的最少边反转次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='换根 DP · 两遍 BFS',
    tags=['灵神题单', '动态规划', '难度分 2295'],
    code=CODE,
    call='Solution().minEdgeReversals(4, [[2,0],[2,1],[1,3]])',
    expect=[1, 1, 0, 2],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='array', var='q', label='q', pointers={'head': 'blue'}, h=110),
        dict(type='array', var='res', label='res', h=110),
    ],
    watch=['now', 'nxt', 'head', 'tail'],
    skip=['g = {i', 'g[x][y] = 1', 'g[y][x] = -1', 'for x, y in edges', 'tail += 1', 'q = [0]', 'vis = set', 'head += 1', 'while head < tail'],
    captions={
        'res[0] += 1': c_cnt,
        'if g[now][nxt] == -1': lambda S, B, r: (f'`g[{S.now}][{S.nxt}]` = {S.g[S.now][S.nxt]}：' + ('是 −1，这条边要反转' if S.g[S.now][S.nxt] == -1 else '不是 −1，顺着走，不用反转')),
        'res[nxt] = res[now]': '`{nxt}` 和 `{now}` 相邻：除了这条边，到其余点的反转数完全相同，先继承 `res[{now}]` = =={res[nxt]}=='.replace('=={res[nxt]}==', '=={res[now]}=='),
        'res[nxt] += 1': c_up,
        'res[nxt] -= 1': c_dn,
        'nxt not in vis': lambda S, B, r: (f'`{S.nxt}` 还没访问过 → 是 `{S.now}` 的孩子，==入队==' if S.nxt not in B.vis else f'`{S.nxt}` 已访问过 → 它是 `{S.now}` 的父亲，==不回头==，跳过'),
        'now = q[head]': '队首出队：`now = q[{B.head}]` = =={now}==，从它向外扩',
    },
    cards=dict(
        one_liner='相邻两点的答案，只差中间那条边的方向',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个点的有向图，忽略方向后是一棵树；反转一条边 = 改变它的方向',
                 '对每个点，求从它出发到达所有点最少要反转几条边',
                 '示例：`edges=[[2,0],[2,1],[1,3]]` → `[1,1,0,2]`'],
        quote='若这条边是从x出发到y的边，那么从x出发时这条边无需反转，但是从y出发时这条边需要反转，因此res[y] = res[x] + 1；反之则 res[y] = res[x] - 1。',
        quote_src='—— yiduobo 题解',
        idea=['树上两点只有一条路，路上的反向边必须反转，不能绕路',
              '把相邻的 x、y 看成一个整体：到其余点的反转数相同，只差 x-y 这条边',
              '第一遍 BFS 求 `res[0]`；第二遍 BFS 用 `res[y] = res[x] ± 1` 一层层扩出去'],
        summary=['时间 `O(n)`，空间 `O(n)`；两遍 BFS 都不用递归，不怕栈溢出',
                 '易错：字典里 `g[x][y]=1`（原方向）、`g[y][x]=-1`（逆方向），符号别搞反',
                 '第二遍要重置 `vis` 和队列，`res[0]` 保持第一遍的结果',
                 '题解的 `head/tail` 是手写队列指针，`tail` 记录入队个数'],
    ),
)
