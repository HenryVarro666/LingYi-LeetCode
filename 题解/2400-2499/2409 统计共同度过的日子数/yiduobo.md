---
title: "2409. 统计共同度过的日子数"
aliases: ["yiduobo的每日leetcode 2409.统计共同度过的日子数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/api", "leetcode/simulation", "leetcode/shi-jian"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568081892"
zhihu_id: "568081892"
zhihu_title: "yiduobo的每日leetcode 2409.统计共同度过的日子数"
question_id: "2409"
question: "统计共同度过的日子数"
problem_url: "https://leetcode.cn/problems/count-days-spent-together/"
difficulty: "Easy"
created: "2022-09-25T23:10:27+08:00"
updated: "2022-09-25T23:10:27+08:00"
upvotes: 0
comments: 0
---

# 2409. 统计共同度过的日子数

> **[yiduobo的每日leetcode 2409.统计共同度过的日子数](https://zhuanlan.zhihu.com/p/568081892) · 知乎 · 2022-09-25 · 赞同 0**
> 力扣：[2409. 统计共同度过的日子数](https://leetcode.cn/problems/count-days-spent-together/) · Easy · 灵茶山艾府：[模拟 + 计算区间交集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2409.统计共同度过的日子数

[力扣](https://leetcode.cn/problems/count-days-spent-together/)

题目本质上是给出两个区间，求这两个区间交集的长度。不过在这里给出的区间是月-日这种形式的，使用起来不太方便，需要先将其转化为一年中的第几天。

接下来对于两个区间，先排除掉不想交的情况，即一个区间的右边界在另一个区间的左边界的左侧这种情况。确定相交之后，相交区间的左右边界就分别是两个区间左边界的较大值，以及两个区间右边界的较小值，使用这两个新的边界更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countDaysTogether(self, arriveAlice, leaveAlice, arriveBob, leaveBob):
        """
        :type arriveAlice: str
        :type leaveAlice: str
        :type arriveBob: str
        :type leaveBob: str
        :rtype: int
        """

        dates = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        s = [0]
        for d in dates[:11]:
            s.append(s[-1] + d)
        
        def get_date(date_s):
            m, d = date_s.split('-')
            return s[int(m) - 1] + int(d)

        alice = [get_date(arriveAlice), get_date(leaveAlice)]
        bob = [get_date(arriveBob), get_date(leaveBob)]

        if alice[1] < bob[0] or bob[1] < alice[0]:
            return 0
        else:
            return min(alice[1], bob[1]) - max(alice[0], bob[0]) + 1
```
