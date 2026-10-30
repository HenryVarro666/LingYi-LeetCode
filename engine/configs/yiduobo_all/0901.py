PRICES = [100, 80, 60, 70, 60, 75, 85]
L_WHILE, L_POP, L_RES, L_APP, L_INC, L_RET = 8, 9, 11, 12, 13, 14


def _cur(S):
    c = S.get('self.cnt')
    if c is None or 'price' not in S:
        return None
    return c - 1 if S.get('_line') in (L_INC, L_RET) else c


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'price 序列（蓝 = 当前 p，紫 = 栈里可能成为答案的下标，灰 = 没有价值了）', 24, T['muted'], bold=True)
    n = len(PRICES)
    cur = _cur(S)
    st = S.get('self.stack') or []
    days = {d for _, d in st}
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
        cv.text((X + cell / 2, base + 8), f'下标{i}', 18, T['dim'], anchor='mt')
    cv.line([(x0 + 20, base), (x1 - 20, base)], T['border'], 2)
    if S.get('_line') in (L_RES, L_APP, L_INC, L_RET) and cur is not None and 'res' in S:
        q = cur - S['res']
        a = sx + (q + 1) * cell + 6
        b = sx + (cur + 1) * cell - 6
        y = base + 38
        cv.line([(a, y - 10), (a, y), (b, y), (b, y - 10)], T['green'], 3)
        cv.text(((a + b) / 2, y + 4), f'p - q = {S["res"]}', 22, T['green'], anchor='mt', bold=True)


def _fmt(x):
    p, d = x
    return f'{p}@{d}'


def _while(S, B, ret):
    top = S['self.stack'][-1]
    p = S.price
    if p >= top[0]:
        return f'栈顶 `{top[0]} ≤ price = {p}` → 下标 {top[1]} 被更近、不更小的 p 挡住，==以后不可能是答案=='
    return f'栈顶 `{top[0]} > price = {p}` → 下标 `q = {top[1]}` 就是==最近的更大值=='


CONFIG = dict(
    num=901, title='股票价格跨度', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 栈底放 100001 哨兵',
    tags=['labuladong', '灵神题单·单调栈', '难度分 1709'],
    code='''
class StockSpanner(object):

    def __init__(self):
        self.stack = [[100001, -1]]
        self.cnt = 0

    def next(self, price):
        while price >= self.stack[-1][0]:
            self.stack.pop()

        res = self.cnt - self.stack[-1][1]
        self.stack.append([price, self.cnt])
        self.cnt += 1
        return res
''',
    call=f'''s = StockSpanner()
ans = [s.next(p) for p in {PRICES}]
ans''',
    expect=[1, 1, 1, 2, 1, 4, 6],
    views=[
        dict(type='custom', draw=_draw, h=470),
        dict(type='stack', var='self.stack', label='self.stack（价格@下标）', fmt=_fmt, h=120),
    ],
    watch=[('price', 'price', 'blue'), ('cnt', 'self.cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'self.stack = [[': '栈底放 `[100001, -1]`：比所有价格都大，==不用再判断栈是否为空==',
        'self.cnt = 0': '`cnt` 记录当前输入的下标',
        'while price >=': _while,
        'self.stack.pop()': '弹出 `{B["self.stack"][-1]}`：==没有再存在的价值了==',
        'res = self.cnt': '答案 = 当前下标 − 栈顶下标 = `{self.cnt} − ({self.stack[-1][1]})` = =={res}==',
        'self.stack.append(': '把 `[{price}, {self.cnt}]` 压入栈中',
        'self.cnt += 1': '下标 +1 → `cnt = {self.cnt}`',
        'return res': '返回跨度 =={res}==：下标 `{self.cnt - res}` 到 `{self.cnt - 1}` 的价格都 ≤ `{price}`',
    },
    skip=['self.cnt += 1'],
    max_steps=80,
    cards=dict(
        one_liner='找 p 之前最近的 q 使 price[q] > price[p]，答案就是 p − q',
        complexity='均摊 `O(1)` / 次，空间 `O(n)`',
        problem=['每天输入一个股票价格 `price`，返回今天的==价格跨度==：',
                 '从今天往前数，连续 `≤ price` 的天数（含今天）',
                 '示例：`100,80,60,70,60,75,85` → `1,1,1,2,1,4,6`'],
        quote='对于输入的任意price[i]，若其后续出现了一个price[j]满足price[j] >= price[i]，那么price[i]就没有再存在的价值了，因此很自然想到使用一个单调栈。',
        quote_src='—— yiduobo 题解原文',
        idea=['反证：若 `i < j` 且 `price[i] ≤ price[j]`，q 取 i 就要求 `price[j] ≤ price[p] < price[i]`，==矛盾==',
              '所以 j 一出现，i 就可以出栈 → 栈中价格从底到顶递减',
              '弹完后：答案 = 当前下标 − 栈顶下标；再把 price 压栈'],
        summary=['每个价格至多入栈出栈各一次 → 均摊 `O(1)`',
                 '哨兵 `100001` 大于所有价格（题目 `price ≤ 10^5`），下标 `-1` 让答案自动等于 `cnt + 1`',
                 '先算 `res` 再压栈，所以用的是 `stack[-1]`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神栈元素是 `(天, 价格)`、哨兵用 `inf`，思路相同'],
    ),
)
