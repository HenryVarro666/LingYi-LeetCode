def _prices(S):
    pl = S.get('self.price_list')
    if pl is None:
        return {}
    return {p: v for p, v in enumerate(pl) if v}


def _tag(S):
    if 'self.cnt' not in S:
        return '价目表：商品编号 → 单价；顾客计数 `cnt` 到 `n` 就打折'
    cnt, n = S['self.cnt'], S['self.n']
    if 'product' in S and 'res' in S:
        return f'本次账单累计 `res = {S["res"]}`；已服务 `cnt = {cnt}` 位，第 `{n}` 位享折扣'
    return f'已服务 `cnt = {cnt}` 位，第 `{n}` 位享折扣'


CONFIG = dict(
    num=1357, title='每隔n个顾客打折', difficulty='Medium', category='设计',
    author='yiduobo', technique='价目表 + 顾客计数器',
    tags=[],
    code='''
class Cashier(object):

    def __init__(self, n, discount, products, prices):

        l = len(products)
        self.price_list = [0] * 201
        for index in range(l):
            self.price_list[products[index]] = prices[index]
        self.cnt = 0
        self.discount = discount
        self.n = n

    def getBill(self, product, amount):
        
        res = 0
        for index in range(len(product)):
            res += self.price_list[product[index]] * amount[index]
        
        self.cnt += 1
        if self.cnt == self.n:
            res *= 1 - self.discount * 1.0 / 100
            self.cnt = 0
        
        return res
''',
    call='''c = Cashier(3, 50, [1, 2, 3, 7], [100, 200, 300, 400])
out = []
out.append(c.getBill([1, 2], [1, 2]))
out.append(c.getBill([3, 7], [1, 1]))
out.append(c.getBill([1, 2, 3], [1, 1, 1]))
out''',
    expect=[500, 700, 300.0],
    views=[
        dict(type='text', fn=_tag, h=60),
        dict(type='map', var=_prices, label='价目表 price_list（只显示有价格的商品）', fmt=lambda k, v: f'{k} → {v}', h=150),
        dict(type='array', var='product', label='本单商品 product', pointers={'index': 'blue'}, h=130),
        dict(type='array', var='amount', label='数量 amount', pointers={'index': 'blue'}, h=130),
        dict(type='calls', label='正在执行', h=100),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green'), ('cnt', 'self.cnt', 'yellow'), ('n', 'self.n', 'pink')],
    skip=['self.discount = discount', 'self.n = n'],
    captions={
        'l = len(products)': '一共 `{l}` 种商品要登记价格',
        'self.price_list = [0] * 201': '商品编号 ≤ 200：开长度 201 的数组，`price_list[编号]` = 单价',
        'self.price_list[products[index]] = prices[index]': '商品 `{products[index]}` 的单价记为 `{prices[index]}`',
        9: '`cnt` 记录当前折扣周期内已经结账了几位顾客',
        'res = 0': '新账单，`res` 从 0 开始',
        'for index in range(len(product))': lambda S, B, r: ('所有商品都算完了' if 'index' in B and B['index'] == S['index']
                                                             else f'第 `{S.index}` 件：商品 `{S.product[S.index]}`，数量 `{S.amount[S.index]}`'),
        'res += self.price_list': '`res += {self.price_list[product[index]]} × {amount[index]}` → =={res}==',
        'self.cnt += 1': '又服务了一位顾客：`cnt` = {self.cnt}',
        'if self.cnt == self.n': lambda S, B, r: (f'`cnt = {S["self.cnt"]} == n = {S["self.n"]}`：这是第 n 位顾客，==要打折==' if S['self.cnt'] == S['self.n']
                                                  else f'`cnt = {S["self.cnt"]} ≠ n = {S["self.n"]}`：还没轮到打折'),
        'res *= 1 - self.discount': '打折：`res` 乘 `1 − {self.discount}/100` → =={res}==',
        22: '折扣已给出，计数器 ==重置为 0==，重新数 n 位',
        'return res': '本单应付 =={ret}==',
    },
    cards=dict(
        one_liner='先记价目表，再数顾客：每到第 n 位就打折并清零',
        complexity='构造 `O(P)`；`getBill` 每次 `O(商品种数)`',
        problem=['超市有一个折扣活动：==每 n 位顾客==，第 n 位的账单打 `discount`% 的折扣',
                 '`getBill(product, amount)`：返回本单应付金额',
                 '例：`n=3, discount=50`，第 3 位顾客 `[1,2,3]` 各一件 = 600，打折后 `300.0`'],
        quote='按照题目意思计算每个顾客的花销，并统计当前是第几个顾客。每到第n个顾客时，并打折然后重置计数器。',
        quote_src='—— yiduobo 题解原文',
        idea=['编号 ≤ 200，直接用定长数组做价目表，`O(1)` 查单价',
              '`getBill`：逐件累加 `单价 × 数量`',
              '`cnt` 加一；等于 `n` 就把总价乘 `1 − discount/100` 并清零'],
        summary=['易错：打折后要把 `cnt` 清零，重新数 n 位',
                 '折扣系数是 `1 − discount/100`，不是 `discount/100`',
                 '返回浮点数，如 `300.0`；未打折时是整数'],
    ),
)
