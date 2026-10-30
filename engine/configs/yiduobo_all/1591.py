GRID = [[1, 1, 1], [1, 2, 3]]
PAL = {1: 'blue', 2: 'pink', 3: 'yellow', 4: 'green'}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    m, n = len(GRID), len(GRID[0])
    line = S.get('_line', 0)
    cell = min(96, (x1 - x0 - 60) / n, (y1 - y0 - 80 - 36 * 3) / m)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    sy = y0 + 70
    # 正在分析的颜色及其外接矩形
    c = None
    if line >= 25 and S.get('color') is not None:
        c = S['color']
    elif line >= 13 and line <= 21 and S.get('now') is not None:
        c = S['now']
    L, R, Tp, Bt = (S.get(k, {}) for k in ('left', 'right', 'top', 'bottom'))
    head = '目标网格（每格的数字 = 颜色）'
    if c is not None and c in L and c in R and c in Tp and c in Bt:
        head = f'颜色 {c} 的范围：行 {Tp[c]}~{Bt[c]}，列 {L[c]}~{R[c]}'
    cv.text((x0 + 18, y0 + 4), head, 24, T['muted'], bold=True)
    for i in range(m):
        for j in range(n):
            v = GRID[i][j]
            X, Y = sx + j * cell, sy + i * cell
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T[PAL[v]], r=10, alpha=235)
            cv.text((X + cell / 2, Y + cell / 2), v, 36, T['bg'], anchor='mm', bold=True)
            cv.text((X + 8, Y + 6), f'{i},{j}', 14, T['bg'], anchor='la', mono=True)
    yt = sy + m * cell + 14
    for k, col in enumerate(sorted(L)):
        if col in R and col in Tp and col in Bt:
            yy = yt + k * 34
            cv.rect((x0 + 40, yy + 4, x0 + 64, yy + 28), fill=T[PAL[col]], r=6)
            cv.text((x0 + 76, yy + 16), f'颜色 {col}：行 {Tp[col]}~{Bt[col]}，列 {L[col]}~{R[col]}', 22,
                    T['text'] if col == c else T['muted'], anchor='lm', bold=(col == c))
    if c is not None and c in L and c in R and c in Tp and c in Bt:
        cv.rect((sx + L[c] * cell, sy + Tp[c] * cell, sx + (R[c] + 1) * cell, sy + (Bt[c] + 1) * cell),
                outline=T['text'], width=6, r=8)
    if 'i' in S and 'j' in S and 0 <= S['i'] < m and 0 <= S['j'] < n and line >= 11:
        X, Y = sx + S['j'] * cell, sy + S['i'] * cell
        cv.rect((X, Y, X + cell, Y + cell), outline=T['red'], width=5, r=10)


def _k(S):
    dec = 2 - sum(S['ind'].values())
    before = sum(len(S['g'].get(p, ())) for p in S['q'][:S['l'] - 1])
    return dec - before, list(S['g'].get(S['now'], ()))


def _edges(S):
    g = S.get('g')
    if not g:
        return '边 x → color（x 压在 color 的范围内）：暂无'
    return '边 x → color： ' + '，'.join(f'`{a} → {b}`' for a in g for b in sorted(g[a]))


CONFIG = dict(
    num=1591, title='奇怪的打印机 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='颜色范围建图 · 拓扑排序判环',
    tags=['灵神题单', '图论算法'],
    code='''
class Solution(object):
    def isPrintable(self, targetGrid):

        m = len(targetGrid)
        n = len(targetGrid[0])

        left = {}
        right = {}
        top = {}
        bottom = {}
        for i in range(m):
            for j in range(n):
                now = targetGrid[i][j]
                if left.get(now, n) > j:
                    left[now] = j
                if right.get(now, -1) < j:
                    right[now] = j
                if top.get(now, m) > i:
                    top[now] = i
                if bottom.get(now, -1) < i:
                    bottom[now] = i
        
        g = {}
        ind = {}
        for color in left:
            ind[color] = 0
            for i in range(top[color], bottom[color] + 1):
                for j in range(left[color], right[color] + 1):
                    if targetGrid[i][j] != color:
                        if targetGrid[i][j] not in g:
                            g[targetGrid[i][j]] = set()
                        g[targetGrid[i][j]].add(color)
        
        for color in g:
            for next in g[color]:
                ind[next] = ind.get(next, 0) + 1

        q = []
        for color in ind:
            if ind[color] == 0:
                q.append(color)
        
        l, r = 0, len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return len(q) == len(ind)
''',
    call='Solution().isPrintable([[1,1,1],[1,2,3]])',
    expect=True,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=lambda S: _edges(S), size=26, h=60),
        dict(type='map', var='ind', label='ind（有几种颜色压在它的范围里）', h=110),
        dict(type='array', var='q', label='q（拓扑序：从最上层往下剥）', pointers={'l': 'blue', 'r': 'pink'}, h=170),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink')],
    max_steps=100,
    skip=['m = len', 'n = len', 'left = {}', 'right = {}', 'top = {}', 'bottom = {}', 'g = {}', 'ind = {}', 'q = []',
          'if left.get', 'if right.get', 'if top.get', 'if bottom.get', 'if targetGrid[i][j] not in g',
          'now = targetGrid[i][j]', 'ind[color] = 0', 'l += 1', 'r += 1', 'for i in range(top[color]', 'for next in g[color]', 'for color in g:'],
    captions={
        'left[now] = j': '格子 `({i},{j})` 是颜色 `{now}`，它的最左列更新为 `{j}`：`left` = {left}',
        'right[now] = j': '格子 `({i},{j})` 是颜色 `{now}`，最右列更新为 `{j}`：`right` = {right}',
        'top[now] = i': '颜色 `{now}` 最上行更新为 `{i}`：`top` = {top}',
        'bottom[now] = i': '颜色 `{now}` 最下行更新为 `{i}`：`bottom` = {bottom}',
        'for color in left': lambda S, B, r: (f'分析颜色 `{S.color}`：它至少要涂满整个外接矩形' if B.get('color') != S.color or B.get('ind', {}).get(S.color) is None
                                              else '所有颜色都分析完了'),
        'for i in range(top[color]': lambda S, B, r: f'逐行扫描颜色 `{S.color}` 的矩形：行 `{S.top[S.color]} ~ {S.bottom[S.color]}`',
        'if targetGrid[i][j] != color': lambda S, B, r: (f'`({S.i},{S.j})` 是颜色 `{GRID[S.i][S.j]}` ≠ `{S.color}` → 它必须在 `{S.color}` ==之后==才涂上去' if GRID[S.i][S.j] != S.color
                                                       else f'`({S.i},{S.j})` 就是 `{S.color}`，没有约束'),
        'g[targetGrid[i][j]].add(color)': lambda S, B, r: f'连边 `{GRID[S.i][S.j]} → {S.color}`：`{GRID[S.i][S.j]}` 盖在 `{S.color}` 上面，==先剥它==',
        'for color in g': lambda S, B, r: f'统计入度：看颜色 `{S.color}` 压住了谁',
        'ind[next] = ind.get': '`{next}` 被 `{color}` 压住 → `ind[{next}]` = =={ind[next]}==',
        'for color in ind': lambda S, B, r: (f'检查颜色 `{S.color}`' if B.get('color') != S.color else '检查完所有颜色'),
        'if ind[color] == 0': lambda S, B, r: (f'`ind[{S.color}] = 0`：没有别的颜色压在它的范围里 → ==可以最先剥掉=='  if S.ind[S.color] == 0
                                               else f'`ind[{S.color}] = {S.ind[S.color]}`：还有颜色压着，不能先剥'),
        'q.append(color)': '`{color}` 入队：`q` = {q}',
        'l, r = 0, len(q)': '队列区间 `[l, r)`：`l = {l}`，`r = {r}`',
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`，继续剥' if S.l < S.r else f'`l = {S.l} = r`：队列空了'),
        'now = q[l]': '取队首颜色 `now = {now}`：把它剥掉（视为万用色），`l` 随后右移',
        'for next in g.get': lambda S, B, r_: (lambda kk, lst: (
            f'`{S.now}` 没有压住任何颜色，直接跳过' if not lst else
            '它压住的颜色都处理完了，回到 while' if kk >= len(lst) else
            f'`{S.now}` 被剥掉，看被它压住的 `{lst[kk]}`' if kk == 0 else f'再看被它压住的 `{lst[kk]}`'))(*_k(S)),
        'ind[next] -= 1': '`{next}` 上面少一层：`ind[{next}]` = =={ind[next]}==',
        'if ind[next] == 0': lambda S, B, r_: (f'`{S.next}` 上面已经没有别的颜色 → ==入队==' if S.ind[S.next] == 0 else f'`{S.next}` 上面还有 `{S.ind[S.next]}` 种颜色'),
        'q.append(next)': '`{next}` 入队：`q` = {q}，`r` 随后右移',
        'return len(q) == len(ind)': '`len(q) = {len(q)}`，颜色总数 `{len(ind)}`：全部剥完 → 无环 → ==能打印=={ret}',
    },
    cards=dict(
        one_liner='每种颜色只涂一次：谁盖在谁上面连成图，有环就不可能',
        complexity='时间 `O(C·m·n)`（C 为颜色数），空间 `O(C²)`',
        problem=['奇怪的打印机每次把一个矩形涂成同一种颜色，==每种颜色只能用一次==',
                 '给定目标网格 `targetGrid`，问能否打印出来',
                 '本视频：`[[1,1,1],[1,2,3]]` → `True`'],
        quote='确定数字范围指的是找出某个数字其最左、最右、最上、最下的出现的位置，那么在打印这个数字至少需要覆盖这整块区域。',
        quote_src='—— yiduobo 题解原文',
        idea=['先求每种颜色的最左、最右、最上、最下，得到它的外接矩形',
              '矩形里出现的别的颜色 x ==一定在它之后才涂==，连边 `x → color`',
              '拓扑排序：每次剥掉最上层的颜色；全部剥完 = 无环 = 能打印'],
        summary=['时间 `O(C·m·n)`：每种颜色扫一遍自己的外接矩形',
                 '有环 = 两种颜色互相要求对方在后涂 = 不可能打印',
                 '用「剥颜色」代替真的替换成万用色，只看先后关系',
                 '原文本身是 Python 3 可运行的写法，代码未改动',
                 '同类题：1591 是 664 奇怪的打印机（一维）的二维、每色一次版本'],
    ),
)
