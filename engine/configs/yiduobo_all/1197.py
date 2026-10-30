TX, TY = 3, 3


def _dists():
    d = {(0, 0): 0}
    fr = [(0, 0)]
    for k in range(1, 7):
        nf = []
        for a, b in fr:
            for da, db in ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)):
                p = (a + da, b + db)
                if p not in d:
                    d[p] = k
                    nf.append(p)
        fr = nf
    return d


DIST = _dists()


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    R = 4
    N = 2 * R + 1
    cv.text((x0 + 18, y0 + 4), '棋盘局部（横轴 y，纵轴 x；绿 = 已访问，黄 = 在队列里待展开，粉 = 终点）', 22, T['muted'], bold=True)
    cell = min(86, (y1 - y0 - 100) / N, (x1 - x0 - 40) / N)
    sx = x0 + ((x1 - x0) - cell * N) / 2
    sy = y0 + 56
    q = S.get('q')
    vis = S.get('vis', set())
    head = S.get('head', 0)
    pend = {tuple(p) for p in q[head:]} if q is not None and 'tail' in S else set()
    for i in range(N):
        for j in range(N):
            px, py = R - i, j - R
            X = sx + j * cell
            Y = sy + i * cell
            fill = T['panel2']
            lab = ''
            if (px, py) in vis:
                fill = T['yellow'] if (px, py) in pend and (px, py) != (0, 0) else T['green']
                lab = str(DIST.get((px, py), ''))
            if (px, py) == (TX, TY) and (px, py) not in vis:
                fill = T['pink']
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=8, outline=T['border'])
            if (px, py) == (0, 0):
                lab = '起'
            elif (px, py) == (TX, TY):
                lab = '终' if (px, py) not in vis else lab + '终'
            if lab:
                cv.text((X + cell / 2, Y + cell / 2), lab, 26, T['bg'], anchor='mm', bold=True)
    if 'nowx' in S and abs(S['nowx']) <= R and abs(S['nowy']) <= R:
        X, Y = sx + (S['nowy'] + R) * cell, sy + (R - S['nowx']) * cell
        cv.rect((X, Y, X + cell, Y + cell), outline=T['blue'], width=5, r=10)
    if 'nx' in S and S.get('_line') in (20, 21) and abs(S['nx']) <= R and abs(S['ny']) <= R:
        X, Y = sx + (S['ny'] + R) * cell, sy + (R - S['nx']) * cell
        cv.rect((X, Y, X + cell, Y + cell), outline=T['pink'], width=5, r=10)
    cv.text((sx + N * cell / 2, sy + N * cell + 14), f"已访问 {len(vis)} 个点，已搜 {S.get('res', 0)} 层（格内数字 = 最少步数）", 24, T['text'], anchor='mt', bold=True)


CONFIG = dict(
    num=1197, title='进击的骑士', difficulty='Medium', category='网格图',
    author='yiduobo', technique='暴力 BFS（数组当队列）',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def minKnightMoves(self, x, y):

        

        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [2, 1, -1, -2, -2, -1, 1, 2]

        q = [[0, 0]]
        vis = set()
        vis.add((0, 0))
        head, tail = 0, 1
        res = 0
        while (x, y) not in vis:
            res += 1
            for nowx, nowy in q[head : tail]:
                for index in range(8):
                    nx = nowx + dx[index]
                    ny = nowy + dy[index]
                    if -300 <= nx <= 300 and -300 <= ny <= 300 and (nx, ny) not in vis:
                        vis.add((nx, ny))
                        q.append([nx, ny])
            
            head, tail = tail, len(q)
        
        return res
''',
    call=f'Solution().minKnightMoves({TX}, {TY})',
    expect=2,
    skip=['dx = [', 'dy = [', 'nx = nowx', 'ny = nowy', 'for index in range(8)', 'q.append', 'head, tail = 0, 1'],
    max_steps=58,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('res', 'res', 'green'), 'head', 'tail', ('nowx', 'nowx', 'blue'), ('nowy', 'nowy', 'blue')],
    captions={
        'q = [[0, 0]]': '队列只放起点 `(0,0)`：棋盘无限，所以从起点向外一圈圈搜',
        'vis.add((0, 0))': '起点标为已访问，避免走回头路',
        'res = 0': '`res` 记录已经搜了几层 = 最少跳几步',
        'while (x, y) not in vis': lambda S, B, r: (f'终点 `({S.x},{S.y})` 还没被访问到 → 再搜一层' if (S.x, S.y) not in S.vis
                                                    else f'终点 `({S.x},{S.y})` 已被访问 → 停止，最少步数就是 `res = {S.res}`'),
        'res += 1': '开始搜新的一层：这一层的点都需要 `{res}` 步',
        'for nowx, nowy in q[head : tail]': '取出上一层的点 `({nowx},{nowy})`，它试 8 种跳法',
        'if -300 <= nx': lambda S, B, r: (f'`({S.nx},{S.ny})` 在 ±300 内且没访问过 → ==新点，入队=='
                                          if (-300 <= S.nx <= 300 and -300 <= S.ny <= 300 and (S.nx, S.ny) not in S.vis)
                                          else f'`({S.nx},{S.ny})` 已访问过（或越界）→ 跳过，BFS 先到的一定更短'),
        'vis.add((nx, ny))': '`({nx},{ny})` 第一次到达，一定是最短的：标记已访问并入队',
        'head, tail = tail, len(q)': '这一层搜完：`head` 移到新一层开头 `{head}`，`tail` = {tail}',
        'return res': '终点在第 `{res}` 层被访问到：最少 ==`{res}`== 步',
    },
    cards=dict(
        one_liner='棋盘无限？限制在 ±300 内，暴力 BFS 一层层往外扩',
        complexity='时间 `O(600 × 600)`（最坏），空间同阶',
        problem=['无限棋盘，骑士从 `(0,0)` 出发，按「日」字走（8 种跳法）',
                 '求跳到 `(x, y)` 最少要几步',
                 '本视频：`(3, 3)` → `2`（先 `(1,2)` 再 `(2,1)`）'],
        quote='目标点(x, y)的两维都被限制在300之内，因此即使不考虑任何优化，也只需在300 * 300大小的棋盘内做一次bfs，时间复杂度方面是完全没有问题的。',
        quote_src='—— yiduobo 题解原文',
        idea=['每步权重相同 → ==BFS 第一次碰到终点的层数就是最少步数==',
              '用数组 `q` 当队列，`q[head:tail]` 正好是「当前这一层」',
              '原文提到更优解：只有 4 种方向，枚举两个方向步数解方程；他偷懒用了暴力'],
        summary=['时间最坏 `O(600^2)`，空间同阶；`vis` 用集合防重复入队',
                 '`-300 <= nx <= 300` 是给无限棋盘划的边界，允许绕出 `x`、`y` 以外一点',
                 '入队时就标记 `vis`，而不是出队时，避免同一点重复入队',
                 '原文是 Python 2 风格的类，代码无需修改；小示例只展示前两层，真实输入可到 300'],
    ),
)
