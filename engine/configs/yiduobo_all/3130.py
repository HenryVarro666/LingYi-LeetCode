def _num(S, name):
    return S.get(name)


def _col(name):
    def fn(S, r, c, v):
        i, j = S.get('i'), S.get('j')
        line = S.get('_line')
        if i is None or j is None or 'limit' not in S:
            return None
        lim = S['limit']
        if line == 17 or line == 19:      # f[i][j] 来自 sg 的列区间
            if name == 'f' and (r, c) == (i, j):
                return 'yellow'
            if name == 'sg' and c == j and (r == i - 1 or (i > lim and r == i - lim - 1)):
                return 'blue' if r == i - 1 else 'pink'
        if line in (22, 24):              # g[i][j] 来自 sf 的行区间
            if name == 'g' and (r, c) == (i, j):
                return 'yellow'
            if name == 'sf' and r == i and (c == j - 1 or (j > lim and c == j - lim - 1)):
                return 'blue' if c == j - 1 else 'pink'
        if line in (28,) and name == 'sf' and (r, c) == (i, j):
            return 'yellow'
        if line in (32,) and name == 'sg' and (r, c) == (i, j):
            return 'yellow'
        return None
    return fn


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None:
        return '`f` = 最后一位是 0，`g` = 最后一位是 1；`sg` 按列累加 g，`sf` 按行累加 f'
    return f'当前格 `({i}, {j})`：{i} 个 0、{j} 个 1'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    specs = [('f', 'f：最后一位是 0', 0, 0), ('g', 'g：最后一位是 1', 1, 0),
             ('sf', 'sf：f 沿行累加', 0, 1), ('sg', 'sg：g 沿列累加', 1, 1)]
    cw = (x1 - x0) / 2
    ch = (y1 - y0) / 2
    cmap = {'yellow': T['yellow'], 'blue': T['blue'], 'pink': T['pink']}
    for name, lab, cx, cy in specs:
        g = S.get(name)
        if g is None:
            continue
        R, C = len(g), len(g[0])
        cell = min(72, (cw - 90) / C, (ch - 90) / R)
        ox = x0 + cx * cw + (cw - cell * C) / 2 + 14
        oy = y0 + cy * ch + 64
        cv.text((x0 + cx * cw + 20, y0 + cy * ch + 8), lab, 24, T['muted'], bold=True)
        fn = _col(name)
        for j in range(C):
            cv.text((ox + j * cell + cell / 2, oy - 4), j, 18, T['dim'], anchor='mb', mono=True)
        for i in range(R):
            cv.text((ox - 8, oy + i * cell + cell / 2), i, 18, T['dim'], anchor='rm', mono=True)
            for j in range(C):
                c = fn(S, i, j, g[i][j])
                X, Y = ox + j * cell, oy + i * cell
                changed = B.get(name) is not None and B[name][i][j] != g[i][j]
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=cmap[c] if c else T['panel2'], r=6,
                        outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
                cv.text((X + cell / 2, Y + cell / 2), g[i][j], 26, T['bg'] if c else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=3130, title='找出所有稳定的二进制数组 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='结尾分类 DP + 前缀和优化区间转移',
    tags=['灵神题单·动态规划', '难度分 2825'],
    code='''
class Solution(object):
    def numberOfStableArrays(self, zero, one, limit):

        f = [[0] * (one + 1) for _ in range(zero + 1)]
        g = [[0] * (one + 1) for _ in range(zero + 1)]
        sf = [[0] * (one + 1) for _ in range(zero + 1)]
        sg = [[0] * (one + 1) for _ in range(zero + 1)]

        f[0][0] = g[0][0] = 1
        sf[0][0] = sg[0][0] = 0

        mod = 10 ** 9 + 7

        for i in range(zero + 1):
            for j in range(one + 1):
                if i > limit:
                    f[i][j] = (sg[i - 1][j] - sg[i - limit - 1][j] + mod) % mod
                elif i > 0:
                    f[i][j] = sg[i - 1][j]

                if j > limit:
                    g[i][j] = (sf[i][j - 1] - sf[i][j - limit - 1] + mod) % mod
                elif j > 0:
                    g[i][j] = sf[i][j - 1]

                if j > 0:
                    sf[i][j] = sf[i][j - 1]
                sf[i][j] = (sf[i][j] + f[i][j]) % mod

                if i > 0:
                    sg[i][j] = sg[i - 1][j]
                sg[i][j] = (sg[i][j] + g[i][j]) % mod

        return (f[-1][-1] + g[-1][-1]) % mod
''',
    call='Solution().numberOfStableArrays(2, 2, 1)',
    expect=2,
    skip=['mod = 10', 'for i in range(zero + 1)', 'for j in range(one + 1)', 'elif', 'if i > limit:', 'if j > limit:', 'if j > 0:', 'if i > 0:',
          'sf[i][j] = sf[i][j - 1]', 'sg[i][j] = sg[i - 1][j]', 'sf[0][0] = sg[0][0]'],
    views=[
        dict(type='custom', draw=_draw, h=560),
        dict(type='text', fn=_txt, size=22, h=50),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), 'limit'],
    max_steps=80,
    captions={
        4: '`f[i][j]`：最后一位是 0 的稳定数组数',
        5: '`g[i][j]`：最后一位是 1 的稳定数组数',
        6: '`sf`：`f` 沿 j 方向的前缀和，用来 O(1) 求 `g` 的区间和',
        7: '`sg`：`g` 沿 i 方向的前缀和，用来 O(1) 求 `f` 的区间和',
        'f[0][0] = g[0][0] = 1': '空数组记 1 种，给后面的转移当起点',
        'f[i][j] = (sg': lambda S, B, r: f'`i = {S.i} > limit = {S.limit}`：末尾至多 limit 个 0，减去超出的一段：`f[{S.i}][{S.j}] = sg[{S.i - 1}][{S.j}] − sg[{S.i - S.limit - 1}][{S.j}]` = =={S.f[S.i][S.j]}=='
                                          ,
        'f[i][j] = sg[i - 1][j]': lambda S, B, r: (f'`i = {S.i} ≤ limit`：不会超限，直接取前缀和 `sg[{S.i - 1}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'g[i][j] = (sf': lambda S, B, r: f'`j = {S.j} > limit = {S.limit}`：减去超出的一段：`g[{S.i}][{S.j}] = sf[{S.i}][{S.j - 1}] − sf[{S.i}][{S.j - S.limit - 1}]` = =={S.g[S.i][S.j]}==',
        'g[i][j] = sf[i][j - 1]': lambda S, B, r: f'`j = {S.j} ≤ limit`：不会超限，直接取前缀和 `sf[{S.i}][{S.j - 1}]` = =={S.g[S.i][S.j]}==',
        'sf[i][j] = (sf': '`sf[{i}][{j}]` = 左边的前缀和 + `f[{i}][{j}]` = =={sf[i][j]}==',
        'sg[i][j] = (sg': '`sg[{i}][{j}]` = 上边的前缀和 + `g[{i}][{j}]` = =={sg[i][j]}==',
        'return (f': '最后一位是 0 的 + 是 1 的：`{f[-1][-1]} + {g[-1][-1]}` = =={ret}==',
    },
    cards=dict(
        one_liner='结尾分 0 和 1 两类，区间和用前缀和 O(1) 取',
        complexity='时间 `O(zero·one)`，空间 `O(zero·one)`',
        problem=['由 `zero` 个 0、`one` 个 1 组成，长度大于 `limit` 的子数组都要同时含 0 和 1',
                 '求这样的稳定二进制数组个数（对 `10^9+7` 取模）',
                 '示例：`zero=3, one=3, limit=2` → `14`；本视频用 `2, 2, 1` → `2`'],
        quote='f[i][j] = g[i - 1][j] + g[i - 2][j] + ... + g[i - limit][j] ……上面的转移方程复杂度为O(limit)，需要优化。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：最后一位是 0；末尾是连续 1…limit 个 0，前面一定接一个 1 结尾的数组',
              '所以 `f[i][j]` 是 `g[i-1..i-limit][j]` 的区间和，`g` 同理是 `f[i][j-1..j-limit]` 的区间和',
              '用前缀和 `sg`、`sf` 把区间和变成两项相减，转移降到 `O(1)`'],
        summary=['时间 `O(zero·one)`，空间 `O(zero·one)`（四张表）',
                 '易错：只有 `i > limit` 才能减 `sg[i-limit-1]`，所以代码分 `if / elif` 防越界',
                 '`(a - b + mod) % mod`：减法后先加 `mod` 再取模',
                 '`f[0][0] = g[0][0] = 1` 是空数组起点，`sf[0][0] = sg[0][0] = 0` 是原文写法',
                 '对比灵神：他用 `f[i-1][j][0] + f[i-1][j][1] − f[i-limit-1][j][1]`，不单独维护前缀和'],
    ),
)
