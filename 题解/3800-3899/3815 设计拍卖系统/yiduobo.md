---
title: "3815. 设计拍卖系统"
aliases: ["yiduobo的每日leetcode 3815.设计拍卖系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1997030195908076642"
zhihu_id: "1997030195908076642"
zhihu_title: "yiduobo的每日leetcode 3815.设计拍卖系统"
question_id: "3815"
question: "设计拍卖系统"
problem_url: "https://leetcode.cn/problems/design-auction-system/"
difficulty: "Medium"
rating: 1854
created: "2026-01-22T00:58:31+08:00"
updated: "2026-01-22T00:58:36+08:00"
upvotes: 0
comments: 0
---

# 3815. 设计拍卖系统

> **[yiduobo的每日leetcode 3815.设计拍卖系统](https://zhuanlan.zhihu.com/p/1997030195908076642) · 知乎 · 2026-01-22 · 赞同 0**
> 力扣：[3815. 设计拍卖系统](https://leetcode.cn/problems/design-auction-system/) · Medium · 灵茶山艾府：[懒删除堆（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3815.设计拍卖系统

<https://leetcode.cn/problems/design-auction-system/description/>

现在要求设计一个拍卖系统，该系统可以实时管理来自多个用户的出价，每个出价都与一个userId、一个itemId和一个bidAmount关联。

具体来说，需要实现AuctionSystem类，包括：

- AuctionSystem()：初始化AuctionSystem对象
- void addBid(int userId, int itemid, int bidAmount)：为itemId添加userId的一条新的出价，金额为bidAmount。若同一个userId已经对itemId出过价了，就用新的bidAmount替换原有出价。
- void updateBid(int userId, int itemId, int newAmount)：将userId对itemId的已有出价更新为newAmount。题目保证此出价一定存在。
- void removeBid(int userId, int itemId)：移除userId对itemId的出价。题目保证此出价一定存在。
- int getHightestBidder(int itemId)：返回对itemId的出价最高的用户userId。如果有多个用户的出价相同且最高，则返回userId较大的用户。若该商品没有出价，则返回-1。

如果抛开最后取最高价用户id的操作不看，实际上就只需要为每个item记录每个出价的用户以及对应的价格就行了，因此在这里可以使用一个嵌套的哈希表来储存：外层哈希表的key为itemId，value为内层哈希表；内层哈希表的key为userId，value为最新的出价。这样一来，就可以通过修改哈希表中储存的值来完成addBid、updateBid以及removeBid操作了。

而对于寻找出价最高的用户id的操作，则可以为每种item都维护一个堆，储存当前每个用户的出价。由于python原生的堆不好进行删除操作，因此在可以采用懒删除的策略，当价格变化时，并不即时从堆中删去原来的价格，而是等到查询时，判断堆顶对应的用户和价格是否和当前哈希表中记录的一致，若不一致，再执行删除。

最后附上python代码：

```python
class AuctionSystem(object):

    def __init__(self):
        self.amount = {}
        self.ma = {}

    def addBid(self, userId, itemId, bidAmount):
        """
        :type userId: int
        :type itemId: int
        :type bidAmount: int
        :rtype: None
        """
        
        if itemId not in self.amount:
            self.amount[itemId] = {}
            self.ma[itemId] = []
        
        self.amount[itemId][userId] = bidAmount
        heapq.heappush(self.ma[itemId], (-bidAmount, -userId))

    def updateBid(self, userId, itemId, newAmount):
        """
        :type userId: int
        :type itemId: int
        :type newAmount: int
        :rtype: None
        """
        self.addBid(userId, itemId, newAmount)

    def removeBid(self, userId, itemId):
        """
        :type userId: int
        :type itemId: int
        :rtype: None
        """
        self.amount[itemId].pop(userId)

    def getHighestBidder(self, itemId):
        """
        :type itemId: int
        :rtype: int
        """
        if itemId not in self.ma:
            return -1
        
        while self.ma[itemId] and self.amount[itemId].get(-self.ma[itemId][0][1], None) != -self.ma[itemId][0][0]:
            heapq.heappop(self.ma[itemId])
        
        if self.ma[itemId]:
            return -self.ma[itemId][0][1]
        
        return -1

# Your AuctionSystem object will be instantiated and called as such:
# obj = AuctionSystem()
# obj.addBid(userId,itemId,bidAmount)
# obj.updateBid(userId,itemId,newAmount)
# obj.removeBid(userId,itemId)
# param_4 = obj.getHighestBidder(itemId)
```
