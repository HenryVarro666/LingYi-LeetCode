CONFIG = dict(
    num=3815, title='设计拍卖系统', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='嵌套哈希表 + 每商品一个堆（懒删除）',
    tags=['难度分 1854'],
    code='''
class AuctionSystem(object):

    def __init__(self):
        self.amount = {}
        self.ma = {}

    def addBid(self, userId, itemId, bidAmount):
        
        if itemId not in self.amount:
            self.amount[itemId] = {}
            self.ma[itemId] = []
        
        self.amount[itemId][userId] = bidAmount
        heapq.heappush(self.ma[itemId], (-bidAmount, -userId))

    def updateBid(self, userId, itemId, newAmount):
        self.addBid(userId, itemId, newAmount)

    def removeBid(self, userId, itemId):
        self.amount[itemId].pop(userId)

    def getHighestBidder(self, itemId):
        if itemId not in self.ma:
            return -1
        
        while self.ma[itemId] and self.amount[itemId].get(-self.ma[itemId][0][1], None) != -self.ma[itemId][0][0]:
            heapq.heappop(self.ma[itemId])
        
        if self.ma[itemId]:
            return -self.ma[itemId][0][1]
        
        return -1
''',
    call='''a = AuctionSystem()
out = []
a.addBid(1, 7, 5)
a.addBid(2, 7, 6)
out.append(a.getHighestBidder(7))
a.updateBid(1, 7, 8)
out.append(a.getHighestBidder(7))
a.removeBid(1, 7)
out.append(a.getHighestBidder(7))
a.removeBid(2, 7)
out.append(a.getHighestBidder(7))
out.append(a.getHighestBidder(3))
out''',
    expect=[2, 1, 2, -1, -1],
    views=[
        dict(type='map', var='self.amount', label='amount（商品 → {用户: 当前出价}）', fmt=lambda k, v: f'商品{k} → {dict(v)}', h=110),
        dict(type='heap', var='self.ma[7]', label='商品 7 的最小堆（存 (-出价, -用户)）', fmt=lambda x: f'{-x[0]}:u{-x[1]}', top_color='orange', h=190),
    ],
    watch=[('userId', 'userId', 'blue'), ('itemId', 'itemId', 'pink'), ('bidAmount', 'bidAmount', 'orange')],
    skip=['self.ma = {}'],
    captions={
        'self.amount = {}': '外层哈希表：商品 → 内层哈希表（用户 → ==最新==出价）',
        'if itemId not in self.amount': lambda S, B, r: (
            f'`addBid`：商品 {S.itemId} 还没人出过价 → 先建内层表和空堆' if S.itemId not in S['self.amount']
            else f'`addBid`：商品 {S.itemId} 已经有记录，直接写入'),
        'self.amount[itemId][userId] = bidAmount': '内层表里写入 用户 `{userId}` 的出价 `{bidAmount}`（同用户会覆盖）',
        'heapq.heappush': '堆里存 `(-出价, -用户)`：最小堆的堆顶 = ==出价最高，同价用户最大==；旧出价留在堆里',
        'self.addBid(userId, itemId, newAmount)': '更新出价和新增出价做一样的事：覆盖哈希表、再压一条新的',
        'self.amount[itemId].pop(userId)': '`removeBid`：只从内层表删掉用户 `{userId}`，堆里的记录==不动==',
        'if itemId not in self.ma': lambda S, B, r: ('这个商品从没人出价 → 直接返回 `-1`' if S.itemId not in S['self.ma']
                                                      else f'商品 {S.itemId} 有出价记录，去堆里找最高者'),
        'while self.ma[itemId] and': lambda S, B, r: (
            '堆空了，停止清理' if not S['self.ma'][S.itemId] else
            (lambda t: f'堆顶是用户 `{-t[1]}`、出价 `{-t[0]}`；哈希表里他的出价是 `{S["self.amount"][S.itemId].get(-t[1])}` → '
                       + ('==不一致==，过期，弹掉' if S['self.amount'][S.itemId].get(-t[1]) != -t[0] else '一致，停止清理'))(S['self.ma'][S.itemId][0])),
        'heapq.heappop(self.ma[itemId])': '弹掉过期的堆顶（被更新或删除的旧出价）',
        'if self.ma[itemId]:': lambda S, B, r: ('堆里还有有效出价' if S['self.ma'][S.itemId] else '堆被清空，没有有效出价'),
        'return -self.ma[itemId][0][1]': '堆顶的 `-用户` 取负 → 最高出价者 =={ret}==',
        'return -1': '没有出价，返回 `-1`',
    },
    max_steps=110,
    cards=dict(
        one_liner='用嵌套哈希表存真实出价，堆里的旧价等查询时再清',
        complexity='add/update `O(log q)`，remove `O(1)`，get 均摊 `O(log q)`',
        problem=['管理多位用户对多个商品的出价：加价、更新、撤价、查最高者',
                 '同一用户重复出价就==替换==；最高价并列时取 userId 大的；没出价返回 `-1`',
                 '本视频：商品 7 上用户 1、2 出价，更新、撤价后反复查询'],
        quote='由于python原生的堆不好进行删除操作，因此在可以采用懒删除的策略，当价格变化时，并不即时从堆中删去原来的价格，而是等到查询时，判断堆顶对应的用户和价格是否和当前哈希表中记录的一致，若不一致，再执行删除。',
        quote_src='—— yiduobo 题解原文',
        idea=['先不看“最高者”：嵌套哈希表（商品 → 用户 → 出价）就能完成加、改、删',
              '最高者：每个商品一个堆，Python 只有最小堆，所以存 `(-出价, -用户)`',
              '查询时核对堆顶与哈希表，不一致就弹掉，直到堆顶有效'],
        summary=['时间：add/update `O(log q)`，remove `O(1)`，查询均摊 `O(log q)`；空间 `O(q)`',
                 '取负数同时处理了“出价高优先”和“同价用户大优先”两条规则',
                 '易错：商品从没出价过时 `self.ma` 里没有这个 key，要先判断再取',
                 '原文为 Python 2 风格写法，在 Python 3 中可直接运行，未改动代码',
                 '对比灵神：灵神用 `(商品,用户)` 元组做键的单个哈希表，yiduobo 用嵌套哈希表'],
    ),
)
