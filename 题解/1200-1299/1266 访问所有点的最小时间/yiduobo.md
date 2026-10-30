---
title: "1266. 访问所有点的最小时间"
aliases: ["yiduobo的每日leetcode 1266.访问所有点的最小时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387048033"
zhihu_id: "387048033"
zhihu_title: "yiduobo的每日leetcode 1266.访问所有点的最小时间"
question_id: "1266"
question: "访问所有点的最小时间"
problem_url: "https://leetcode.cn/problems/minimum-time-visiting-all-points/"
difficulty: "Easy"
rating: 1303
created: "2021-07-06T11:15:44+08:00"
updated: "2021-07-06T11:15:44+08:00"
upvotes: 0
comments: 0
---

# 1266. 访问所有点的最小时间

> **[yiduobo的每日leetcode 1266.访问所有点的最小时间](https://zhuanlan.zhihu.com/p/387048033) · 知乎 · 2021-07-06 · 赞同 0**
> 力扣：[1266. 访问所有点的最小时间](https://leetcode.cn/problems/minimum-time-visiting-all-points/) · Easy · 灵茶山艾府：[切比雪夫距离（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1266.访问所有点的最小时间

[力扣](https://leetcode-cn.com/problems/minimum-time-visiting-all-points/)

由于题目要求按照顺序走完所有点，实际上只需要遍历所有点，求解相邻点之间的访问时间，并求和即为最终答案。

可以明确的一点是，若两个点不在同行也不在同列，走斜线就是最好的选择，那么可以不断走斜线，直到两个点在同一行或者同一列，然后再进行水平或者竖直的移动即可。于是两个点之间的访问时间就是二者水平距离和竖直距离中的较大值。

最后附上python代码：

```python
class Solution(object):
    def minTimeToVisitAllPoints(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        res = 0
        for index in range(1, len(points)):
            res += max(abs(points[index][0] - points[index - 1][0]), abs(points[index][1] - points[index - 1][1]))
        
        return res
```
