---
title: "3829. 设计共享出行系统"
aliases: ["yiduobo的每日leetcode 3829.设计共享出行系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/queue", "leetcode/hash-table", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2002215133578012622"
zhihu_id: "2002215133578012622"
zhihu_title: "yiduobo的每日leetcode 3829.设计共享出行系统"
question_id: "3829"
question: "设计共享出行系统"
problem_url: "https://leetcode.cn/problems/design-ride-sharing-system/"
difficulty: "Medium"
rating: 1594
created: "2026-02-05T02:58:15+08:00"
updated: "2026-02-05T02:58:21+08:00"
upvotes: 1
comments: 0
---

# 3829. 设计共享出行系统

> **[yiduobo的每日leetcode 3829.设计共享出行系统](https://zhuanlan.zhihu.com/p/2002215133578012622) · 知乎 · 2026-02-05 · 赞同 1**
> 力扣：[3829. 设计共享出行系统](https://leetcode.cn/problems/design-ride-sharing-system/) · Medium · 灵茶山艾府：[队列模拟，均摊 O(1) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3829.设计共享出行系统

<https://leetcode.cn/problems/design-ride-sharing-system/description/>

题目要求设计一个共享出行系统，来管理乘客的叫车请求以及司机的空闲状态。

乘客发出叫车请求，司机在系统中陆续变为可用状态。

系统需要根据乘客以及司机到达的顺序进行匹配。

要求实现RideSharingSystem类：

- RideSharingSystem()：初始化系统
- void addRider(int riderId)：添加id为riderId的新乘客。题目保证riderId在乘客中唯一，且仅被添加一次。
- void addDriver(int driverId)：添加id为driverId的新司机。题目保证driverId在司机中唯一，且仅被添加一次。
- int[] matchDriverWithRider()：匹配最早到达的空闲司机，以及最早等待的乘客，并将这二者从系统中移除。返回一个大小为2的整数数组result \= [driverId, riderId]，表示匹配的司机与乘客。若没有可用的匹配，返回[-1, -1]。
- void cancelRider(int riderId)：取消riderId的乘客的叫车请求，前提是该乘客存在，且还没有被匹配。

由于题目中的匹配是先到先匹配的，因此很自然想到使用两个队列drivers和riders分别储存空闲司机以及等待的乘客。当新的司机或者乘客被添加时，分别加入到对应的队列末尾即可。

由于还存在取消操作，而实时从队列中进行删除的时间复杂度较高，因此在这里可以采用懒删除的策略，使用一个集合waiting记录哪些乘客还存在于队列中。当取消的请求过来时，先检测其是否存在于waiting中，若存在，则将其从waiting中弹出，否则无需进行任何操作。

另一方面，对于匹配操作，首先需要检测riders队首的乘客是否在waiting中，若不在，说明订单取消了，此时应该将其从riders中弹出。重复此过程直到riders为空，或者队首的乘客依然在waiting中。

接下来，若riders以及drivers都非空，就将两个队列的队首进行匹配，并将这个乘客从waiting中删去，然后返回匹配的id对；若有至少一个为空，说明无法匹配，此时应该返回[-1, -1]。

最后附上python代码：

```python
class RideSharingSystem(object):

    def __init__(self):
        self.drivers = deque()
        self.riders = deque()
        self.waiting = set()

    def addRider(self, riderId):
        """
        :type riderId: int
        :rtype: None
        """
        self.riders.append(riderId)
        self.waiting.add(riderId)

    def addDriver(self, driverId):
        """
        :type driverId: int
        :rtype: None
        """
        self.drivers.append(driverId)

    def matchDriverWithRider(self):
        """
        :rtype: List[int]
        """
        if not self.drivers:
            return [-1, -1]
        
        while self.riders and self.riders[0] not in self.waiting:
            self.riders.popleft()
        
        if not self.riders:
            return [-1, -1]
        
        res = [self.drivers[0], self.riders[0]]
        self.drivers.popleft()
        self.riders.popleft()
        self.waiting.remove(res[1])
        return res

    def cancelRider(self, riderId):
        """
        :type riderId: int
        :rtype: None
        """
        if riderId in self.waiting:
            self.waiting.remove(riderId)

# Your RideSharingSystem object will be instantiated and called as such:
# obj = RideSharingSystem()
# obj.addRider(riderId)
# obj.addDriver(driverId)
# param_3 = obj.matchDriverWithRider()
# obj.cancelRider(riderId)
```
