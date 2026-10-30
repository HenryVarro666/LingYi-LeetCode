PRICES = [1, 3, 5, 4, 2, 6]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    p = S.get('prices') or PRICES
    n = len(p)
    cv.text((x0 + 18, y0 + 4), 'prices（绿箭头 = 赚到的上涨差价，灰箭头 = 下跌不操作）', 22, T['muted'], bold=True)
    cell = min(130, (x1 - x0 - 80) / n)
    sx = x0 + 40 + ((x1 - x0 - 80) - cell * n) / 2
    base, top = y1 - 70, y0 + 90
    scale = (base - top) / max(p)
    idx = S.get('index')
    ln = S.get('_line')
    done = 0 if idx is None else (idx + 1 if ln == 9 or (ln == 8 and not (p[idx] > p[idx - 1])) else idx)
    if ln == 11:
        done = n
    for k, v in enumerate(p):
        X = sx + k * cell
        bw = cell * 0.5
        cur = idx is not None and ln in (7, 8, 9) and k in (idx, idx - 1)
        fill = T['orange'] if cur else (110, 120, 132)
        cv.rect((X + (cell - bw) / 2, base - v * scale, X + (cell + bw) / 2, base), fill=fill, r=5)
        cv.text((X + cell / 2, base - v * scale - 6), v, 28, T['text'], anchor='mb', bold=True)
        cv.text((X + cell / 2, base + 8), k, 20, T['dim'], anchor='mt', mono=True)
    for k in range(1, done):
        a, b = p[k - 1], p[k]
        xa, xb = sx + (k - 1) * cell + cell / 2, sx + k * cell + cell / 2
        ya, yb = base - a * scale - 40, base - b * scale - 40
        up = b > a
        c = T['green'] if up else T['dim']
        cv.arrow((xa + 14, ya), (xb - 14, yb), c, 4 if up else 3, 14)
        if up:
            cv.text(((xa + xb) / 2 - 10, (ya + yb) / 2 - 8), f'+{b - a}', 26, T['green'], anchor='rb', bold=True)
    if idx is not None and ln in (8, 9):
        k = idx
        xa, xb = sx + (k - 1) * cell + cell / 2, sx + k * cell + cell / 2
        cv.text(((xa + xb) / 2, y0 + 52), f'比较第 {k - 1} 天和第 {k} 天', 24, T['orange'], anchor='mm', bold=True)


def _cap_if(S, B, ret):
    i, p = S.index, S.prices
    if p[i] > p[i - 1]:
        return f'`prices[{i}] = {p[i]} > prices[{i - 1}] = {p[i - 1]}`：上涨 → ==第 {i - 1} 天买、第 {i} 天卖=='
    return f'`prices[{i}] = {p[i]} ≤ prices[{i - 1}] = {p[i - 1]}`：下跌或持平 → ==什么都不做=='


CONFIG = dict(
    num=122, title='买卖股票的最佳时机 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='贪心：赚下所有上涨日的差价',
    tags=['热题173', '面试经典150'],
    code='''
class Solution(object):
    def maxProfit(self, prices):
        ans = 0
        if not prices:
            return 0

        for index in range(1, len(prices)):
            if prices[index] > prices[index - 1]:
                ans += prices[index] - prices[index - 1]

        return ans
''',
    call=f'Solution().maxProfit({PRICES})',
    expect=8,
    views=[
        dict(type='custom', draw=_draw, h=520),
        dict(type='text', fn=lambda S: (f"连续上涨 `1 → 3 → 5`：`(3 − 1) + (5 − 3)` = `5 − 1` = 4，和「1 买 5 卖」一样"
                                        if S.get('_line') == 11 else ''), size=26, h=60),
    ],
    watch=[('index', 'index', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计利润',
        'if not prices': '`prices` 非空，继续',
        'for index in range': lambda S, B, ret: (f'看第 `{S.index}` 天：和前一天比' if S.get('index') != B.get('index')
                                                 else '所有相邻两天都比较完了'),
        'if prices[index] > prices[index - 1]': _cap_if,
        'ans += prices[index]': '赚到差价 `{prices[index]} − {prices[index - 1]} = {prices[index] - prices[index - 1]}`，`ans` → =={ans}==',
        'return ans': '所有上涨段的差价之和 = =={ret}==',
    },
    cards=dict(
        one_liner='连续上涨拆成每天买卖，收益不变；下跌就不操作',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`prices[i]` 是第 `i` 天的股价，可以买卖==任意多次==',
                 '但手里最多只能持有一股（必须先卖再买），求最大利润',
                 '示例：`[7,1,5,3,6,4]` → `7`',
                 f'本视频：`{PRICES}` → `8`'],
        quote='若价格连续上涨……在k买进，在m卖出，收益为prices[m] - prices[k]；在k买进，在k + 1卖出，同时在k + 1买进……化简后依然是prices[m] - prices[k]。若价格连续下降，那么不应当进行操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['股价不变没有意义 → 只剩==连续上涨==和==连续下降==两种波动',
              '连续上涨：第一天买最后一天卖 = 每天买入第二天卖出，收益相同',
              '所以一趟扫描：`prices[k−1] < prices[k]` 就赚 `prices[k] − prices[k−1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '贪心的正确性：任何一笔交易的收益都能拆成若干相邻两天的差价之和',
                 '只累加正差价；持平和下跌都不操作',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用状态机 DP（持有 / 未持有），这套方法能推广到 123 / 188 / 309 / 714'],
    ),
)
