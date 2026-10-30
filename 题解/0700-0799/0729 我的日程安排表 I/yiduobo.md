---
title: "729. 我的日程安排表I"
aliases: ["yiduobo的每日leetcode 729.我的日程安排表I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/ordered-map", "leetcode/hong-hei-shu", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/335337749"
zhihu_id: "335337749"
zhihu_title: "yiduobo的每日leetcode 729.我的日程安排表I"
question_id: "729"
question: "我的日程安排表 I"
problem_url: "https://leetcode.cn/problems/my-calendar-i/"
difficulty: "Medium"
created: "2020-12-09T22:26:33+08:00"
updated: "2020-12-09T22:26:33+08:00"
upvotes: 0
comments: 0
---

# 729. 我的日程安排表I

> **[yiduobo的每日leetcode 729.我的日程安排表I](https://zhuanlan.zhihu.com/p/335337749) · 知乎 · 2020-12-09 · 赞同 0**
> 力扣：[729. 我的日程安排表 I](https://leetcode.cn/problems/my-calendar-i/) · Medium · 灵茶山艾府：[Go 平衡树](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

729.我的日程安排表I

[力扣](https://leetcode-cn.com/problems/my-calendar-i/)

又是动态区间相关的问题，不过注意到这里操作次数不超过100，那么直接使用O(n^2)的朴素算法已经足够了。具体来说就是对于新来的start和end，枚举之前已经有的所有start和end，判断是否会出现相交的情况。若出现，那么返回false，否则将新来的start和end加入日程表数组，然后返回true。

最后附上python代码：

```python
class MyCalendar(object):

    def __init__(self):
        self.canlendar = []

    def book(self, start, end):
        """
        :type start: int
        :type end: int
        :rtype: bool
        """
        for now_start, now_end in self.canlendar:
            if start < now_end and end > now_start:
                return False
        
        self.canlendar.append([start, end])
        return True

# Your MyCalendar object will be instantiated and called as such:
# obj = MyCalendar()
# param_1 = obj.book(start,end)
```
