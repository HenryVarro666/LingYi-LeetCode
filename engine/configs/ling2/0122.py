PRICES = [7, 1, 5, 3, 6, 4]


def _tbl(S):
    """columns not computed yet are shown as · (they still hold the initial 0)"""
    f = S.get('f')
    if f is None:
        return None
    i, ln = S.get('i'), S.get('_line')
    rows = [[r[0] for r in f], [r[1] for r in f]]
    if i is None:
        upto = 0 if ln in (4, 5) else len(f) - 1
        part = None
    elif ln == 6 and f[i + 1] == [0, 0]:
        upto, part = i, None
    elif ln == 7:
        upto, part = i, 0
    else:
        upto, part = i + 1, None
    for c in range(len(f)):
        for r in range(2):
            if c > upto and not (part == r and c == upto + 1):
                rows[r][c] = None
    return rows


def _tcolor(S, r, c, v):
    i = S.get('i')
    ln = S.get('_line')
    if i is None:
        return 'purple' if (r, c) == (1, 0) and ln == 5 else None
    if c == i + 1:
        if (ln == 7 and r == 0) or (ln == 8 and r == 1):
            return 'green'
    if c == i and ln in (7, 8):
        src = {7: [(0, 'blue'), (1, 'pink')], 8: [(1, 'blue'), (0, 'pink')]}[ln]
        for rr, cc in src:
            if rr == r:
                return cc
    if ln == 9 and (r, c) == (0, len(S['prices'])):
        return 'green'
    return None


def _formula(S, B):
    ln, i = S.get('_line'), S.get('i')
    f = S.get('f')
    if ln == 7:
        a, b, p = f[i][0], f[i][1], S['p']
        return f"`f[{i + 1}][0] = max(f[{i}][0], f[{i}][1] + {p})` = max({_s(a)}, {_s(b + p)}) = =={_s(f[i + 1][0])}=="
    if ln == 8:
        a, b, p = f[i][1], f[i][0], S['p']
        return f"`f[{i + 1}][1] = max(f[{i}][1], f[{i}][0] − {p})` = max({_s(a)}, {_s(b - p)}) = =={_s(f[i + 1][1])}=="
    if ln == 5:
        return '`f[0][1] = -inf`：第 0 天之前不可能持有股票（对应递归边界 `dfs(-1, True) = -inf`）'
    if f is not None and i is None:
        return '`f[i+1]` 对应 `dfs(i)`：多出的 `f[0]` 存递归边界 `dfs(-1, ·)`'
    return ''


def _s(x):
    return '-inf' if x == float('-inf') else str(x)


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    ln = S.get('_line')
    items = [('green', '正在计算'), ('blue', '今天不操作'), ('pink', '今天卖出' if ln == 7 else '今天买入' if ln == 8 else '今天买/卖')]
    for c, t in items:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 40


def _cap_sell(S, B, ret):
    i, p, f = S.i, S.p, S.f
    keep, sell = f[i][0], f[i][1] + p
    how = '今天卖出更赚' if sell > keep else '不操作'
    return (f'第 {i} 天结束==未持有==：昨天就未持有 `{_s(keep)}`，或昨天持有今天卖出 `{_s(f[i][1])} + {p} = {_s(sell)}` '
            f'→ {how}，`{_s(f[i + 1][0])}`')


def _cap_buy(S, B, ret):
    i, p, f = S.i, S.p, S.f
    keep, buy = f[i][1], f[i][0] - p
    how = '今天买入更好' if buy > keep else '继续持有'
    return (f'第 {i} 天结束==持有==：昨天就持有 `{_s(keep)}`，或昨天未持有今天买入 `{f[i][0]} − {p} = {buy}` '
            f'→ {how}，`{_s(f[i + 1][1])}`')


CONFIG = dict(
    num=122, title='买卖股票的最佳时机 II', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP：记忆化搜索 → 递推',
    tags=['热题173', '面试经典150'],
    code='''
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        f = [[0] * 2 for _ in range(n + 1)]
        f[0][1] = -inf
        for i, p in enumerate(prices):
            f[i + 1][0] = max(f[i][0], f[i][1] + p)
            f[i + 1][1] = max(f[i][1], f[i][0] - p)
        return f[n][0]
''',
    call=f'Solution().maxProfit({PRICES})',
    expect=7,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='bars', var='prices', label='prices（第 i 天的股价）', pointers={'i': 'orange'}, h=270,
             color=lambda S, k, v: 'orange' if k == S.get('i') else None,
             dim=lambda S, k, v: S.get('i') is not None and k > S['i'], cell=110),
        dict(type='table', var=_tbl, label='f（列 = f[0..n]，f[i+1] 对应第 i 天结束）', rows=['未持有', '持有'],
             cols=lambda S: [f'f[{k}]' for k in range(len(S['f']))], color=_tcolor, cell=110, h=230),
        dict(type='custom', draw=_legend, h=44),
    ],
    watch=[('i', 'i', 'orange'), ('p', 'p', 'orange'), ('未持有 f[i+1][0]', lambda S: _tbl(S)[0][S['i'] + 1] if 'i' in S else None, 'green'),
           ('持有 f[i+1][1]', lambda S: _tbl(S)[1][S['i'] + 1] if 'i' in S else None, 'purple')],
    captions={
        'n = len(prices)': '`n = {n}` 天',
        'f = [[0] * 2': '`f` 有 `n + 1 = {len(f)}` 行：`f[i+1][hold]` ↔ `dfs(i, hold)`，==整体右移一位==放递归边界',
        'f[0][1] = -inf': '`f[0][1] = -inf`：第一天开始前不可能持有股票；`f[0][0] = 0`',
        'for i, p in enumerate': lambda S, B, ret: (f'第 `{S.i}` 天，股价 `p = {S.p}`' if S.get('i') != B.get('i')
                                                    else '所有天数处理完毕'),
        'f[i + 1][0] = max': _cap_sell,
        'f[i + 1][1] = max': _cap_buy,
        'return f[n][0]': '最后一天结束时==不持有==股票才是最大利润：`f[{n}][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='每天结束时只有两种状态：持有 / 未持有，从前一天转移过来',
        complexity='时间 `O(n)`，空间 `O(n)`（可优化到 `O(1)`）',
        problem=['`prices[i]` 是第 `i` 天的股价，可以买卖==任意多次==',
                 '但手里最多只能持有一股（必须先卖再买），求最大利润',
                 '示例：`[7,1,5,3,6,4]` → `7`（1 买 5 卖 + 3 买 6 卖）'],
        before=[dict(heading='第一步：状态定义 + 记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i, hold)`：第 `i` 天==结束时==持有 / 未持有股票的最大利润',
            '未持有：昨天就未持有 `dfs(i-1, False)`，或昨天持有今天卖出 `dfs(i-1, True) + prices[i]`',
            '持有：昨天就持有 `dfs(i-1, True)`，或昨天未持有今天买入 `dfs(i-1, False) - prices[i]`',
            '边界：`dfs(-1, False) = 0`，`dfs(-1, True) = -inf`（不合法）',
        ])],
        quote='注意本题 dfs 可能会算出负数，不能用 −1 作为 memo 数组的初始值。可以改用其他 dfs 算不出的值。',
        quote_src='—— 灵茶山艾府题解 · 一、记忆化搜索',
        idea_heading='第二步：1:1 翻译成递推',
        idea=['`f[i+1][hold]` 对应 `dfs(i, hold)`，`f[0]` 对应递归边界 `dfs(-1, ·)`',
              '`f[0][0] = 0`，`f[0][1] = -inf`；答案 `f[n][0]`（最后不持有）',
              '递推顺序：`i` 从小到大，每天先算未持有、再算持有'],
        after=[dict(heading='第三步：空间优化', lines=[
            '`f[i+1]` 只依赖 `f[i]` → 两个变量 `f0, f1` 就够了',
            '`f0, f1 = max(f0, f1 + p), max(f1, f0 - p)`（同时赋值，用的都是昨天的值）',
            '空间 `O(1)`；这套模板可以直接推广到 123 / 188 / 309 / 714',
        ])],
        summary=['时间 `O(n)`，空间 `O(n)` → 优化后 `O(1)`',
                 '`f[0][1]` 必须是 `-inf`：第 0 天前不可能持有',
                 '答案取 `f[n][0]`：最后持有股票一定不如卖掉',
                 '套路：状态机 DP，==状态 = (天数, 是否持有)==，转移 = 今天买 / 卖 / 不操作',
                 '另一种思路：贪心，所有上涨日的差价都赚到'],
    ),
)
