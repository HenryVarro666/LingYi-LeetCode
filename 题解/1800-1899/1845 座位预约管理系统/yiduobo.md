---
title: "1845. 座位预约管理系统"
aliases: ["yiduobo的每日leetcode 1845.座位预约管理系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469915601"
zhihu_id: "469915601"
zhihu_title: "yiduobo的每日leetcode 1845.座位预约管理系统"
question_id: "1845"
question: "座位预约管理系统"
problem_url: "https://leetcode.cn/problems/seat-reservation-manager/"
difficulty: "Medium"
rating: 1429
created: "2022-02-20T19:30:41+08:00"
updated: "2022-02-20T19:30:41+08:00"
upvotes: 0
comments: 0
---

# 1845. 座位预约管理系统

> **[yiduobo的每日leetcode 1845.座位预约管理系统](https://zhuanlan.zhihu.com/p/469915601) · 知乎 · 2022-02-20 · 赞同 0**
> 力扣：[1845. 座位预约管理系统](https://leetcode.cn/problems/seat-reservation-manager/) · Medium · 灵茶山艾府：[两种方法：维护可预约的座位/维护取消预约的座位（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1845.作为预约管理系统

[力扣](https://leetcode-cn.com/problems/seat-reservation-manager/)

非常直观的使用堆的题目，题目中的三种操作分别对应了建堆、弹出堆顶和入堆三种操作，用兴趣的话可以手动实现，我在这里直接使用了python的heapq。

最后附上python代码：

```python
class SeatManager(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.heap = range(1, n + 1)

    def reserve(self):
        """
        :rtype: int
        """
        return heapq.heappop(self.heap)

    def unreserve(self, seatNumber):
        """
        :type seatNumber: int
        :rtype: None
        """
        heapq.heappush(self.heap, seatNumber)

# Your SeatManager object will be instantiated and called as such:
# obj = SeatManager(n)
# param_1 = obj.reserve()
# obj.unreserve(seatNumber)
```
