import math as _math


def _gdraw(cv, T, box, title, pos, edges, color_of, sub_of=None, ecolor_of=None, R=26):
    """有向图：pos = [(fx, fy)]（0~1 的相对位置），edges = [(a, b)]"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), title, 22, T['muted'], bold=True)
    Wd, Hd = x1 - x0 - 100, y1 - y0 - 110
    P = [(x0 + 50 + fx * Wd, y0 + 60 + fy * Hd) for fx, fy in pos]
    es = set(edges)
    for a, b in edges:
        ec = (ecolor_of(a, b) if ecolor_of else None) or 'dim'
        col = T[ec] if isinstance(ec, str) else ec
        (xa, ya), (xb, yb) = P[a], P[b]
        if a == b:
            cv.arc_arrow((xa - 12, ya - R + 2), (xa + 12, ya - R + 2), 46, col, 3, 11)
            continue
        dx, dy = xb - xa, yb - ya
        L = _math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        off = 9 if (b, a) in es else 0
        nx, ny = -uy * off, ux * off
        cv.arrow((xa + ux * (R + 3) + nx, ya + uy * (R + 3) + ny), (xb - ux * (R + 6) + nx, yb - uy * (R + 6) + ny), col, 3, 12)
    for i, (x, y) in enumerate(P):
        c = color_of(i)
        fill = T[c] if isinstance(c, str) else (c or T['panel2'])
        cv.rect((x - R, y - R, x + R, y + R), fill=fill, outline=T['border'], r=R)
        cv.text((x, y), i, 26, T['bg'] if c else T['muted'], anchor='mm', bold=True)
        if sub_of:
            s = sub_of(i)
            if s:
                cv.text((x, y + R + 6), s, 19, T['text'], anchor='mt', mono=True)
    return P


REC = [1, 1, 1, 2, 3]
K = 3
_N = len(REC)
POS = [(0.62, 0.95), (0.62, 0.38), (0.41, 0.38), (0.2, 0.38), (0.0, 0.38)]


def _col(S, i):
    if 'pa' not in S:
        return None
    if 'ans' in S:
        if i == S.get('i'):
            return 'pink'
        if i == S.get('x'):
            return 'blue'
        return None
    if i == S.get('x'):
        return 'blue'
    if S.get('_line') in (8, 9, 10) and i == S.get('p'):
        return 'yellow'
    return None


def _draw_g(cv, S, B, box, T):
    r = S['receiver']
    _gdraw(cv, T, box, 'receiver 图：i → receiver[i]（蓝 = x，黄 = 跳到的点，粉 = 起点）', POS,
           [(i, r[i]) for i in range(_N)], lambda i: _col(S, i))


def _draw_t(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pa = S['pa']
    n = len(pa)
    cols = len(pa[0])
    cv.text((x0 + 18, y0 + 4), 'pa[x][j] = (走 2^j 步到的点, 这 2^j 步经过的编号和，不含 x)', 22, T['muted'], bold=True)
    cw = min(210, (x1 - x0 - 110) / cols)
    rh = min(46, (y1 - y0 - 100) / (n + 1))
    sx, sy = x0 + 80, y0 + 56
    for j in range(cols):
        cv.text((sx + j * cw + cw / 2, sy), f'j={j}（{2 ** j} 步）', 20, T['dim'], anchor='mm', mono=True)
    line = S.get('_line', 0)
    ans = 'ans' in S
    for x in range(n):
        Y = sy + 22 + x * rh
        hot_row = (x == S.get('x') and not ans) or (ans and x == S.get('x'))
        cv.text((sx - 16, Y + rh / 2), f'x={x}', 22, T['pink'] if (ans and x == S.get('i')) else (T['blue'] if hot_row else T['muted']), anchor='rm', mono=True, bold=True)
        for j in range(cols):
            v = pa[x][j]
            X = sx + j * cw
            fill = T['panel2']
            col = T['text'] if v is not None else T['dim']
            if not ans and 'i' in S and hot_row:
                if j == S['i'] and v is not None and line in (8, 9, 10):
                    fill = (40, 74, 120)       # 读 pa[x][i]
                elif j == S['i'] + 1 and v is not None and line == 10:
                    fill = (110, 88, 30)       # 刚写入 pa[x][i+1]
            if not ans and 'p' in S and x == S['p'] and 'i' in S and j == S['i'] and v is not None and line in (9, 10):
                fill = (110, 40, 78)           # 读 pa[p][i]
            cv.rect((X + 4, Y + 2, X + cw - 4, Y + rh - 2), fill=fill, outline=T['border'], r=8)
            cv.text((X + cw / 2, Y + rh / 2), f'({v[0]},{v[1]})' if v is not None else '?', 22, col, anchor='mm', mono=True, bold=v is not None)
    if ans and 'j' in S:
        j = S['j']
        cv.rect((sx + j * cw + 2, sy + 12, sx + j * cw + cw - 2, sy + 22 + n * rh + 2), outline=T['yellow'], width=3, r=10)


def _cap_bit(S, B, ret):
    b = (K >> S.j) & 1
    return f'`k` 的第 {S.j} 位（二进制 `{K:b}` 从低往高）是 `{b}` → ' + (f'==要跳 {2 ** S.j} 步==' if b else '这一位是 0，不跳')


CONFIG = dict(
    num=2836, title='在传球游戏中最大化函数值', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='树上倍增 · 二进制拆 k',
    tags=['灵神题单·图论算法', '灵神题单·链表树与回溯', '难度分 2769'],
    code='''
class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        m = k.bit_length() - 1
        pa = [[(p, p)] + [None] * m for p in receiver]
        for i in range(m):
            for x in range(n):
                p, s = pa[x][i]
                pp, ss = pa[p][i]
                pa[x][i + 1] = (pp, s + ss)  # 合并节点值之和

        ans = 0
        for i in range(n):
            x = sum = i
            for j in range(m + 1):
                if (k >> j) & 1:  # k 的二进制从低到高第 j 位是 1
                    x, s = pa[x][j]
                    sum += s
            ans = max(ans, sum)
        return ans
''',
    call=f'Solution().getMaxFunctionValue({REC}, {K})',
    expect=10,
    views=[
        dict(type='text', fn=lambda S: f'k = {K} = 二进制 `{K:b}`：k 步 = 拆成若干个 2^j 步，每一位 1 跳一次' if 'receiver' in S else ''),
        dict(type='custom', draw=_draw_g, h=250),
        dict(type='custom', draw=_draw_t, h=300),
    ],
    watch=[('i', 'i', 'pink'), ('x', 'x', 'blue'), ('sum', lambda S: S['sum'] if 'ans' in S else 0, 'yellow'), ('ans', 'ans', 'green')],
    skip=['n = len(receiver)'],
    max_steps=62,
    captions={
        'm = k.bit_length()': '`k = {k}` 的二进制是 `{k:b}`，最高位是 2^{m}：只要预处理到走 2^{m} 步，所以 `m = {m}`',
        'pa = [[(p, p)]': '`pa[x][0] = (receiver[x], receiver[x])`：走 1 步到 `p`，沿途编号和（不含 x）就是 `p` 自己；后面几列先空着',
        'p, s = pa[x][i]': '从 `{x}` 走 2^{i} 步 → 到 `p = {p}`，沿途编号和 `s = {s}`',
        'pp, ss = pa[p][i]': '再从 `{p}` 走 2^{i} 步 → 到 `pp = {pp}`，沿途和 `ss = {ss}`',
        'pa[x][i + 1] =': '倍增合并：走 2^{i + 1} 步 = 两段 2^{i} 步 → 到 `{pp}`，和 `{s} + {ss}` = =={s + ss}==',
        'ans = 0': '预处理完毕。现在枚举每个起点 `i`，按 k 的二进制一段一段往前跳',
        'x = sum = i': '起点 `{i}`：`x` 是当前位置，`sum` 先记上起点自己的编号 `{i}`',
        'if (k >> j) & 1': _cap_bit,
        'x, s = pa[x][j]': '一次跳 {2 ** j} 步：`{B.x}` → `{x}`，这一段经过的编号和 `s = {s}`',
        'sum += s': '累加：`sum` = `{B.sum} + {s}` = =={sum}==',
        'ans = max(ans, sum)': '`f({i}) = {sum}`；`ans = max({B.ans}, {sum}) = {ans}`',
        'return ans': '最大的函数值 = =={ret}==',
    },
    cards=dict(
        one_liner='k 太大不能模拟：预处理跳 2^j 步，再按 k 的二进制跳',
        complexity='时间 `O(n log k)`，空间 `O(n log k)`',
        problem=['`receiver[i]` 是 `i` 传球给的人，从 `x` 出发传 `k` 次',
                 '`f(x)` = `x` + 之后每个接球人的编号之和（重复触球累加），求 `f(x)` 最大值',
                 '本视频：`receiver = [1,1,1,2,3]`，`k = 3` → `10`'],
        quote='利用倍增算法，预处理每个节点 x 的第 2^i 个祖先节点，以及从 x 的父节点到 x 的第 2^i 个祖先节点的节点编号之和。最后枚举起点 x，一边向上跳一边累加节点编号。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pa[x][i]` 存两个数：走 2^i 步到哪里，沿途编号和（不含起点）',
              '`pa[x][i+1]` 由两段 2^i 合并：先到 `p`，再从 `p` 走一段，和相加',
              '枚举起点，k 的二进制哪一位是 1 就跳哪一段，`k` 最大 10^10 也只要 34 位'],
        summary=['时间 `O(n log k)`，空间 `O(n log k)`',
                 '`sum` 先记起点自己，`pa` 里的和不含起点，别漏也别重复加',
                 '`m = k.bit_length() - 1`，列数是 `m + 1`',
                 '做法就是树上倍增模板；思考题是 `O(n)`：把内向基环树的树枝和环分开处理'],
    ),
)
