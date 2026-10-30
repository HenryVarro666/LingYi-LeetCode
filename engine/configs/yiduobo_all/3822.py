CONFIG = dict(
    num=3822, title='设计订单管理系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='数组存订单 · 遍历查找',
    tags=[],
    code='''
class OrderManagementSystem(object):

    def __init__(self):
        self.orders = []

    def addOrder(self, orderId, orderType, price):
        self.orders.append([orderId, orderType, price])

    def modifyOrder(self, orderId, newPrice):
        for index in range(len(self.orders)):
            if self.orders[index][0] == orderId:
                self.orders[index][2] = newPrice
                break

    def cancelOrder(self, orderId):
        for index in range(len(self.orders)):
            if self.orders[index][0] == orderId:
                break
        self.orders.pop(index)

    def getOrdersAtPrice(self, orderType, price):
        res = []
        for index in range(len(self.orders)):
            if self.orders[index][1] == orderType and self.orders[index][2] == price:
                res.append(self.orders[index][0])
        
        return res
''',
    call="""oms = OrderManagementSystem()
out = []
oms.addOrder(1, 'buy', 10)
oms.addOrder(2, 'sell', 12)
oms.addOrder(3, 'buy', 10)
oms.modifyOrder(2, 10)
oms.cancelOrder(1)
out.append(oms.getOrdersAtPrice('buy', 10))
out.append(oms.getOrdersAtPrice('sell', 10))
out""",
    expect=[[3], [2]],
    views=[
        dict(type='table', var='self.orders', label='self.orders（每行 [orderId, orderType, price]）',
             cols=['id', 'type', '价格'], h=420),
    ],
    watch=['orderId', 'orderType', 'price', 'newPrice', 'index', ('res', 'res', 'green')],
    captions={
        'self.orders = []': '用一个数组 `orders` 记录所有订单，操作不超过 2000 次，`O(n)` 查找足够',
        'self.orders.append': '新订单 `{[orderId, orderType, price]}` 加到 `orders` 末尾',
        'for index in range(len(self.orders))': '从头遍历 `orders`，逐个看订单号',
        'if self.orders[index][0] == orderId': lambda S, B, r: (f"`orders[{S.index}][0] = {S.self.orders[S.index][0]}` 就是要找的 `{S.orderId}` → ==找到=="
                                                              if S.self.orders[S.index][0] == S.orderId
                                                              else f"`orders[{S.index}][0] = {S.self.orders[S.index][0]}` ≠ `{S.orderId}` → 继续往后找"),
        'self.orders[index][2] = newPrice': '订单 `{orderId}` 的价格改成 `{newPrice}`',
        'break': '已找到，不用再扫了',
        'self.orders.pop(index)': '题目保证订单存在，循环 break 时 `index` 就是它的位置 → ==pop 掉== 即取消',
        'res = []': '`res` 收集满足条件的订单号',
        'if self.orders[index][1] == orderType': lambda S, B, r: (f"类型 `{S.self.orders[S.index][1]}`、价格 `{S.self.orders[S.index][2]}`，要找 `{S.orderType}`、`{S.price}` → "
                                                                  + ('==匹配==' if S.self.orders[S.index][1] == S.orderType and S.self.orders[S.index][2] == S.price else '不匹配')),
        'res.append': '符合条件，订单号加入 `res` → `{res}`',
        'return res': '返回匹配的订单号 `{res}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='数据量小，一个数组 + 线性扫描就够了',
        complexity='每次操作 `O(n)`，空间 `O(n)`',
        problem=['设计订单系统：`addOrder` 加单、`modifyOrder` 改价、`cancelOrder` 撤单',
                 '`getOrdersAtPrice(type, price)` 返回类型和价格都匹配的订单号',
                 '本视频：加 3 单 → 改价 → 撤单 → 查询两次'],
        quote='由于题目保证所有操作的次数不超过2000次，因此在这里使用一个O(n^2)的算法就足够了，于是只需使用一个数组orders记录所有的订单。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个订单存成 `[orderId, orderType, price]`，放进数组 `orders`',
              '改价 / 撤单：遍历找到 `orderId`，改价格或 `pop`',
              '查询：遍历一遍，类型和价格都相等的订单号收进答案'],
        summary=['每次操作 `O(n)`，总共不超过 2000 次，不会超时',
                 '撤单直接 `pop`，所以 `orders` 里的订单都是有效的',
                 '易错：查询要同时比较类型和价格；不存在时返回空列表',
                 '原文为 Python 2 风格 `class ...(object)`，Python 3 照常运行，代码未改',
                 '想更快可用「订单号 → 订单」哈希表，但本题数据量不必要'],
    ),
)
