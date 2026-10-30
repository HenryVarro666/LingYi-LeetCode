---
title: "278. 第一个错误的版本"
aliases: ["yiduobo的每日leetcode 278.第一个错误的版本"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/152535171"
zhihu_id: "152535171"
zhihu_title: "yiduobo的每日leetcode 278.第一个错误的版本"
question_id: "278"
question: "第一个错误的版本"
problem_url: "https://leetcode.cn/problems/first-bad-version/"
created: "2020-07-01T17:41:34+08:00"
updated: "2020-07-01T17:41:34+08:00"
upvotes: 0
comments: 0
---

# 278. 第一个错误的版本

> **[yiduobo的每日leetcode 278.第一个错误的版本](https://zhuanlan.zhihu.com/p/152535171) · 知乎 · 2020-07-01 · 赞同 0**
> 力扣：[278. 第一个错误的版本](https://leetcode.cn/problems/first-bad-version/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

278.第一个错误的版本<https://leetcode-cn.com/problems/first-bad-version/>

依然是二分的题目，对1到n进行二分，若当前的mid是错误的版本，那么答案就位于left到mid之间，否则答案位于mid + 1到right之间。

二分的思路总是很简单的，但是具体实现时需要注意最终答案的位置来决定left与right如何通过mid进行迭代，尤其是对于mid \= (left + right)/2，如果left的迭代是通过left \= mid进行的，那么就有可能出现死循环，需要特别判断。

最后附上python代码：

```python
# The isBadVersion API is already defined for you.
# @param version, an integer
# @return a bool
# def isBadVersion(version):

class Solution(object):
    def firstBadVersion(self, n):
        """
        :type n: int
        :rtype: int
        """

        left = 1
        right = n

        while left < right:
            mid = (left + right) / 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1

        return left
```
