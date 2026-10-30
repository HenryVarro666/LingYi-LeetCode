---
title: "732. 我的日程安排表III"
aliases: ["yiduobo的每日leetcode 732.我的日程安排表III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336273971"
zhihu_id: "336273971"
zhihu_title: "yiduobo的每日leetcode 732.我的日程安排表III"
question_id: "732"
question: "我的日程安排表III"
problem_url: "https://leetcode.cn/problems/my-calendar-iii/"
created: "2020-12-11T23:13:26+08:00"
updated: "2020-12-11T23:13:26+08:00"
upvotes: 0
comments: 0
---

# 732. 我的日程安排表III

> **[yiduobo的每日leetcode 732.我的日程安排表III](https://zhuanlan.zhihu.com/p/336273971) · 知乎 · 2020-12-11 · 赞同 0**
> 力扣：[732. 我的日程安排表III](https://leetcode.cn/problems/my-calendar-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

732.我的日程安排表III

[力扣](https://leetcode-cn.com/problems/my-calendar-iii/)

依然是动态区间问题，这里是求最多的区间叠加次数，因此可以使用与上一题完全相同的算法。

[yiduobo：yiduobo的每日leetcode 731.我的日程安排表II](https://zhuanlan.zhihu.com/p/335841685)

对于这一题，则是每一次预定都将开始时间与结束时间加入time_list中，排序后从头到尾扫描进行统计。同样可以使用乘2以及乘2减1的方式来简化判断。

最后附上python代码：

```python
class MyCalendarThree(object):

    def __init__(self):
        self.time_list = []        

    def book(self, start, end):
        """
        :type start: int
        :type end: int
        :rtype: int
        """
        self.time_list.append(start * 2)
        self.time_list.append(end * 2 - 1)

        res = cnt = 0
        for time_point in sorted(self.time_list):
            if time_point & 1:
                cnt -= 1
            else:
                cnt += 1
                res = max(res, cnt)
        
        return res

# Your MyCalendarThree object will be instantiated and called as such:
# obj = MyCalendarThree()
# param_1 = obj.book(start,end)
```
