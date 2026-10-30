K = 2
PRICES = [1, 4, 2, 7]
NINF = float('-inf')


def _s(x):
    return '-∞' if x == NINF else str(x)


def _shown(S, h, i_col, j):
    """has f[i_col][j][h] been computed yet (or is it a boundary value)?"""
    if i_col == 0 or j == 0:
        return True
    i, ln = S.get('i'), S.get('_line')
    f = S['f']
    if i is None:
        return ln == 11
    if i_col <= i:
        return True
    if i_col > i + 1:
        return False
    # i_col == i + 1
    if ln == 7:
        return f[i + 1][1][0] != NINF
    jj = S.get('j')
    if jj is None:
        return False
    if j < jj:
        return True
    if j > jj:
        return False
    return h == 0 or ln == 10


def _hi(S):
    i, j, ln = S.get('i'), S.get('j'), S.get('_line')
    out = {}
    if i is None or j is None:
        if ln == 11:
            out[(0, len(S['f']) - 1, len(S['f'][0]) - 1)] = 'green'
        return out
    if ln == 9:
        out[(0, i + 1, j)] = 'green'
        out[(0, i, j)] = 'blue'
        out[(1, i, j)] = 'pink'
    elif ln == 10:
        out[(1, i + 1, j)] = 'green'
        out[(1, i, j)] = 'blue'
        out[(0, i, j - 1)] = 'pink'
    return out


def _tables(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    if f is None:
        return
    nc, nr = len(f), len(f[0])
    hi = _hi(S)
    gap = 24
    w = (x1 - x0 - 40 - gap) / 2
    for h in range(2):
        tx = x0 + 20 + h * (w + gap)
        title = 'f[i][j][0]：未持有' if h == 0 else 'f[i][j][1]：持有'
        cv.text((tx + 4, y0 + 4), title, 24, T['muted'], bold=True)
        lw = 92
        cell = min(72, (w - lw) / nc, (y1 - y0 - 80) / nr)
        sx, sy = tx + lw, y0 + 70
        for c in range(nc):
            cv.text((sx + c * cell + cell / 2, sy - 6), f'f[{c}]', 18, T['muted'], anchor='mb', mono=True)
        for j in range(nr):
            cv.text((sx - 8, sy + j * cell + cell / 2 - 10), f'j={j}', 18, T['muted'], anchor='rm', mono=True)
            cv.text((sx - 8, sy + j * cell + cell / 2 + 12), '非法' if j == 0 else f'至多{j - 1}笔', 16, T['dim'], anchor='rm')
            for c in range(nc):
                X, Y = sx + c * cell, sy + j * cell
                col = hi.get((h, c, j))
                shown = _shown(S, h, c, j)
                v = f[c][j][h]
                bv = B.get('f')
                changed = bv is not None and bv[c][j][h] != v
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=T[col] if col else (T['panel2'] if j else (38, 34, 40)),
                        r=6, outline=T['yellow'] if changed else T['border'], width=3 if changed else 1)
                txt = _s(v) if shown else '·'
                cv.text((X + cell / 2, Y + cell / 2), txt, int(cell * 0.38), T['bg'] if col else (T['text'] if j else T['dim']),
                        anchor='mm', bold=True)


def _prices(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S.get('prices') or PRICES
    i = S.get('i')
    cv.text((x0 + 18, y0 + 4), f'prices（k = {K}：至多 {K} 笔交易）', 24, T['muted'], bold=True)
    cell = 120
    sx = x0 + 20 + 56 + 120
    for k, v in enumerate(p):
        X = sx + k * cell
        on = k == i
        cv.rect((X + 6, y0 + 44, X + cell - 6, y0 + 104), fill=T['orange'] if on else T['panel2'], r=10,
                outline=T['border'])
        cv.text((X + cell / 2, y0 + 74), v, 30, T['bg'] if on else (T['dim'] if i is not None and k > i else T['text']),
                anchor='mm', bold=True)
        cv.text((X + cell / 2, y0 + 110), f'第 {k} 天', 18, T['dim'], anchor='mt')


def _formula(S, B):
    ln, i, j = S.get('_line'), S.get('i'), S.get('j')
    f = S.get('f')
    if ln == 9:
        a, b, p = f[i][j][0], f[i][j][1], S['p']
        return (f"`f[{i + 1}][{j}][0] = max(f[{i}][{j}][0], f[{i}][{j}][1] + {p})`"
                f" = max({_s(a)}, {_s(b + p)}) = =={_s(f[i + 1][j][0])}==")
    if ln == 10:
        a, b, p = f[i][j][1], f[i][j - 1][0], S['p']
        return (f"`f[{i + 1}][{j}][1] = max(f[{i}][{j}][1], f[{i}][{j - 1}][0] − {p})`"
                f" = max({_s(a)}, {_s(b - p)}) = =={_s(f[i + 1][j][1])}==")
    if ln in (4, 5, 6):
        return '`j = 0` 一行对应 `dfs(·, -1, ·)`：交易 -1 次不合法，==全是 -∞=='
    return ''


def _cap_sell(S, B, ret):
    i, j, p, f = S.i, S.j, S.p, S.f
    keep, sell = f[i][j][0], f[i][j][1] + p
    return (f'第 {i} 天·==未持有==·至多 {j - 1} 笔：不动 `{_s(keep)}`，卖出 `{_s(f[i][j][1])} + {p} = {_s(sell)}`'
            f' → `{_s(f[i + 1][j][0])}`')


def _cap_buy(S, B, ret):
    i, j, p, f = S.i, S.j, S.p, S.f
    keep, buy = f[i][j][1], f[i][j - 1][0] - p
    return (f'第 {i} 天·==持有==·至多 {j - 1} 笔：不动 `{_s(keep)}`，买入（用掉 1 笔）`{_s(f[i][j - 1][0])} − {p} = {_s(buy)}`'
            f' → `{_s(f[i + 1][j][1])}`')


CONFIG = dict(
    num=188, title='买卖股票的最佳时机 IV', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP：在 122 的基础上加一维 j',
    tags=['面试经典150'],
    code='''
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        f = [[[-inf] * 2 for _ in range(k + 2)] for _ in range(n + 1)]
        for j in range(1, k + 2):
            f[0][j][0] = 0
        for i, p in enumerate(prices):
            for j in range(1, k + 2):
                f[i + 1][j][0] = max(f[i][j][0], f[i][j][1] + p)
                f[i + 1][j][1] = max(f[i][j][1], f[i][j - 1][0] - p)
        return f[-1][-1][0]
''',
    call=f'Solution().maxProfit({K}, {PRICES})',
    expect=8,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='custom', draw=_prices, h=150),
        dict(type='custom', draw=_tables, h=420),
    ],
    skip=['for j in range(1, k + 2)'],
    watch=[('i', 'i', 'orange'), ('p', 'p', 'orange'), ('j', 'j', 'cyan')],
    captions={
        'n = len(prices)': '`n = {n}` 天，`k = {k}`',
        'f = [[[-inf]': '`f[i+1][j+1][hold]` ↔ `dfs(i, j, hold)`：`j` 的范围 `[-1, k]` 共 ==`k + 2`== 个数，初始全是 `-inf`',
        'f[0][j][0] = 0': lambda S, B, ret: (f'`f[0][{S.j}][0] = 0`：第 0 天前不持有、交易次数合法 → 利润 0（递归边界 `i < 0`）'
                                             if S.j == 1 else f'`f[0][{S.j}][0] = 0`'),
        'for i, p in enumerate': lambda S, B, ret: (f'第 `{S.i}` 天，`p = {S.p}`：枚举 `j = 1..{S.k + 1}`'
                                                    if S.get('i') != B.get('i') else '所有天数处理完毕'),
        'f[i + 1][j][0] = max': _cap_sell,
        'f[i + 1][j][1] = max': _cap_buy,
        'return f[-1][-1][0]': '最后一天、至多 `k` 笔、不持有：`f[{n}][{k + 1}][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='在 122 的状态里加一维 j：至多还能交易几次',
        complexity='时间 `O(nk)`，空间 `O(nk)`（可优化到 `O(k)`）',
        problem=['`prices[i]` 是第 `i` 天的股价，==至多==完成 `k` 笔交易（买 + 卖 = 一笔）',
                 '手里最多持有一股，求最大利润。示例：`k = 2`，`[3,2,6,5,0,3]` → `7`',
                 f'本视频：`k = {K}`，`{PRICES}` → `8`（1 买 4 卖 + 2 买 7 卖）'],
        before=[dict(heading='第一步：记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i, j, hold)`：前 `i` 天至多买入 `j` 次，第 `i` 天结束时是否持有',
            '持有 = `max(dfs(i-1, j, True), dfs(i-1, j-1, False) - p)`；未持有 = `max(dfs(i-1, j, False), dfs(i-1, j, True) + p)`',
            '边界：`j < 0` → `-inf`；`i < 0` → 持有 `-inf`、未持有 `0`',
        ])],
        quote='在 122 的基础上，添加一个参数 j，表示当前可以至多交易 j 次。⚠注意：买入 + 卖出才算一笔交易，不是两笔交易。',
        quote_src='—— 灵茶山艾府题解 · 一、记忆化搜索',
        idea_heading='第二步：1:1 翻译成递推',
        idea=['`j` 的范围 `[-1, k]` 共 `k + 2` 个数 → `f[i+1][j+1][hold]` ↔ `dfs(i, j, hold)`',
              '`f` 中 `j = 0` 对应交易 `-1` 次，==不合法==，初始值必须是 `-inf`',
              '「`j-1` 写在买入时」：今天买入，之前只能多买 `j-1` 次'],
        after=[dict(heading='第三步：空间优化 & 思考题', lines=[
            '去掉第一维，`j` ==倒序==枚举（避免用到今天刚算出的值），空间 `O(k)`',
            '恰好 `k` 笔：只初始化 `f[0][1][0] = 0`；至少 `k` 笔：「至少 0 次」按 122 转移',
        ])],
        summary=['时间 `O(nk)`，空间 `O(nk)` → `O(k)`',
                 '第二维大小 `k + 2`；`j = 0` 一行全是 `-inf`；`f[0][j][0] = 0`（`j ≥ 1`）',
                 '买入时 `j - 1`，卖出时 `j` 不变（写在卖出时也对）',
                 '股票系列 121 / 122 / 123 / 188 / 309 / 714 都是这套状态机 DP'],
    ),
)
