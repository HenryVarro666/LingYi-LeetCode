PRICES = [100, 80, 60, 70, 60, 75, 85]
L_WHILE, L_POP, L_INC, L_APP, L_RET = 7, 8, 9, 10, 11


def _cur(S):
    d = S.get('self.cur_day')
    if d is None or 'price' not in S:
        return None
    return d + 1 if S.get('_line') in (L_WHILE, L_POP) else d


def _stack_days(S):
    return [d for d, _ in (S.get('self.stack') or [])]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '每天的价格（蓝 = 今天，紫 = 还在栈里，灰 = 已被弹出）', 24, T['muted'], bold=True)
    n = len(PRICES)
    cur = _cur(S)
    days = set(_stack_days(S))
    cell = min(130, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cell * n) / 2
    base, top = y1 - 72, y0 + 80
    scale = (base - top) / max(PRICES)
    for i, v in enumerate(PRICES):
        X = sx + i * cell
        bw = cell * 0.6
        bx0, bx1 = X + (cell - bw) / 2, X + (cell + bw) / 2
        if cur is None or i > cur:
            cv.rect((bx0, base - v * scale, bx1, base), outline=T['border'], width=2, r=4)
            cv.text((X + cell / 2, base - v * scale - 4), v, 22, T['dim'], anchor='mb')
        else:
            fill = T['blue'] if i == cur else (T['purple'] if i in days else (70, 76, 86))
            cv.rect((bx0, base - v * scale, bx1, base), fill=fill, r=4)
            cv.text((X + cell / 2, base - v * scale - 4), v, 24, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 8), f'第{i}天', 18, T['dim'], anchor='mt')
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if S.get('_line') == L_RET and cur is not None:
        prev = S['self.stack'][-2][0]
        a = sx + (prev + 1) * cell + 6
        b = sx + (cur + 1) * cell - 6
        y = base + 38
        cv.line([(a, y - 10), (a, y), (b, y), (b, y - 10)], T['green'], 3)
        cv.text(((a + b) / 2, y + 4), f'跨度 {cur - prev}', 22, T['green'], anchor='mt', bold=True)


def _fmt(x):
    d, p = x
    return f'{d}:∞' if p == float('inf') else f'{d}:{p}'


def _while(S, B, ret):
    top = S['self.stack'][-1]
    p = S.price
    if p >= top[1]:
        return f'`price = {p} ≥ 栈顶价格 {top[1]}`（第 {top[0]} 天）→ 栈顶==不可能再当后面的「上一个更大元素」=='
    tp = '∞' if top[1] == float('inf') else top[1]
    return f'`price = {p} < 栈顶价格 {tp}` → 栈顶就是 ==上一个更大元素==，停止弹栈'


CONFIG = dict(
    num=901, title='股票价格跨度', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 找上一个更大元素',
    tags=['labuladong', '灵神题单·单调栈', '难度分 1709'],
    code='''
class StockSpanner:
    def __init__(self):
        self.stack = [(-1, inf)]  # 这样无需判断栈为空的情况
        self.cur_day = -1  # 第一个 next 调用算作第 0 天

    def next(self, price: int) -> int:
        while price >= self.stack[-1][1]:
            self.stack.pop()  # 栈顶数据后面不会再用到了，因为 price 更大
        self.cur_day += 1
        self.stack.append((self.cur_day, price))
        return self.cur_day - self.stack[-2][0]
''',
    call=f'''s = StockSpanner()
ans = [s.next(p) for p in {PRICES}]
ans''',
    expect=[1, 1, 1, 2, 1, 4, 6],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='stack', var='self.stack', label='self.stack（天:价格，价格严格递减）', fmt=_fmt, h=120),
    ],
    watch=[('price', 'price', 'blue'), ('cur_day', 'self.cur_day', 'cyan'),
           ('栈顶', lambda S: _fmt(S['self.stack'][-1]) if S.get('self.stack') else '', 'purple')],
    captions={
        'self.stack = [': '栈底放哨兵 `(-1, ∞)`：==栈永远不会空==，省去特判',
        'self.cur_day = -1': '`cur_day = -1`：第一次 `next` 算第 0 天',
        'while price >=': _while,
        'self.stack.pop()': '弹出 `{B["self.stack"][-1]}`：它 ≤ 今天且更远，==以后再也用不到==',
        'self.cur_day += 1': '今天是第 `{self.cur_day}` 天，价格 `{price}`',
        'self.stack.append(': '把 `({self.cur_day}, {price})` 入栈：它可能是后面某天的上一个更大元素',
        'return self.cur_day': '上一个更大元素在第 `{self.stack[-2][0]}` 天 → 跨度 `{self.cur_day} − ({self.stack[-2][0]})` = =={ret}==',
    },
    max_steps=80,
    cards=dict(
        one_liner='跨度 = 到上一个更大元素的距离；比今天小的旧价格直接扔掉',
        complexity='均摊 `O(1)` / 次，空间 `O(min(q, U))`',
        problem=['每天输入一个股票价格 `price`，返回今天的==价格跨度==：',
                 '从今天往前数，连续 `≤ price` 的天数（含今天）',
                 '示例：`100,80,60,70,60,75,85` → `1,1,1,2,1,4,6`'],
        quote='对于小于等于 price 的数 x，不可能作为后续 next 输入的数的上一个更大元素（因为 x≤price 且更远）。所以一旦发现小于等于 price 的数，就直接移除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['十六字真言：==及时去掉无用数据，保证栈中元素有序==',
              '栈里存 `(天, 价格)`，价格从底到顶严格递减',
              '弹完后栈顶就是上一个更大元素，跨度 = 天数之差'],
        summary=['每个元素至多入栈出栈各一次 → 均摊 `O(1)`',
                 '哨兵 `(-1, inf)`：比所有价格都大，第 `-1` 天让跨度直接等于 `cur_day + 1`',
                 '易错：弹栈条件是 `>=`，相等的旧价格也要弹掉',
                 '易错：返回时栈顶是今天自己，要用 `stack[-2]`'],
    ),
)
