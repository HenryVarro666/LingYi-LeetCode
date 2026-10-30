---
title: "4080. 设计公交车座位预订系统"
aliases: ["yiduobo的每日leetcode 4080.设计公交车座位预订系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2094182990456828126"
zhihu_id: "2094182990456828126"
zhihu_title: "yiduobo的每日leetcode 4080.设计公交车座位预订系统"
question_id: "4080"
question: "设计公交车座位预订系统"
problem_url: "https://leetcode.cn/problems/design-bus-seat-booking-system/"
created: "2026-10-15T22:50:38+08:00"
updated: "2026-10-15T22:50:58+08:00"
upvotes: 1
comments: 0
---

# 4080. 设计公交车座位预订系统

> **[yiduobo的每日leetcode 4080.设计公交车座位预订系统](https://zhuanlan.zhihu.com/p/2094182990456828126) · 知乎 · 2026-10-15 · 赞同 1**
> 力扣：[4080. 设计公交车座位预订系统](https://leetcode.cn/problems/design-bus-seat-booking-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4080.设计公交车座位预定系统

<https://leetcode.cn/problems/design-bus-seat-booking-system/description/>

题目要求设计一个公交车座位预订系统。

公交车一共有n排座位，每一排有4个座位，分别标记为'A'、'B'、'C'、'D'。

座位'A'和'D'靠窗，'B'和'C'则靠过道，其中'A'和'B'相邻，'C'和'D'相邻。

如果计划预定一个靠过道的位置，那么只需要1秒。如果预订的是靠窗的位置，那么若与其相邻的靠过道的位置还没有被预定，那么就需要1秒，反之如果相邻的靠过道已经被预定，那么就需要3秒。

一个座位由形如'A1'或者'D20'的字符串表示，即一个从'A'到'D'的字母，后面跟着所在的排号。

要求实现BusBooking类：

- BusBooking(int n)：使用n排空座位初始化系统
- void toggle(string seat)：如果seat还没有被预订，那么就预订这个座位，否则释放这个座位
- int getTotalTime()：返回目前预订的座位所需的总时间，预订的顺序按照这些座位对应的toggle调用顺序。如果当前没有已经预订的座位，则返回0
- int getMinTime()：返回预订当前所有已预订作为所需的最小总时间，可以任意调整预定的顺序。如果没有已经预订的座位，则返回0

需要注意，一个座位的时间开销在其被预订时确定，之后预订或释放其他座位都不影响已预订座位的时间开销。

对于题目中的几种操作：

- 预订座位：必须记录哪些座位已经预订了，哪些还没有预订，并且可以高效修改这个状态
- 返回总时间：必须记录目前已经预订的座位分别花费的时间
- 返回最小总时间：由于可以任意调整顺序，那么就可以先预定靠窗座位，再预定靠过道座位，因此每个座位所需的事件都是1，所需的最小总时间就是目前已经预订座位的数量

综合起来，在这里就只需要使用一个哈希表booked，key是目前已经预订的座位标号，value是花费的时间。同时还需要使用一个变量total记录预订所有座位花费的总时间。那么对于每种操作：

- 预订座位：若seat在booked中出现过，那么就将total减去之前预订该座位需要的事件booked[seat]，然后将其从booked中弹出。反之，则判断其相邻的座位是否为过道且已经被预订了，如果是，那么此次预订的代价t就是3，否则就是1，然后将t累加到total，并将{seat: t}加入到booked中
- 返回总时间：直接返回total即可
- 返回最小总时间：直接返回booked的大小即可

最后附上python代码：

```python
class BusBooking(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.booked = {}
        self.total = 0

    def toggle(self, seat):
        """
        :type seat: str
        :rtype: None
        """

        if seat in self.booked:
            self.total -= self.booked[seat]
            self.booked.pop(seat)
            return

        p = seat[0]
        if (p == 'A' and 'B' + seat[1:] in self.booked) or (p == 'D' and 'C' + seat[1:] in self.booked):
            t = 3
        else:
            t = 1
        
        self.booked[seat] = t
        self.total += t

    def getTotalTime(self):
        """
        :rtype: int
        """
        return self.total

    def getMinTime(self):
        """
        :rtype: int
        """
        return len(self.booked)

# Your BusBooking object will be instantiated and called as such:
# obj = BusBooking(n)
# obj.toggle(seat)
# param_2 = obj.getTotalTime()
# param_3 = obj.getMinTime()
```
