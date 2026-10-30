---
title: "731. 我的日程安排表II"
aliases: ["yiduobo的每日leetcode 731.我的日程安排表II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/335841685"
zhihu_id: "335841685"
zhihu_title: "yiduobo的每日leetcode 731.我的日程安排表II"
question_id: "731"
question: "我的日程安排表II"
problem_url: "https://leetcode.cn/problems/my-calendar-ii/"
created: "2020-12-10T23:17:49+08:00"
updated: "2020-12-10T23:17:49+08:00"
upvotes: 0
comments: 0
---

# 731. 我的日程安排表II

> **[yiduobo的每日leetcode 731.我的日程安排表II](https://zhuanlan.zhihu.com/p/335841685) · 知乎 · 2020-12-10 · 赞同 0**
> 力扣：[731. 我的日程安排表II](https://leetcode.cn/problems/my-calendar-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

731.我的日程安排表II

[力扣](https://leetcode-cn.com/problems/my-calendar-ii/)

注意到题目保证调用的次数不超过1000次，那么也还是可以用最朴素的算法来做。不过这里同一时间可以出现两次预定，那么我们可以适当转化思路。

我们假想出一条时间轴，那么每次预定就是在这个时间轴上设置了两个点。我们从时间轴上最早的点出发往后走，若这是一个预定起点，那么我们就将计数器加一，若这是一个终点，则将计数器减一。若某个时刻计数器超过了2，说明此时有三个预定同时发生，是非法情况。

于是现在的做法为，对于新来的某个预定，我们将其加入time_list，然后对于排序后的time_list，我们按上面说的方法进行检测。若检测不通过，则将这个预定从time_list中删去。在这里使用二分查找的话，最终时间复杂度位O(n^2)，使用排序则是O(n^2 \* logn)，方便起见我就使用的排序。

另外，对于这类开闭区间还有一个小技巧，就是将区间起点乘以2，区间终点乘以2然后减1，这样一来，原始的[x, y)以及[y, z)，就转换成了[2x, 2y - 1]以及[2y，2z - 1]，相比之下会更加方便直观。

最后附上python代码：

```python
class MyCalendarTwo(object):

    def __init__(self):
        self.time_list = []

    def book(self, start, end):
        """
        :type start: int
        :type end: int
        :rtype: bool
        """
        self.time_list.append(start * 2)
        self.time_list.append(end * 2 - 1)

        cnt = 0
        for time_point in sorted(self.time_list):
            if time_point & 1:
                cnt -= 1
            else:
                cnt += 1
                if cnt > 2:
                    self.time_list.pop()
                    self.time_list.pop()
                    return False

        return True

# Your MyCalendarTwo object will be instantiated and called as such:
# obj = MyCalendarTwo()
# param_1 = obj.book(start,end)
```
