---
title: "2034. 股票价格波动"
aliases: ["yiduobo的每日leetcode 2034.股票价格波动"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508763942"
zhihu_id: "508763942"
zhihu_title: "yiduobo的每日leetcode 2034.股票价格波动"
question_id: "2034"
question: "股票价格波动"
problem_url: "https://leetcode.cn/problems/stock-price-fluctuation/"
created: "2022-05-03T15:19:58+08:00"
updated: "2022-05-03T15:19:58+08:00"
upvotes: 0
comments: 0
---

# 2034. 股票价格波动

> **[yiduobo的每日leetcode 2034.股票价格波动](https://zhuanlan.zhihu.com/p/508763942) · 知乎 · 2022-05-03 · 赞同 0**
> 力扣：[2034. 股票价格波动](https://leetcode.cn/problems/stock-price-fluctuation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2034.股票价格波动

[力扣](https://leetcode-cn.com/problems/stock-price-fluctuation/)

对于题目要求的几种操作分别进行讨论：

1、记录每一时刻的股票价格，并随时可能更新。对于这个操作直接使用dict记录每一时刻的价格即可

2、找出当前已知的时间戳最晚的股票的价格。对于这个操作需要使用一个变量来记录当前已知的最晚时间戳，然后对应的价格就可以通过操作1中的dict来查询

3、找出当前价格最高和最低的股票。由于存在更新操作，因此这是一个动态的最大值和最小值问题，可以使用两个堆来分别处理

另外在具体实现上，更新操作需要修改堆中某个元素的值，必须知道目标元素在堆中的位置，并在修改后进行对堆进行调整。一个更简便的做法是只将最新的价格加入到堆中，但不删去老的价格。当需要查询时，若此时堆中保留的价格与操作1中dict记录的价格不一致，说明堆中的价格过期了，此时再执行删除操作也不迟

最后附上python代码：

```python
class StockPrice(object):

    def __init__(self):
        self.num_dict = {}
        self.max_heap = []
        self.min_heap = []
        self.max_timestamp = 0

    def update(self, timestamp, price):
        """
        :type timestamp: int
        :type price: int
        :rtype: None
        """
        self.num_dict[timestamp] = price
        heapq.heappush(self.max_heap, [-price, timestamp])
        heapq.heappush(self.min_heap, [price, timestamp])
        self.max_timestamp = max(self.max_timestamp, timestamp)

    def current(self):
        """
        :rtype: int
        """
        return self.num_dict[self.max_timestamp]

    def maximum(self):
        """
        :rtype: int
        """
        p, t = heapq.heappop(self.max_heap)
        while -p != self.num_dict[t]:
            p, t = heapq.heappop(self.max_heap)
        
        heapq.heappush(self.max_heap, [p, t])
        return -p

    def minimum(self):
        """
        :rtype: int
        """
        p, t = heapq.heappop(self.min_heap)
        while p != self.num_dict[t]:
            p, t = heapq.heappop(self.min_heap)
        
        heapq.heappush(self.min_heap, [p, t])
        return p

# Your StockPrice object will be instantiated and called as such:
# obj = StockPrice()
# obj.update(timestamp,price)
# param_2 = obj.current()
# param_3 = obj.maximum()
# param_4 = obj.minimum()
```
