CONFIG = dict(
    num=3815, title='设计拍卖系统', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 + 懒删除堆',
    tags=['难度分 1854'],
    code='''
class AuctionSystem:
    def __init__(self):
        self.amount = {}  # (userId, itemId) -> bidAmount
        self.item_h = defaultdict(list)  # itemId -> [(bidAmount, userId)]

    def addBid(self, userId: int, itemId: int, bidAmount: int) -> None:
        self.amount[(userId, itemId)] = bidAmount
        heappush_max(self.item_h[itemId], (bidAmount, userId))

    def updateBid(self, userId: int, itemId: int, newAmount: int) -> None:
        self.addBid(userId, itemId, newAmount)
        # 堆中重复的元素在 getHighestBidder 中删除（懒更新）

    def removeBid(self, userId: int, itemId: int) -> None:
        # 题目保证 (userId, itemId) 在 self.amount 中，如果不保证的话，用下面这行代码
        # self.amount.pop((userId, itemId), None)
        del self.amount[(userId, itemId)]
        # 堆中元素在 getHighestBidder 中删除（懒删除）

    def getHighestBidder(self, itemId: int) -> int:
        h = self.item_h.get(itemId, None)
        while h:
            bidAmount, userId = h[0]
            if bidAmount == self.amount.get((userId, itemId), None):
                return userId
            # 货不对板，堆顶出价与实际出价不符
            heappop_max(h)
        return -1
''',
    setup='''
# Python 3.14 才自带 heappush_max / heappop_max；这里用 heapq 的内部函数补上（不被追踪）
def heappush_max(heap, item):
    heap.append(item)
    heapq._siftdown_max(heap, 0, len(heap) - 1)

def heappop_max(heap):
    last = heap.pop()
    if heap:
        top = heap[0]
        heap[0] = last
        heapq._siftup_max(heap, 0)
        return top
    return last
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
out''',
    expect=[2, 1, 2, -1],
    views=[
        dict(type='map', var='self.amount', label='amount（(用户, 商品) → 实际出价）', fmt=lambda k, v: f'u{k[0]}·商品{k[1]} → {v}', h=110),
        dict(type='heap', var='self.item_h[7]', label='商品 7 的最大堆（出价:用户）', fmt=lambda x: f'{x[0]}:u{x[1]}', top_color='orange', h=190),
    ],
    watch=[('userId', 'userId', 'blue'), ('itemId', 'itemId', 'pink'), ('bidAmount', 'bidAmount', 'orange')],
    skip=['self.item_h = defaultdict'],
    captions={
        'self.amount = {}': '`amount` 记录每个 (用户, 商品) ==当前真实==的出价',
        'self.addBid(userId, itemId, newAmount)': '更新 = 再出一次价：==新出价压进堆，旧的先不管==',
        'self.amount[(userId, itemId)] = bidAmount': '`addBid({userId}, {itemId}, {bidAmount})`：哈希表记下实际出价',
        'heappush_max': '压进该商品的最大堆（先比出价，再比用户编号，正好满足“同价取大编号”）',
        'del self.amount': '`removeBid`：只删哈希表；堆里的旧记录==不动==，等查询时懒删除',
        'h = self.item_h.get': '取出商品 `{itemId}` 的堆',
        'while h:': lambda S, B, r: ('堆里还有元素，看堆顶' if S.h else '堆空了 → 没有任何有效出价'),
        'bidAmount, userId = h[0]': '看堆顶：出价 `{bidAmount}`，用户 `{userId}`',
        'if bidAmount == self.amount.get': lambda S, B, r: (
            f'堆顶出价 `{S.bidAmount}` 与实际出价 `{S["self.amount"].get((S.userId, S.itemId))}`'
            + (' ==一致== → 它就是最高出价' if S.bidAmount == S['self.amount'].get((S.userId, S.itemId)) else ' ==不一致== → 货不对板')),
        'return userId': '返回最高出价的用户 =={ret}==',
        'heappop_max(h)': '堆顶是过期（被更新或删除）的出价 → 弹掉，继续看下一个',
        'return -1': lambda S, B, r: '没有出价，返回 `-1`',
    },
    max_steps=110,
    cards=dict(
        one_liner='堆里的旧出价不急着删，查到堆顶不对板再弹',
        complexity='addBid/updateBid `O(log q)`，removeBid `O(1)`，get 均摊 `O(log q)`',
        problem=['拍卖系统：`addBid`、`updateBid`、`removeBid`、`getHighestBidder(itemId)`',
                 '最高出价相同时返回==用户编号更大==的人；没有出价返回 `-1`',
                 '本视频：商品 7 上用户 1、2 出价，更新、删除后反复查最高者'],
        quote='对于 getHighestBidder，不断查看堆顶，如果堆顶出价与实际出价不符，那么弹出堆顶。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两样东西：哈希表存每个 (用户, 商品) 的实际出价；每个商品一个最大堆存历史出价',
              '更新、删除都只动哈希表（更新另外压一个新值），不去堆里找旧元素',
              '查询时核对堆顶与哈希表：不符就是过期数据，弹掉直到相符'],
        summary=['时间：add/update `O(log q)`，remove `O(1)`，查询均摊 `O(log q)`；空间 `O(q)`',
                 '堆元素 `(出价, 用户)` 的比较顺序正好是“出价高优先，同价用户大优先”',
                 '易错：同一用户先出价 5 后改成 8，堆里 `(5, u)` 与 `(8, u)` 都在，必须核对出价',
                 '写法二：有序集合也能做，但懒删除堆常数更小',
                 'heappush_max / heappop_max 是 Python 3.14 才有的，视频里用 heapq 内部函数补上'],
    ),
)
