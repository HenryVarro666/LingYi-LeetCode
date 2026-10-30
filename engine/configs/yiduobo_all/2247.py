N0 = 4
EDGES = [[0, 1, 4], [1, 2, 3], [1, 3, 6], [2, 3, 5]]
K0 = 2
POS = {0: (0.12, 0.45), 1: (0.4, 0.05), 2: (0.88, 0.45), 3: (0.4, 0.95)}


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = S['_inner']
    cv.text((x0 + 18, y0 + 4), '绿 = state 内城市，蓝 = last_pos，黄 = pre_pos', 20, T['muted'], bold=True)
    w, h = x1 - x0, y1 - y0
    P = {k: (x0 + 40 + (w - 80) * a, y0 + 50 + (h - 90) * b) for k, (a, b) in POS.items()}
    st, last, pre = I.get('state'), I.get('last_pos'), I.get('pre_pos')
    for x, y, v in EDGES:
        hot = last is not None and pre is not None and {x, y} == {last, pre} and S.get('_line') in (38, 39, 37)
        cv.line([P[x], P[y]], T['yellow'] if hot else T['border'], 6 if hot else 3)
        mx, my = (P[x][0] + P[y][0]) / 2, (P[x][1] + P[y][1]) / 2
        cv.rect((mx - 20, my - 16, mx + 20, my + 16), fill=T['bg'], r=8)
        cv.text((mx, my), v, 24, T['yellow'] if hot else T['text'], anchor='mm', bold=True)
    for k in range(N0):
        cx, cy = P[k]
        fill = T['panel2']
        if st is not None and st >> k & 1:
            fill = T['green']
        if k == last:
            fill = T['blue']
        if k == pre and S.get('_line') in (36, 37, 38, 39):
            fill = T['yellow']
        cv.rect((cx - 30, cy - 30, cx + 30, cy + 30), fill=fill, outline=T['border'], r=30)
        cv.text((cx, cy), k, 30, T['bg'] if fill != T['panel2'] else T['text'], anchor='mm', bold=True)


def _ft(S):
    f = S.get('f')
    if f is None:
        return [['·'] * N0 for _ in range(1 << N0)]
    return [['·' if v is None else v for v in row] for row in f]


def _col(S, r, c, v):
    I = S['_inner']
    if 'state' in I and 'last_pos' in I and r == I['state'] and c == I['last_pos']:
        return 'yellow'
    if 'pre_state' in I and I.get('pre_pos') is not None and S.get('_line') in (37, 38, 39) and r == I['pre_state'] and c == I['pre_pos']:
        return 'blue'
    return None


def _cand(S):
    c = S.get('candidate')
    if not c:
        return '`candidate`：恰好包含 k+1 个城市的所有 state'
    return '`candidate` = ' + '、'.join(format(x, f'0{N0}b') for x in c)


CONFIG = dict(
    num=2247, title='K条高速公路的最大旅行费用', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 路径经过的城市集合',
    tags=['状压 DP'],
    code='''
class Solution(object):
    def maximumCost(self, n, highways, k):

        if k + 1 > n:
            return -1

        g = {index : {} for index in range(n)}
        for x, y, v in highways:
            g[x][y] = g[y][x] = v

        candidate = []
        def dfs(level, now, cnt):
            if cnt == k + 1:
                candidate.append(now)
                return
            
            if level == n:
                return

            dfs(level + 1, now, cnt)
            dfs(level + 1, now | (1 << level), cnt + 1)

        dfs(0, 0, 0)

        max_state = 1 << n
        f = [[None] * n for _ in range(max_state)]
        for index in range(n):
            f[1 << index][index] = 0
        res = -1

        def calc(state, last_pos):
            if f[state][last_pos] is None:
                f[state][last_pos] = -1
                pre_state = state ^ (1 << last_pos)
                for pre_pos in g[last_pos]:
                    if pre_state & (1 << pre_pos) == (1 << pre_pos):
                        pre_dis = calc(pre_state, pre_pos)
                        if pre_dis != -1:
                            f[state][last_pos] = max(f[state][last_pos], pre_dis + g[last_pos][pre_pos])

            return f[state][last_pos]

        for state in candidate:
            for last_pos in range(n):
                if state & (1 << last_pos) == (1 << last_pos):
                    res = max(res, calc(state, last_pos))

        return res
''',
    call=f'Solution().maximumCost({N0}, {EDGES}, {K0})',
    expect=11,
    skip=[8, 9, 12, 13, 14, 15, 17, 18, 20, 21, 25, 27, 28, 41, 44],
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='text', fn=_cand, size=22, h=54),
        dict(type='table', var=_ft, label='f：行 = 城市集合（最低位是城市 0），列 = 停在哪', h=420, cell=56,
             rows=lambda S: [format(x, f'0{N0}b') for x in range(1 << N0)], cols=lambda S: [str(x) for x in range(N0)], color=_col),
        dict(type='calls', h=90, hide=('highways',)),
    ],
    watch=[('state', lambda S: format(S['_inner']['state'], f'0{N0}b') if 'state' in S['_inner'] else '', 'cyan'),
           ('last_pos', lambda S: S['_inner'].get('last_pos'), 'blue'), ('pre_pos', lambda S: S['_inner'].get('pre_pos'), 'yellow'),
           ('res', lambda S: S.get('res'), 'green')],
    captions={
        'if k + 1 > n': '走 `k` 条路要经过 `k+1` 个不同城市：`k + 1 = {k + 1}`，`n = {n}` → ' + '城市够，继续',
        'g = {index': '先建邻接表：`g[x][y] = 过路费`',
        'candidate = []': '`g` 建好了：`{g}`',
        'dfs(0, 0, 0)': '先 dfs 枚举「恰好选 k+1 个城市」的所有集合，得到 `candidate`：路径只可能经过这些集合',
        'f = [[None]': '`f[state][last]`：已到过 state 里的城市、停在 last 的最大费用；`None` 表示还没算',
        'f[1 << index][index] = 0': '起点：只在城市 `{index}` 一个城市，费用 0',
        'res = -1': '`res = -1`：找不到合法路径就返回 -1',
        'if f[state][last_pos] is None': lambda S, B, r: ('这个状态还没算 → 开始计算' if S.f[S.state][S.last_pos] is None else '已经算过 → 直接用'),
        'f[state][last_pos] = -1': '先记成 -1，表示「暂时没有合法路径」',
        'pre_state = state ^': lambda S, B, r: f'去掉停留的城市 `{S.last_pos}`：`pre_state = {S.pre_state:0{N0}b}`，路径的上一段在这个集合里',
        'for pre_pos in g[last_pos]': lambda S, B, r: f'枚举和城市 {S.last_pos} 相邻的城市 `pre_pos = {S.pre_pos}`',
        'if pre_state & (1 << pre_pos)': lambda S, B, r: (f'城市 {S.pre_pos} 在 `pre_state` 里 → 可以从它走过来' if S.pre_state >> S.pre_pos & 1 else f'城市 {S.pre_pos} 不在 `pre_state` 里 → 没到过，跳过'),
        'pre_dis = calc': '先求出「停在 `{B.pre_pos}`、到过 `pre_state`」的最大费用',
        'if pre_dis != -1': lambda S, B, r: ('`pre_dis = -1`：那个状态无合法路径 → 不用' if S.pre_dis == -1 else f'`pre_dis = {S.pre_dis}`：有合法路径'),
        'f[state][last_pos] = max': lambda S, B, r: f'`f[{S.state:0{N0}b}][{S.last_pos}] = max(旧值, {S.pre_dis} + 过路费 {S.g[S.last_pos][S.pre_pos]})`',
        'for state in candidate': lambda S, B, r: (f'`state = {S.state:0{N0}b}`：对每个候选集合，枚举停在哪个城市' if S.get('state') is not None else '候选都试完了'),
        'if state & (1 << last_pos)': lambda S, B, r: (f'城市 {S.last_pos} 在集合里 → 可以作为终点' if S.state >> S.last_pos & 1 else f'城市 {S.last_pos} 不在集合里 → 跳过'),
        'res = max(res, calc': '用 `f[state][last_pos]` 更新答案：`res` 先取 `max(旧 res, f)`',
        'return f[state][last_pos]': '这个状态的最大费用 `{f[state][last_pos]}`',
        'return res': '最大旅行费用 `{ret}`',
    },
    max_steps=66,
    cards=dict(
        one_liner='k 条路 = k+1 个不同城市：状态记「到过哪些城市、停在哪」',
        complexity='时间 `O(2^n · n^2)`，空间 `O(2^n · n)`',
        problem=['`n` 个城市，`highways[i] = [a, b, toll]` 是双向高速公路',
                 '恰好走 `k` 条路、每个城市最多访问一次，求最大总过路费；不可能则返回 `-1`',
                 '本视频：`n=4`，边 `[0,1,4] [1,2,3] [1,3,6] [2,3,5]`，`k=2` → `11`',
                 '（题面库里没有，题意按 LeetCode 2247 补写）'],
        quote='经过K条告诉公路意味着经过K + 1个城市，若这里的K + 1 > n，那么必然无解，直接返回-1即可。……本题的数据规模较小，可以使用状态压缩动态规划来求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[state][last]`：已到过 state 里的城市，最后停在 last 的最大费用',
              '去掉 last 得 `pre_state`，枚举相邻的 `pre_pos`：`f[pre_state][pre_pos] + toll`',
              '先 dfs 找出所有恰好 k+1 个城市的集合，再对这些集合、每个终点取最大值'],
        summary=['时间 `O(2^n n^2)`，空间 `O(2^n n)`',
                 '`k + 1 > n` 直接返回 -1；`f` 为 -1 表示该状态没有合法路径，不能参与转移',
                 '起点 `f[1<<i][i] = 0`：任何城市都可以作为出发点',
                 '原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
