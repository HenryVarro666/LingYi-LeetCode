POS = {'EUR': (0.1, 0.18), 'USD': (0.9, 0.18), 'JPY': (0.9, 0.82), 'CHF': (0.1, 0.82)}


def _fmt(v):
    return f'{v:.4g}'


def _draw(cv, S, B, box, T):
    import math
    x0, y0, x1, y1 = box
    pairs, rates = S.get('pairs'), S.get('rates')
    if pairs is None:
        pairs, rates = S.get('pairs1'), S.get('rates1')
        day = 0
    else:
        day = 1 if pairs == S.get('pairs1') else 2
    if pairs is None:
        return
    amount = S.get('amount') or {}
    inn = S['_inner']
    cur = inn.get('x') if 'cur_amount' in inn else None
    to = inn.get('to') if cur else None
    gw = (x1 - x0) * 0.58
    R = 46

    def P(u):
        fx, fy = POS[u]
        return x0 + 70 + fx * (gw - 140), y0 + 90 + fy * (y1 - y0 - 220)

    if day:
        cv.text((x0 + 20, y0 + 12), f'第 {day} 天汇率图（箭头旁 = 汇率）', 22, T['muted'], bold=True)
    for (a, b), r in zip(pairs, rates):
        (ax, ay), (bx, by) = P(a), P(b)
        d = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / d, (by - ay) / d
        hot = (cur == a and to == b) or (cur == b and to == a)
        cv.arrow((ax + ux * R, ay + uy * R), (bx - ux * (R + 4), by - uy * (R + 4)),
                 T['yellow'] if hot else T['muted'], 6 if hot else 3, 16 if hot else 12)
        mx, my = (ax + bx) / 2 - uy * 24, (ay + by) / 2 + ux * 24
        cv.text((mx, my), f'×{r}', 24, T['yellow'] if hot else T['cyan'], anchor='mm', bold=True)
    for u in POS:
        X, Y = P(u)
        seen = u in amount
        cv.d.ellipse((X - R, Y - R, X + R, Y + R), fill=T['green'] if seen else T['panel2'],
                     outline=T['yellow'] if u == cur else T['border'], width=6 if u == cur else 2)
        cv.text((X, Y - (12 if seen else 0)), u, 22, T['bg'] if seen else T['text'], anchor='mm', bold=True)
        if seen:
            cv.text((X, Y + 16), _fmt(amount[u]), 22, T['bg'], anchor='mm', bold=True)
    lx = x0 + gw + 20
    rows = [('amount（本次 DFS）', amount, 'yellow'), ('day1_amount', S.get('day1_amount'), 'cyan'),
            ('day2_amount', S.get('day2_amount'), 'orange')]
    yy = y0 + 16
    for name, dct, c in rows:
        if name.startswith('amount') and not amount:
            continue
        cv.text((lx, yy), name, 21, T[c], bold=True)
        yy += 36
        for k, v in (dct or {}).items():
            cv.text((lx + 12, yy), f'{k}: {_fmt(v)}', 22, T['text'], mono=True)
            yy += 30
        yy += 12


def _skipchk(S, B, ret):
    to = S.to
    if to in B.amount:
        return f'`{to}` 已经算出金额 → 不再递归（汇率不矛盾，重复算结果一样）'
    return f'`{to}` 还没到过 → 要递归过去'


def _ret(S, B, ret):
    d1, d2 = S.day1_amount, S.day2_amount
    items = {x: d1.get(x, 0.0) / a2 for x, a2 in d2.items()}
    s = '，'.join(f'{x}:{_fmt(v)}' for x, v in items.items())
    return f'枚举中转货币 x：`day1[x] / day2[x]` → {s}；最大 =={_fmt(ret)}=='


CONFIG = dict(
    num=3387, title='两天自由外汇交易后的最大货币数', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='两次 DFS 算金额 · 枚举中转货币',
    tags=['灵神题单', '图论算法', '难度分 1788'],
    code='''
class Solution:
    def calc_amount(self, pairs: List[List[str]], rates: List[float], initialCurrency: str) -> Dict[str, float]:
        g = defaultdict(list)
        for (x, y), r in zip(pairs, rates):
            g[x].append((y, r))
            g[y].append((x, 1.0 / r))

        amount = {}
        def dfs(x: str, cur_amount: float) -> None:
            amount[x] = cur_amount
            for to, rate in g[x]:
                # 每个节点只需递归一次（重复递归算出来的结果是一样的，因为题目保证汇率没有矛盾）
                if to not in amount:
                    dfs(to, cur_amount * rate)
        dfs(initialCurrency, 1.0)
        return amount

    def maxAmount(self, initialCurrency: str, pairs1: List[List[str]], rates1: List[float], pairs2: List[List[str]], rates2: List[float]) -> float:
        day1_amount = self.calc_amount(pairs1, rates1, initialCurrency)
        day2_amount = self.calc_amount(pairs2, rates2, initialCurrency)
        return max(day1_amount.get(x, 0.0) / a2 for x, a2 in day2_amount.items())
''',
    call='Solution().maxAmount("EUR", [["EUR","USD"],["USD","JPY"]], [2.0,3.0], [["JPY","USD"],["USD","CHF"],["CHF","EUR"]], [4.0,5.0,6.0])',
    expect=720.0,
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='calls', h=150),
    ],
    watch=[('x', lambda S: S['_inner'].get('x'), 'yellow'), ('cur_amount', lambda S: S['_inner'].get('cur_amount'), 'green')],
    skip=['g = defaultdict', 'for (x, y), r in zip', 'amount = {}', 'def dfs'],
    max_steps=90,
    captions={
        'g[x].append((y, r))': '建图：`{x} → {y}` 汇率 `{r}`',
        'g[y].append((x, 1.0 / r))': '反向边：`{y} → {x}` 汇率 `1 / {r}` = {1.0 / r:.4g}',
        'amount[x] = cur_amount': '记录 `amount[{x}] = {cur_amount:.4g}`：1 单位 `{initialCurrency}` 能换到的 {x}',
        'if to not in amount': _skipchk,
        'dfs(to, cur_amount * rate)': '递归：到 `{B.to}`，金额 `{B.cur_amount:.4g} × {B.rate:.4g}` = =={B.cur_amount * B.rate:.4g}==',
        'dfs(initialCurrency, 1.0)': '从 `{initialCurrency}` 出发 DFS，初始金额 1.0',
        'return amount': '这一天能到的货币和金额：`{amount}`',
        'day1_amount = ': '第 1 天：1 {initialCurrency} 能换成的各种货币',
        'day2_amount = ': '第 2 天同理。==day2 金额的倒数==就是把这种货币换回 {initialCurrency} 的汇率',
        'return max(': _ret,
    },
    cards=dict(
        one_liner='第 1 天换到 x，第 2 天换回来：答案 = max(day1[x] / day2[x])',
        complexity='时间 `O((n+m)L)`，空间 `O((n+m)L)`',
        problem=['初始 1.0 单位 `initialCurrency`，第 1 天、第 2 天各有一组汇率，可任意次兑换',
                 '每个货币对反向兑换的汇率是 `1 / rate`；求两天后最多有多少初始货币',
                 '示例：`EUR`，两天的汇率如图 → `720.0`'],
        quote='枚举中转货币 x，答案为 day1Amount[x] / day2Amount[x] 的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两天独立：各建一张图，从 `initialCurrency` DFS，边走边乘汇率得到金额',
              '第 2 天从 x 换回初始货币 = ==day2[x] 的倒数==（把第 2 天的路反着走）',
              '汇率无矛盾，所以每个点只递归一次，不用管走哪条路'],
        summary=['时间 `O((n+m)L)`，空间同；L 是货币名长度',
                 '==每个点只 DFS 一次==：`if to not in amount`，汇率保证无矛盾',
                 '第 1 天没到过的货币用 `get(x, 0.0)`，比值为 0 不会被选中',
                 '思考题：多天时把每天的货币拆成「第 i 天的 x」节点再建图'],
    ),
)
