PRICES = [1, 4, 2, 6, 3]
NAMES = ['buy_one', 'sell_one', 'buy_two', 'sell_two']
LABELS = ['买入一次', '卖出一次', '买入两次', '卖出两次']
ACTIVE = {10: 'sell_two', 11: 'sell_two', 12: 'sell_two', 14: 'buy_two', 15: 'buy_two', 16: 'buy_two',
          18: 'sell_one', 19: 'sell_one', 21: 'buy_one'}


def _states(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '四个状态：到今天为止，做完这些操作后的最大收益（None = 还不存在）', 24, T['muted'], bold=True)
    act = ACTIVE.get(S.get('_line'))
    bw, bh, gap = 200, 130, 46
    total = 4 * bw + 3 * gap
    sx = x0 + (x1 - x0 - total) / 2
    y = y0 + 70
    for k, nm in enumerate(NAMES):
        X = sx + k * (bw + gap)
        v = S.get(nm)
        changed = nm in S and nm in B and S[nm] != B[nm]
        fill = (60, 52, 30) if nm == act else T['panel2']
        cv.rect((X, y, X + bw, y + bh), fill=fill, outline=T['yellow'] if changed else (T['orange'] if nm == act else T['border']),
                width=4 if changed or nm == act else 1, r=14)
        cv.text((X + bw / 2, y + 22), nm, 22, T['muted'], anchor='mm', mono=True)
        s = '—' if v is None else str(v)
        cv.text((X + bw / 2, y + 68), s if nm in S else '', 44, T['dim'] if v is None else (T['yellow'] if changed else T['text']),
                anchor='mm', bold=True)
        cv.text((X + bw / 2, y + bh + 22), LABELS[k], 22, T['text'], anchor='mm')
        if k:
            ax = X - gap
            cv.arrow((ax + 6, y + bh / 2), (X - 6, y + bh / 2), T['muted'], 3, 11)
            cv.text((ax + gap / 2, y + bh / 2 - 14), '+p' if k % 2 else '−p', 22, T['green'] if k % 2 else T['pink'], anchor='mb', bold=True)
    yo = y + bh + 80
    cv.text((x0 + 18, yo), '每天的更新顺序（倒着来，保证用到的都是昨天的值）：', 24, T['muted'], bold=True)
    order = ['sell_two', 'buy_two', 'sell_one', 'buy_one']
    xx = x0 + 40
    for k, nm in enumerate(order):
        s = f'{"①②③④"[k]} {nm}'
        w = cv.tlen(s, 26, mono=True) + 28
        on = nm == act
        cv.rect((xx, yo + 44, xx + w, yo + 92), fill=T['orange'] if on else T['panel2'], r=10)
        cv.text((xx + w / 2, yo + 68), s, 26, T['bg'] if on else T['text'], anchor='mm', mono=True, bold=on)
        xx += w + 14
        if k < 3:
            cv.text((xx - 7, yo + 68), '→', 24, T['muted'], anchor='mm')
            xx += 10


def _cand(name, expr_fn, old_fn, verb):
    def f(S, B, ret):
        c = expr_fn(S)
        old = old_fn(B)
        if old is None:
            return f'{verb}得 `{c}`；`{name}` 还不存在 → ==直接取它=='
        if old < c:
            return f'{verb}得 `{c}` > 之前的 `{old}` → ==更新=='
        return f'{verb}得 `{c}`，不比之前的 `{old}` 好 → 保持不变'
    return f


def _exists(dep, what):
    def f(S, B, ret):
        if B[dep] is None:
            return f'`{dep}` 还不存在 → 不可能{what}，跳过'
        return f'`{dep} = {B[dep]}` 已存在 → 可以考虑{what}'
    return f


CONFIG = dict(
    num=123, title='买卖股票的最佳时机 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='四状态 DP + 滚动变量',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
class Solution(object):
    def maxProfit(self, prices):
        if not prices:
            return 0

        buy_one = -prices[0]
        buy_two = sell_one = sell_two = None

        for i in range(1, len(prices)):
            if buy_two is not None:
                if sell_two is None or sell_two < buy_two + prices[i]:
                    sell_two = buy_two + prices[i]

            if sell_one is not None:
                if buy_two is None or buy_two < sell_one - prices[i]:
                    buy_two = sell_one - prices[i]

            if sell_one is None or sell_one < buy_one + prices[i]:
                sell_one = buy_one + prices[i]

            buy_one = max(buy_one, -prices[i])

        if sell_one is None: sell_one = -1
        if sell_two is None: sell_two = -1
        return max(0, sell_one, sell_two)
''',
    call=f'Solution().maxProfit({PRICES})',
    expect=7,
    views=[
        dict(type='array', var='prices', label='prices（i = 今天）', cell=84, pointers={'i': 'blue'},
             color=lambda S, i, v: 'blue' if i == S.get('i') else None, dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='custom', draw=_states, h=440),
    ],
    watch=[('i', 'i', 'blue'), ('prices[i]', 'prices[i]')],
    captions={
        3: '`prices` 不为空 → 继续（空数组会直接返回 0）',
        6: '第 0 天只能买入：`buy_one = -{prices[0]}`',
        7: '另外三个状态在第 0 天==还不存在==，用 `None` 表示',
        9: lambda S, B, ret: (f'第 `{S.i}` 天，价格 `{S.prices[S.i]}`：按 sell_two → buy_two → sell_one → buy_one 倒着更新'
                              if S.get('i') != B.get('i') else '所有天处理完毕'),
        10: _exists('buy_two', '第二次卖出'),
        11: _cand('sell_two', lambda S: S.buy_two + S.prices[S.i], lambda B: B.sell_two, '今天第二次卖出：`buy_two + prices[i]` '),
        12: '`sell_two = {sell_two}`：用的是==昨天的== buy_two（它还没被今天覆盖）',
        14: _exists('sell_one', '第二次买入'),
        15: _cand('buy_two', lambda S: S.sell_one - S.prices[S.i], lambda B: B.buy_two, '今天第二次买入：`sell_one − prices[i]` '),
        16: '`buy_two = {B.sell_one} − {prices[i]}` = =={buy_two}==',
        18: _cand('sell_one', lambda S: S.buy_one + S.prices[S.i], lambda B: B.sell_one, '今天第一次卖出：`buy_one + prices[i]` '),
        19: '`sell_one = {buy_one} + {prices[i]}` = =={sell_one}==',
        21: '`buy_one = max({B.buy_one}, −{prices[i]})` = =={buy_one}==：记住最低的买入价',
        23: lambda S, B, ret: ('`sell_one` 从未出现 → 当作 −1' if B.sell_one is None else f'`sell_one = {S.sell_one}` 存在，不用处理'),
        24: lambda S, B, ret: ('`sell_two` 从未出现 → 当作 −1' if B.sell_two is None else f'`sell_two = {S.sell_two}` 存在，不用处理'),
        25: '答案 = `max(0, 卖一次 {sell_one}, 卖两次 {sell_two})` = =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='四个状态：买一次、卖一次、买两次、卖两次，倒着滚动更新',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是股票第 `i` 天的价格，你==最多完成两笔交易==',
                 '不能同时参与多笔交易：再次买入前必须卖掉手里的股票',
                 '示例：`[3,3,5,0,0,3,1,4]` → `6`；本视频：`[1,4,2,6,3]` → `7`'],
        quote='需要特别注意的是，在更新的过程中需要按 sell_two -> buy_two -> sell_one -> buy_one 这个顺序进行更新。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i][j]`：前 i 天、第 j 种状态（刚买一次 / 刚卖一次 / 刚买两次 / 刚卖两次）的最佳收益',
              '每个状态 = max(之前就做过，==今天做==)；今天做必须从前一个状态转移过来',
              '只依赖前一天 → 滚动成 4 个变量；倒着更新，否则会用到今天刚算出的值'],
        result='`sell_two = 7`：`1` 买 `4` 卖赚 3，`2` 买 `6` 卖赚 4 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`None` 表示状态还不存在：先有第一次买入，才有第一次卖出……',
                 '易错：顺序写成 buy_one 先更新，就可能同一天买了又卖',
                 '推广到 k 次：设 `2k` 个状态依次转移（即 188 题）',
                 '原文为 Python 2 风格，代码未改，仅删去 docstring'],
    ),
)
