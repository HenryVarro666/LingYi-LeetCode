def _color(S, i, j, v):
    I = S['_inner']
    n, m = I.get('n'), I.get('m')
    if n is not None and m is not None and (i, j) == (min(n, m), max(n, m)):
        return 'yellow'
    if v is not None:
        return 'green'
    return None


_PC = ['blue', 'pink', 'green', 'purple', 'yellow']


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    I = B['_inner']
    n, m = I.get('n'), I.get('m')
    if n is None or m is None:
        return
    n, m = min(n, m), max(n, m)
    cv.text((x0 + 18, y0 + 4), f'当前子问题：{n} × {m}（行 × 列）' + ('；风车拆法：4 个角 + 中间 1 块' if 'l' in I else ''), 24, T['muted'], bold=True)
    sc = min((x1 - x0 - 330) / m, (y1 - y0 - 70) / n, 90)
    ox, oy = x0 + 40, y0 + 50
    cv.rect((ox, oy, ox + m * sc, oy + n * sc), outline=T['border'], width=3)
    if all(k in I for k in ('i', 'j', 'k', 'l')) and n == I['n'] and m == I['m']:
        i, j, k, l = I['i'], I['j'], I['k'], I['l']
        parts = [('p1', i, j, 0, 0), ('p2', k, m - j, j, 0), ('p3', n - k, l, m - l, k),
                 ('p4', n - i, m - l, 0, i), ('p5', k - i, l - (m - j), m - l, i)]
        for idx, (name, h, w, px, py) in enumerate(parts):
            c = T[_PC[idx]]
            if h > 0 and w > 0:
                cv.rect((ox + px * sc + 2, oy + py * sc + 2, ox + (px + w) * sc - 2, oy + (py + h) * sc - 2), fill=c, alpha=150, r=6)
                cv.text((ox + (px + w / 2) * sc, oy + (py + h / 2) * sc), name, 22, T['bg'], anchor='mm', bold=True)
            ty = oy + idx * 40
            cv.rect((ox + m * sc + 40, ty + 6, ox + m * sc + 62, ty + 28), fill=c, r=4)
            cv.text((ox + m * sc + 74, ty + 17), f'{name} = {h}×{w}' + (f' → {B[name]}' if name in B else ''), 24, T['text'], anchor='lm', mono=True)
    else:
        cv.rect((ox + 2, oy + 2, ox + m * sc - 2, oy + n * sc - 2), fill=T['yellow'], alpha=90, r=6)


CONFIG = dict(
    num=1240, title='铺瓷砖', difficulty='Hard', category='二叉树与回溯',
    author='yiduobo', technique='记忆化递归 · 周围四块 + 中间一块的拼法',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def tilingRectangle(self, n, m):

        if n > m:
            n, m = m, n

        f = [[None] * (m + 1) for _ in range(n + 1)]

        return  self.dfs(n, m, f)

    def dfs(self, n, m, f):
        if n > m:
            n, m = m, n
        if f[n][m] is None:
            if m == 0:
                f[n][m] = 0
            elif n % m == 0:
                f[n][m] = n // m
            else:
                f[n][m] = n * m
                for i in range(1, n + 1):
                    for j in range(1, m + 1):
                        for k in range(i, n + 1):
                            for l in range(m - j, m + 1):
                                p1 = self.dfs(i, j, f)
                                p2 = self.dfs(k, m - j, f)
                                p3 = self.dfs(n - k, l, f)
                                p4 = self.dfs(n - i, m - l, f)
                                p5 = self.dfs(k - i, l - (m - j), f)
                                f[n][m] = min(f[n][m], p1 + p2 + p3 + p4 + p5)
        return f[n][m]
''',
    call='Solution().tilingRectangle(2, 3)',
    expect=3,
    views=[
        dict(type='custom', draw=_draw, h=250),
        dict(type='table', var='f', label='f[a][b]：a × b 的矩形最少几块（黄 = 当前，绿 = 已算好，空 = 还没算）',
             rows=lambda S: list(range(len(S['f']))) if 'f' in S else [], cols=lambda S: list(range(len(S['f'][0]))) if 'f' in S else [],
             color=_color, cell=60, h=230),
        dict(type='calls', h=130),
    ],
    watch=[('n', lambda S: S['_inner'].get('n'), 'blue'), ('m', lambda S: S['_inner'].get('m'), 'pink'),
           ('i', lambda S: S['_inner'].get('i'), 'cyan'), ('j', lambda S: S['_inner'].get('j'), 'orange')],
    skip=['if n > m', 'for i in range', 'for j in range', 'for k in range', 'for l in range', 'if m == 0', 'f = [[None]'],
    captions={
        'n, m = m, n': '交换使 `n <= m`：==f[i][j] 和 f[j][i] 一定相等==，只存一半',
        'return  self.dfs': '开始：用记忆化递归求 `dfs({n}, {m})`，`f` 里 None 表示还没算过',
        'if f[n][m] is None': lambda S, B, r: (
            f'`f[{S.n}][{S.m}]` 还没算过 → 开始算' if S.f[S.n][S.m] is None
            else f'`f[{S.n}][{S.m}] = {S.f[S.n][S.m]}` ==算过了== → 直接用，不再重复枚举'),
        'f[n][m] = 0': '宽为 0 的矩形不需要瓷砖：`f[{n}][{m}] = 0`',
        'elif n % m == 0': lambda S, B, r: (
            (f'`n = 0`：空矩形，也满足 `n % m == 0` → 不需要瓷砖' if S.n == 0 else f'`n % m == 0`（`{S.n} % {S.m} = 0`）→ 恰好是正方形，一块瓷砖就够') if S.n % S.m == 0
            else f'`{S.n} % {S.m} = {S.n % S.m} != 0` → 不能直接铺满，需要枚举拼法'),
        'f[n][m] = n // m': lambda S, B, r: (f'空矩形：`f[0][{S.m}] = 0`' if S.n == 0 else f'一块 `{S.n}×{S.m}` 的瓷砖铺满：`f[{S.n}][{S.m}] = {S.f[S.n][S.m]}`'),
        'f[n][m] = n * m': '先假设最坏：全用 `1×1` 小瓷砖，`f[{n}][{m}] = {n}×{m} = {f[n][m]}`；下面枚举风车拆法来压低它',
        'p1 = ': '风车拆法：枚举 `i,j,k,l` 把 `{B.n}×{B.m}` 切成 4 个角 + 中间 1 块。左上 `p1` 是 `{B.i}×{B.j}`，递归取最少块数',
        'p2 = ': '右上 `p2`：`{B.k}×{B.m - B.j}`',
        'p3 = ': '右下 `p3`：`{B.n - B.k}×{B.l}`',
        'p4 = ': '左下 `p4`：`{B.n - B.i}×{B.m - B.l}`',
        'p5 = ': '正中间 `p5`：`{B.k - B.i}×{B.l - (B.m - B.j)}`，宽或高为 0 就没有这一块',
        'f[n][m] = min': '五块之和 `{p1}+{p2}+{p3}+{p4}+{p5}` = =={p1 + p2 + p3 + p4 + p5}==，`f[{n}][{m}] = min(旧值, 和)` → =={f[n][m]}==',
        'return f[n][m]': '`dfs` 返回 `f[{n}][{m}] = {ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='把矩形拆成风车：四个角各一块矩形，中间再补一小块',
        complexity='状态 `O(n·m)`，每个状态枚举 `O(n²m²)` 种拆法',
        problem=['给定 `n × m` 的矩形，用==整数边长的正方形==铺满，求最少需要几块',
                 '示例：`n=2, m=3` → `3`（一个 `2×2`、两个 `1×1`）',
                 '示例 3：`n=11, m=13` → `6`',
                 '本视频：`n=2, m=3` → `3`'],
        quote='没有想出什么很好的做法，简单看上去应该可以将所有情况归类到样例3中的情况，分别为左上角的8 * 4的矩形，右上角的5 * 5的矩形，右下角的6 * 6的矩形，左下角的7 * 7的矩形，以及中间的1 * 1的小矩形。',
        quote_src='—— yiduobo 题解原文',
        idea=['把任意铺法看成「风车」：四周 4 个矩形 + 中间 1 个小矩形',
              '令 `f[i][j]` = `i×j` 矩形的最少块数，枚举四个切点，递归算这 5 块再相加',
              '`f[i][j] = f[j][i]`，所以总是交换成 `i <= j`；用 `f` 记忆化避免重复',
              '初始值取 `n*m`（全用 1×1），再用 `min` 不断压低'],
        result='`dfs(2, 3)` 的最少块数是 3 ✓',
        summary=['状态 `O(nm)`，每个状态枚举 `O(n²m²)` 种拆法，只适合 `n, m <= 13`',
                 '递归到 `f[i][j]` 里已有值就直接用：这是记忆化的关键',
                 '代码里 `n % m == 0`（`n <= m` 时只在正方形命中）；其余倍数关系靠枚举也能得到正确值',
                 '风车拆法是作者归类出的经验做法；原文为 Python 2 写法，`n / m` 已改为 `n // m`'],
    ),
)
