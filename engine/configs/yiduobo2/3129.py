ZERO, ONE, LIMIT = 2, 2, 1


def _sources(S):
    """当前这一步用到的格子：[(表名, i, j, 颜色)]"""
    ln, i, j = S.get('_line'), S.get('i'), S.get('j')
    if not isinstance(i, int) or not isinstance(j, int):
        return []
    L = LIMIT
    if ln == 16:
        return [('sg', i - 1, j, 'green'), ('sg', i - L - 1, j, 'red')]
    if ln == 18:
        return [('sg', i - 1, j, 'green')]
    if ln == 21:
        return [('sf', i, j - 1, 'green'), ('sf', i, j - L - 1, 'red')]
    if ln == 23:
        return [('sf', i, j - 1, 'green')]
    if ln == 27:
        return [('f', i, j, 'green')] + ([('sf', i, j - 1, 'green')] if j > 0 else [])
    if ln == 31:
        return [('g', i, j, 'green')] + ([('sg', i - 1, j, 'green')] if i > 0 else [])
    return []


def _target(S):
    ln = S.get('_line')
    return {16: 'f', 18: 'f', 21: 'g', 23: 'g', 27: 'sf', 31: 'sg'}.get(ln)


TITLES = {'f': 'f[i][j]：末位是 0', 'g': 'g[i][j]：末位是 1',
          'sf': 'sf：f 沿 j 的前缀和', 'sg': 'sg：g 沿 i 的前缀和'}


def _table(cv, S, T, name, x0, y0, w, h):
    M = S.get(name)
    cv.text((x0 + 6, y0), TITLES[name], 22, T['muted'], bold=True)
    if not isinstance(M, list):
        cv.text((x0 + 6, y0 + 40), '（尚未创建）', 20, T['dim'])
        return
    R, Cn = len(M), len(M[0])
    cell = min(64, (w - 50) / Cn, (h - 70) / R)
    gx, gy = x0 + 40, y0 + 56
    srcs = _sources(S)
    tgt = _target(S)
    ci, cj = S.get('i'), S.get('j')
    for j in range(Cn):
        cv.text((gx + j * cell + cell / 2, gy - 6), f'j={j}', 16, T['dim'], anchor='mb', mono=True)
    for i in range(R):
        cv.text((gx - 8, gy + i * cell + cell / 2), f'i={i}', 16, T['dim'], anchor='rm', mono=True)
        for j in range(Cn):
            X, Y = gx + j * cell, gy + i * cell
            fill = T['panel2']
            for nm, si, sj, c in srcs:
                if nm == name and si == i and sj == j:
                    fill = T[c]
            out, wd = T['border'], 1
            if name == tgt and i == ci and j == cj:
                out, wd = T['yellow'], 4
            elif i == ci and j == cj:
                out, wd = T['orange'], 2
            cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, outline=out, width=wd, r=6)
            v = M[i][j]
            tc = T['bg'] if fill != T['panel2'] else (T['text'] if v else T['dim'])
            cv.text((X + cell / 2, Y + cell / 2), v, 24, tc, anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) / 2, (y1 - y0) / 2
    _table(cv, S, T, 'f', x0 + 10, y0 + 8, w - 20, h - 10)
    _table(cv, S, T, 'g', x0 + w + 10, y0 + 8, w - 20, h - 10)
    _table(cv, S, T, 'sf', x0 + 10, y0 + h + 4, w - 20, h - 10)
    _table(cv, S, T, 'sg', x0 + w + 10, y0 + h + 4, w - 20, h - 10)


def _text(S):
    i, j = S.get('i'), S.get('j')
    if not isinstance(i, int) or not isinstance(j, int):
        return f'`zero = {ZERO}`，`one = {ONE}`，`limit = {LIMIT}`：连续相同的数最多 `{LIMIT}` 个'
    return f'状态 `({i}, {j})`：用了 `{i}` 个 0、`{j}` 个 1（黄框 = 正在算的格子，绿 = 加，红 = 减）'


def _cap_f_sub(S, B, ret):
    i, j, L = S.i, S.j, LIMIT
    a, b = S.sg[i - 1][j], S.sg[i - L - 1][j]
    return (f'`i = {i} > limit`：末尾连续 0 有 1~{L} 个 → `f[{i}][{j}] = g[{i - L}..{i - 1}][{j}]` 之和'
            f' = `sg[{i - 1}][{j}] − sg[{i - L - 1}][{j}] = {a} − {b}` = =={S.f[i][j]}==')


def _cap_f(S, B, ret):
    i, j = S.i, S.j
    return f'`0 < i ≤ limit`：末尾的 0 段可以一直延伸到开头 → `f[{i}][{j}] = sg[{i - 1}][{j}]` = =={S.f[i][j]}=='


def _cap_g_sub(S, B, ret):
    i, j, L = S.i, S.j, LIMIT
    a, b = S.sf[i][j - 1], S.sf[i][j - L - 1]
    return (f'`j = {j} > limit`：末尾连续 1 有 1~{L} 个 → `g[{i}][{j}]` = `sf[{i}][{j - 1}] − sf[{i}][{j - L - 1}] = {a} − {b}`'
            f' = =={S.g[i][j]}==')


def _cap_g(S, B, ret):
    i, j = S.i, S.j
    return f'`0 < j ≤ limit` → `g[{i}][{j}] = sf[{i}][{j - 1}]` = =={S.g[i][j]}=='


def _cap_sf(S, B, ret):
    i, j = S.i, S.j
    if j == 0:
        return f'前缀和起点：`sf[{i}][0] = f[{i}][0]` = {S.sf[i][j]}'
    return f'`sf[{i}][{j}] = sf[{i}][{j - 1}] + f[{i}][{j}] = {B.sf[i][j]} + {S.f[i][j]}` = {S.sf[i][j]}'


def _cap_sg(S, B, ret):
    i, j = S.i, S.j
    if i == 0:
        return f'前缀和起点：`sg[0][{j}] = g[0][{j}]` = {S.sg[i][j]}'
    return f'`sg[{i}][{j}] = sg[{i - 1}][{j}] + g[{i}][{j}] = {B.sg[i][j]} + {S.g[i][j]}` = {S.sg[i][j]}'


CONFIG = dict(
    num=3129, title='找出所有稳定的二进制数组 I', difficulty='Medium', category='多维动态规划',
    author='yiduobo', technique='f/g 记末位 + 前缀和优化转移',
    tags=['字节30天'],
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
    call=f'Solution().numberOfStableArrays({ZERO}, {ONE}, {LIMIT})',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('i', 'i', 'orange'), ('j', 'j', 'orange'), ('limit', 'limit')],
    skip=['g = [[0]', 'sg = [[0]', 'sf[0][0] = sg[0][0] = 0', 'mod = 10', 'for i in range', 'for j in range',
          'if i > limit', 'elif i > 0', 'if j > limit', 'elif j > 0', 'if j > 0', 'if i > 0',
          'sf[i][j] = sf[i][j - 1]', 'sg[i][j] = sg[i - 1][j]'],
    captions={
        3: '`f[i][j]`：`i` 个 0、`j` 个 1、==最后一位是 0== 的稳定数组个数；`g[i][j]`：最后一位是 1',
        5: '`sf`：`f` 沿 `j` 方向的前缀和；`sg`：`g` 沿 `i` 方向的前缀和（把区间和变成两个前缀相减）',
        'f[0][0] = g[0][0] = 1': '起点：`f[0][0] = g[0][0] = 1`，作为"空数组"分别接 0 段、1 段的起点',
        'f[i][j] = (sg[i - 1][j] - sg[i - limit - 1][j] + mod) % mod': _cap_f_sub,
        'f[i][j] = sg[i - 1][j]': _cap_f,
        'g[i][j] = (sf[i][j - 1] - sf[i][j - limit - 1] + mod) % mod': _cap_g_sub,
        'g[i][j] = sf[i][j - 1]': _cap_g,
        'sf[i][j] = (sf[i][j] + f[i][j]) % mod': _cap_sf,
        'sg[i][j] = (sg[i][j] + g[i][j]) % mod': _cap_sg,
        'return (f[-1][-1] + g[-1][-1]) % mod': '答案 = 末位是 0 + 末位是 1：`f[{zero}][{one}] + g[{zero}][{one}]` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='状态只记末位是 0 还是 1，用前缀和把 O(limit) 的转移降到 O(1)',
        complexity='时间 `O(zero · one)`，空间 `O(zero · one)`',
        problem=['二进制数组恰好有 `zero` 个 0、`one` 个 1，且==每个长度超过 limit 的子数组都同时含 0 和 1==',
                 '等价于：连续相同的数最多 `limit` 个；求这样的数组个数（模 `10^9 + 7`）',
                 '示例：`zero = 1, one = 2, limit = 1` → `1`（只有 `[1,0,1]`）',
                 '本视频：`zero = 2, one = 2, limit = 1` → `2`（`[0,1,0,1]`、`[1,0,1,0]`）'],
        quote='令f[i][j]表示由i个0，j个1组成，且==最后一位为0==的稳定数组数目，令g[i][j]表示由i个0，j个1组成，且最后一位为1的稳定数组数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['末尾是 1~limit 个连续 0：`f[i][j] = g[i−1][j] + … + g[i−limit][j]`',
              '同理 `g[i][j] = f[i][j−1] + … + f[i][j−limit]`',
              '区间和 → ==前缀和相减==：`f[i][j] = sg[i−1][j] − sg[i−limit−1][j]`，转移 `O(1)`'],
        summary=['时间、空间 `O(zero · one)`；3130 题（数据更大）同一份代码也能过',
                 '为什么只记末位：状态数已是 `zero × one`，连续段长度靠转移来保证',
                 '易错：`i ≤ limit` 时没有要减去的部分（会越界），代码分了两种情况',
                 '取模后做减法要 `+ mod` 再 `% mod`，避免负数（Python 其实不会负，但这是好习惯）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
