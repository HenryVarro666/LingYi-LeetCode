H = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
CHECK = (26, 27, 28, 29, 31)   # BFS 跑完之后的几行：此时 used 是本轮 mid 能走到的格子


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    h = H
    m, n = len(h), len(h[0])
    mid = S.get('mid')
    line = S.get('_line')
    fresh = line in CHECK and 'used' in S
    used = S.get('used') if fresh else None
    cv.text((x0 + 18, y0 + 4), '格子里是高度，格子之间是高度差（绿 = ≤ mid 可走，红 = 走不了）', 22, T['muted'], bold=True)
    c, g = 104, 74
    W = n * c + (n - 1) * g
    sx = x0 + (x1 - x0 - W) / 2
    sy = y0 + 56
    def xy(i, j):
        return sx + j * (c + g), sy + i * (c + g)
    # 边
    for i in range(m):
        for j in range(n):
            for di, dj in ((0, 1), (1, 0)):
                a, b = i + di, j + dj
                if a >= m or b >= n:
                    continue
                d = abs(h[a][b] - h[i][j])
                X, Y = xy(i, j)
                if dj:
                    p0, p1 = (X + c, Y + c / 2), (X + c + g, Y + c / 2)
                else:
                    p0, p1 = (X + c / 2, Y + c), (X + c / 2, Y + c + g)
                if mid is None:
                    col, ok = T['muted'], True
                else:
                    ok = d <= mid
                    col = T['green'] if ok else T['red']
                if ok:
                    cv.line([p0, p1], col, 4)
                else:
                    cv.dashed(p0, p1, col, 3, 8, 7)
                mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
                cv.rect((mx - 18, my - 16, mx + 18, my + 16), fill=T['bg'], r=8, outline=col, width=2)
                cv.text((mx, my), d, 22, col, anchor='mm', bold=True, mono=True)
    for i in range(m):
        for j in range(n):
            X, Y = xy(i, j)
            on = used is not None and (i, j) in used
            fill = T['green'] if on else T['panel2']
            cv.rect((X, Y, X + c, Y + c), fill=fill, r=12, outline=T['border'], width=2)
            cv.text((X + c / 2, Y + c / 2), h[i][j], 36, T['bg'] if on else T['text'], anchor='mm', bold=True)
    X, Y = xy(0, 0)
    cv.text((X - 10, Y + c / 2), '起点', 22, T['blue'], anchor='rm', bold=True)
    X, Y = xy(m - 1, n - 1)
    cv.text((X + c + 10, Y + c / 2), '终点', 22, T['pink'], anchor='lm', bold=True)


def _text(S):
    if 'mid' not in S:
        if 'r' in S:
            return f"二分答案：区间 `[l, r] = [{S['l']}, {S['r']}]`"
        return '答案 = 路径上相邻高度差的==最大值==，要让它最小'
    s = f"区间 `[{S['l']}, {S['r']}]`，`mid = {S['mid']}`"
    if S.get('_line') in CHECK and 'used' in S:
        s += f"：BFS 走到 `{len(S['used'])}` 格" + ('，==到得了终点==' if (2, 2) in S['used'] else '，==到不了终点==')
    return s


def _check(S, B, r):
    if (S.m - 1, S.n - 1) in S.used:
        return f'`mid = {S.mid}`：只走高度差 ≤ {S.mid} 的边，BFS ==能到终点== → 答案 ≤ {S.mid}'
    return f'`mid = {S.mid}`：只走高度差 ≤ {S.mid} 的边，BFS 只到了 `{len(S.used)}` 格，==到不了终点=='


CONFIG = dict(
    num=1631, title='最小体力消耗路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='二分答案 + BFS',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def minimumEffortPath(self, heights):
        l = 0
        r = 1000000
        m = len(heights)
        n = len(heights[0])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            mid = (l + r) >> 1
            q = [(0, 0)]
            used = set([(0, 0)])
            head = 0
            tail = 1
            while head < tail:
                nowx, nowy = q[head]
                head += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and abs(heights[x][y] - heights[nowx][nowy]) <= mid and (x, y) not in used:
                        q.append((x, y))
                        used.add((x, y))
                        tail += 1

            if (m - 1, n - 1) in used:
                r = mid
            else:
                l = mid + 1

        return l
''',
    call=f'Solution().minimumEffortPath({H})',
    expect=2,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'while l < r', 'q = [(0, 0)]', 'used = set', 'head = 0',
          'tail = 1', 'while head < tail', 'nowx, nowy = q[head]', 'head += 1', 'for index in range(4)',
          'x = nowx', 'y = nowy', 'if x >= 0', 'q.append', 'used.add', 'tail += 1'],
    max_steps=28,
    views=[
        dict(type='text', fn=_text, h=60, size=24),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'),
           ('能走到的格数', lambda S: len(S['used']) if S.get('_line') in CHECK and 'used' in S else None, 'green')],
    captions={
        'l = 0': '二分答案：最小体力消耗不会小于 `0`',
        'r = 1000000': '高度 ≤ 10^6，所以答案 ≤ `{r}`，二分区间 `[0, {r}]`',
        'mid = (l + r) >> 1': '试一试 `mid = ({l} + {r}) >> 1 = {mid}`：只允许走高度差 ≤ `{mid}` 的边，从起点 BFS',
        'if (m - 1, n - 1) in used': _check,
        'r = mid': '能到 → 答案 ≤ `{mid}`，`r = {r}`，==看看更小的行不行==',
        'l = mid + 1': '到不了 → 答案 > `{B.mid}`，`l = {l}`',
        'return l': '`l == r`：最小的可行值就是答案 =={ret}==',
    },
    cards=dict(
        one_liner='体力值越大能走的边越多：二分体力值，用 BFS 判断能否走到终点',
        complexity='时间 `O(mn log C)`，`C = 10^6`；空间 `O(mn)`',
        problem=['`heights` 是 `m × n` 的高度网格，从左上角走到右下角，每步上下左右',
                 '路径的体力消耗 = 路径上==相邻格子高度差的最大值==，求最小体力消耗',
                 '示例：`[[1,2,2],[3,8,2],[5,3,5]]` → `2`（路径 1→3→5→3→5）'],
        quote='当最小体力消耗越大时，每个点能走的相邻点就越多……一个自然的想法就是==直接二分答案==，然后从起点开始进行bfs，并根据能否走到终点来调整二分的边界。',
        quote_src='—— yiduobo 题解原文',
        idea=['单调性：`mid` 能到终点，比 `mid` 大的也一定能到',
              '固定 `mid`：只走高度差 ≤ `mid` 的边，BFS 看终点在不在 `used` 里',
              '能到就 `r = mid`，到不了就 `l = mid + 1`，找最小可行值'],
        summary=['时间 `O(mn log C)`：二分约 20 轮，每轮一次 BFS',
                 '本视频跳过了 BFS 内部的逐行执行，只展示每轮==能走到的格子=='
                 ,
                 '`r = mid` 而不是 `mid - 1`：mid 本身可能就是答案',
                 '原文也提到可以用 Dijkstra（边权取高度差，路径代价取最大值），复杂度略好',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
