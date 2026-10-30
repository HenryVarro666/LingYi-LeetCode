import math as _m


def _tgraph(cv, T, box, pos, edges, ncol, nsub, ecol, title, R=30, bottom=62, side=None):
    """通用树/图：pos 为 0..1 的相对坐标；nsub 返回 str 或 [str]（画在节点下方）"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    L, Rr, Tp, Bt = x0 + 80, x1 - 80, y0 + 52 + R + (50 if 'a' in (side or {}).values() else 0), y1 - R - bottom
    P = {u: (L + fx * (Rr - L), Tp + fy * (Bt - Tp)) for u, (fx, fy) in pos.items()}
    for u, v in edges:
        c, wd = ecol(u, v)
        cv.line([P[u], P[v]], c, wd)
    for u, (px, py) in P.items():
        fc = ncol(u)
        cv.d.ellipse((px - R, py - R, px + R, py + R), fill=fc, outline=T['border'], width=2)
        cv.text((px, py), u, 28, T['bg'] if fc != T['panel2'] else T['text'], anchor='mm', bold=True)
        s = nsub(u)
        if s is None:
            continue
        sd = (side or {}).get(u, 'b')
        for k, line in enumerate([s] if isinstance(s, str) else s):
            if sd == 'b':
                cv.text((px, py + R + 4 + k * 23), line, 20, T['yellow'], anchor='mt', bold=True, mono=True)
            elif sd == 'a':
                cv.text((px, py - R - 4 - (len(s) - 1 - k) * 23 if not isinstance(s, str) else py - R - 4), line, 20, T['yellow'], anchor='mb', bold=True, mono=True)
            elif sd == 'r':
                cv.text((px + R + 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='lm', bold=True, mono=True)
            else:
                cv.text((px - R - 8, py - R - 4 + k * 23), line, 20, T['yellow'], anchor='rm', bold=True, mono=True)
EDGES = [(0, 1), (0, 2)]
POS = {0: (0.5, 0.0), 1: (0.15, 1.0), 2: (0.85, 1.0)}
SIDE = {0: 'r', 1: 'b', 2: 'b'}
CW, CH = 64, 38


def _val(x):
    return '·' if x is None else str(x)


def _grid(cv, T, x, y, title, name, S, B, now, rows, K):
    cv.text((x, y), title, 22, T['muted'], bold=True)
    cur, old = S.get(name), B.get(name)
    ly = y + 50
    for j in range(K + 1):
        cv.text((x + 56 + j * CW + CW / 2, ly), f'd={j}', 18, T['muted'], anchor='mm', mono=True)
    for i in range(rows):
        Y = ly + 16 + i * CH
        cv.text((x + 46, Y + CH / 2), f'{i}', 22, T['blue'] if i == now else T['muted'], anchor='rm', bold=True)
        for j in range(K + 1):
            v = cur[i][j] if cur else None
            ov = old[i][j] if old else None
            X = x + 56 + j * CW
            ch = cur is not None and v != ov
            cv.rect((X + 2, Y + 2, X + CW - 2, Y + CH - 2), fill=T['panel2'], r=6,
                    outline=T['yellow'] if ch else (T['blue'] if i == now else T['border']), width=3 if ch else (2 if i == now else 1))
            cv.text((X + CW / 2, Y + CH / 2), _val(v), 22, T['text'] if v is not None else T['dim'], anchor='mm', bold=True)


def _draw_a(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inn = S['_inner']
    now, nxt = inn.get('now'), inn.get('nxt')
    f, nums, K = S.get('f'), S.get('nums'), S.get('k')
    w = x1 - x0
    isdfs = 'sf' in inn

    def done(u):
        return f is not None and all(v is not None for v in f[u])

    def ncol(u):
        if u == now and isdfs:
            return T['blue']
        if u == nxt and isdfs and nxt != inn.get('pre'):
            return T['yellow']
        return T['green'] if done(u) else T['panel2']

    def nsub(u):
        return f'值 {nums[u]}'

    def ecol(u, v):
        if isdfs and nxt is not None and {u, v} == {now, nxt}:
            return T['yellow'], 6
        return T['border'], 3

    _tgraph(cv, T, (x0, y0, x0 + w * 0.46, y1), POS, EDGES, ncol, nsub, ecol,
            '蓝 now · 黄 孩子 · 绿 已算完', side=SIDE, bottom=50)
    lx = x0 + w * 0.5
    cv.text((lx, y0 + 4), f'now={now} 的局部数组（对孩子累加）', 22, T['muted'], bold=True)
    for j in range(K + 1):
        cv.text((lx + 66 + j * CW + CW / 2, y0 + 52), f'd={j}', 18, T['muted'], anchor='mm', mono=True)
    for r, name in enumerate(['sf', 'ma_f', 'sg', 'mi_g']):
        arr = inn.get(name) if isdfs else None
        Y = y0 + 66 + r * CH
        cv.text((lx + 56, Y + CH / 2), name, 22, T['cyan'], anchor='rm', bold=True, mono=True)
        oldarr = B['_inner'].get(name) if isdfs and 'sf' in B['_inner'] else None
        for j in range(K + 1):
            v = arr[j] if arr else None
            ov = oldarr[j] if oldarr else None
            X = lx + 66 + j * CW
            ch = arr is not None and v != ov
            cv.rect((X + 2, Y + 2, X + CW - 2, Y + CH - 2), fill=T['panel2'], r=6,
                    outline=T['yellow'] if ch else T['border'], width=3 if ch else 1)
            cv.text((X + CW / 2, Y + CH / 2), _val(v), 22, T['text'] if v is not None else T['dim'], anchor='mm', bold=True)


def _draw_b(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    inn = S['_inner']
    now = inn.get('now') if 'sf' in inn else None
    n, K = len(S['nums']), S['k']
    w = x1 - x0
    _grid(cv, T, x0 + 18, y0 + 4, 'f[v][d]：最大值（行 = 节点 v）', 'f', S, B, now, n, K)
    _grid(cv, T, x0 + w * 0.5, y0 + 4, 'g[v][d]：最小值', 'g', S, B, now, n, K)


def _txt(S):
    inn = S['_inner']
    if 'sf' not in inn:
        return '`f[v][d]`：v 子树里「离 v 最近的反转点距离 ≥ d」时的最大和；`d=0` 表示反转了 v 自己'
    now, K = inn['now'], S['k']
    return f'`f[{now}][d]` / `g[{now}][d]`：按 `d` 与 `k={K}` 的关系分三种情况（`d=0`、`d+d>=k`、`d+d<k`）'


CONFIG = dict(
    num=3949, title='子树反转和II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='树形 DP · f 取大 g 取小',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def subtreeInversionSum(self, edges, nums, k):
        
        n = len(nums)

        f = [[None] * (k + 1) for _ in range(n)]
        g = [[None] * (k + 1) for _ in range(n)]

        t = [[] for _ in range(n)]
        for x, y in edges:
            t[x].append(y)
            t[y].append(x)
        
        def dfs(now, pre, f, g):
            sf = [0] * (k + 1)
            ma_f = [None] * (k + 1)
            sg = [0] * (k + 1)
            mi_g = [None] * (k + 1)

            for nxt in t[now]:
                if nxt == pre:
                    continue
                
                dfs(nxt, now, f, g)
                
                for d in range(k + 1):
                    sf[d] += f[nxt][d]
                    sg[d] += g[nxt][d]
                    if d != 0 and d + d < k:
                        if ma_f[d] is None or f[nxt][d - 1] - f[nxt][k - d - 1] > ma_f[d]:
                            ma_f[d] = f[nxt][d - 1] - f[nxt][k - d - 1]
                        if mi_g[d] is None or g[nxt][d - 1] - g[nxt][k - d - 1] < mi_g[d]:
                            mi_g[d] = g[nxt][d - 1] - g[nxt][k - d - 1]

            for d in range(1, k + 1):
                if d + d >= k:
                    f[now][d] = sf[d - 1] + nums[now]
                    g[now][d] = sg[d - 1] + nums[now]
                else:
                    if ma_f[d] is not None:
                        f[now][d] = sf[k - d - 1] + ma_f[d] + nums[now]
                    if mi_g[d] is not None:
                        g[now][d] = sg[k - d - 1] + mi_g[d] + nums[now]

            f[now][0] = -sg[k - 1] - nums[now]
            g[now][0] = -sf[k - 1] - nums[now]

            for d in range(k - 1, -1, -1):
                if f[now][d] is None or f[now][d] < f[now][d + 1]:
                    f[now][d] = f[now][d + 1]
                if g[now][d] is None or g[now][d] > g[now][d + 1]:
                    g[now][d] = g[now][d + 1]

        dfs(0, -1, f, g)
        return f[0][0]
''',
    call='Solution().subtreeInversionSum([[0,1],[0,2]], [3,-5,-4], 3)',
    expect=6,
    views=[
        dict(type='custom', draw=_draw_a, h=250),
        dict(type='custom', draw=_draw_b, h=215),
        dict(type='text', fn=_txt, size=24, h=60),
    ],
    watch=[('now', lambda S: S['_inner'].get('now') if 'sf' in S['_inner'] else None, 'blue'),
           ('nxt', lambda S: S['_inner'].get('nxt') if 'sf' in S['_inner'] else None, 'yellow'),
           ('d', lambda S: S['_inner'].get('d') if 'sf' in S['_inner'] else None, 'cyan'), ('k', 'k', 'purple')],
    skip=['n = len(nums)', 't = [[]', 'for x, y in edges', 't[x].append', 't[y].append',
          'ma_f = [None]', 'sg = [0]', 'mi_g = [None]', 'for nxt in t[now]', 'if nxt == pre', 'continue',
          'for d in range', 'sg[d] += g', 'if d != 0 and d + d < k',
          'if mi_g[d] is None', 'mi_g[d] = g', 'if ma_f[d] is not None', 'if mi_g[d] is not None',
          'g[now][d] = sg[', 'g[now][0] =', 'if g[now][d] is None', 'g[now][d] = g[now][d + 1]',
          'if d + d >= k', 'if f[now][d] is None'],
    max_steps=75,
    captions={
        'f = [[None]': ('`f[v][d]`：以 v 为根的子树里，==离 v 最近的反转点距离 ≥ d== 时，节点值之和的最大值；'
                        '`d = 0` 表示反转了 v 自己。先全填空'),
        'g = [[None]': '`g` 同理，记最小值：反转 v 时孩子要取最小，所以 f、g 要成对维护',
        'dfs(0, -1, f, g)': '从根 0 开始递归：先算孩子，再算自己',
        'sf = [0]': lambda S, B, r: (f"进入节点 `{S['_inner']['now']}`：`sf[d]` = 孩子们 `f[·][d]` 之和，`sg` 同理；"
                                      '`ma_f[d]` / `mi_g[d]` 记「挑一个特殊孩子」的最优增量'),
        'dfs(nxt, now, f, g)': '先递归孩子 `{B.nxt}`，等它的 `f / g` 算完',
        'sf[d] += f[nxt][d]': '孩子 `{nxt}`：`sf[{d}] += f[{nxt}][{d}] = {f[nxt][d]}` → `sf[{d}] = {sf[d]}`（`sg` 同理）',
        'if ma_f[d] is None or': ('`{d}+{d} < k={k}`：这个孩子可当「特殊孩子」，增量 `f[{nxt}][{d-1}] − f[{nxt}][{k-d-1}]` '
                                  '= `{f[nxt][d-1]} − {f[nxt][k-d-1]}` = =={f[nxt][d-1] - f[nxt][k-d-1]}==，和已有最优比较'),
        'ma_f[d] = f[nxt]': '`ma_f[{d}]` 更新为 =={ma_f[d]}==：特殊孩子取 `d-1`，其余孩子取 `k-d-1`',
        'f[now][d] = sf[d - 1]': ('`d={d}`，`d+d >= k`：两个孩子里的反转点必然离得够远，直接累加。`f[{now}][{d}] = sf[{d-1}] + nums[{now}]` = `{sf[d-1]} + {nums[now]}` = =={f[now][d]}=='
                                  '（没反转 now，`g` 同理）'),
        'f[now][d] = sf[k - d - 1]': ('`f[{now}][{d}] = sf[{k-d-1}] + ma_f[{d}] + nums[{now}]` = `{sf[k-d-1]} + {ma_f[d]} + {nums[now]}`'
                                      ' = =={f[now][d]}==：一个孩子取 `d-1`，其余取 `k-d-1`'),
        'f[now][0] = -sg[k - 1]': ('反转 `{now}` 自己：孩子里最近的反转点至少离它 `k-1` → 用 `g` 取孩子最小再变号：'
                                   '`f[{now}][0] = −sg[{k-1}] − nums[{now}]` = =={f[now][0]}=='),
        'f[now][d] = f[now][d + 1]': '收尾逆序：「距离 ≥ {d}」包含「距离 ≥ {d+1}」，所以 `f[{now}][{d}]` 补成 `f[{now}][{d+1}]` = =={f[now][d]}==（`g` 同理取最小）',
        'return f[0][0]': '答案 `f[0][0] = {ret}`：反转根 0，再看孩子们',
    },
    cards=dict(
        one_liner='f 记最大、g 记最小，d 记「最近的反转点离我多远」',
        complexity='时间 `O(n·k)`，空间 `O(n·k)`',
        problem=['无向树，根为 0，点权 `nums`；可反转若干节点：以它为根的子树所有值 ×(−1)',
                 '任意两个被反转的节点距离至少为 `k`，求操作后点权和的最大值',
                 '本视频：`edges=[[0,1],[0,2]]`，`nums=[3,-5,-4]`，`k=3` → `6`',
                 '（原文的题意；1 和 2 之间距离为 2 < 3，不能同时反转）'],
        quote='因为子树内部的反转距离限制一般是在递归计算时就解决掉了，因此主要需要考虑的还是==兄弟子树间节点的距离==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[now][d]`：最近的反转点距 now ≥ d 时的最大和；`g` 取最小，因为反转 now 时孩子要「最小」才变号后最大',
              '`d=0`：反转 now，孩子侧取 `g[·][k-1]` 变号；`d+d>=k`：直接累加孩子 `d-1`',
              '`d+d<k`：挑一个孩子取 `d-1`，其余取 `k-d-1`，用 `ma_f` 找最优那个',
              '最后从 `k-1` 到 `0` 逆序取 max / min：「≥ d」包含「≥ d+1」'],
        summary=['时间 `O(n·k)`，空间 `O(n·k)`',
                 '反转 now 时 `f` 和 `g` 要==交叉更新==（变号后最大 ↔ 最小）',
                 '`d+d<k` 才需要考虑兄弟子树，所以 `ma_f / mi_g` 只在这时有值（其余位置是 `None`）',
                 '最后的逆序循环别漏：它让 `f[now][d]` 单调，也补上了没赋值的格子',
                 '原文可直接在 Python 3 运行，未改动'],
    ),
)
