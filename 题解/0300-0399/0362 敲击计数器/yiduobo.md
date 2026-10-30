---
title: "362. 敲击计数器"
aliases: ["yiduobo的每日leetcode 362.敲击计数器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/598114936"
zhihu_id: "598114936"
zhihu_title: "yiduobo的每日leetcode 362.敲击计数器"
question_id: "362"
question: "敲击计数器"
problem_url: "https://leetcode.cn/problems/design-hit-counter/"
created: "2023-01-10T23:02:15+08:00"
updated: "2023-01-10T23:02:15+08:00"
upvotes: 0
comments: 0
---

# 362. 敲击计数器

> **[yiduobo的每日leetcode 362.敲击计数器](https://zhuanlan.zhihu.com/p/598114936) · 知乎 · 2023-01-10 · 赞同 0**
> 力扣：[362. 敲击计数器](https://leetcode.cn/problems/design-hit-counter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

362.敲击计数器

[力扣](https://leetcode.cn/problems/design-hit-counter/)

依然是利用队列维护数据流的问题。对于每次hit或getHits操作，首先都需要根据当前时间戳，将队列中所有五分钟之前的敲击从队列中弹出。若当前是hit操作，那么还需要将当前的时间戳加入到队列中，否则直接返回队列长度就行了。

另外，对于题目最后提出的进阶问题，则可以额外使用一个哈希表统计各个时刻的敲击次数。当一次hit到来时，需要先检测当前时间戳是否出现在哈希表中。如果已经出现，那么将对应的敲击次数加1，否则就按照上面的算法先将过期的敲击从队列和哈希表中移除，然后再将当前敲击加入到队列和哈希表中。

最后附上python代码：

```python
class HitCounter(object):

    def __init__(self):
        self.q = deque()
        self.s = 0

    def hit(self, timestamp):
        """
        :type timestamp: int
        :rtype: None
        """
        while self.s > 0:
            first = self.q.popleft()
            if timestamp - first < 300:
                self.q.appendleft(first)
                break
            else:
                self.s -= 1
        
        self.q.append(timestamp)
        self.s += 1

    def getHits(self, timestamp):
        """
        :type timestamp: int
        :rtype: int
        """
        while self.s > 0:
            first = self.q.popleft()
            if timestamp - first < 300:
                self.q.appendleft(first)
                break
            else:
                self.s -= 1

        return self.s

# Your HitCounter object will be instantiated and called as such:
# obj = HitCounter()
# obj.hit(timestamp)
# param_2 = obj.getHits(timestamp)
```
