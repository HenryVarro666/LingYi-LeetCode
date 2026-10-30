---
title: "367. 有效的完全平方数"
aliases: ["yiduobo的每日leetcode 367.有效的完全平方数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/164883565"
zhihu_id: "164883565"
zhihu_title: "yiduobo的每日leetcode 367.有效的完全平方数"
question_id: "367"
question: "有效的完全平方数"
problem_url: "https://leetcode.cn/problems/valid-perfect-square/"
created: "2020-07-28T22:10:08+08:00"
updated: "2020-07-28T22:10:08+08:00"
upvotes: 0
comments: 0
---

# 367. 有效的完全平方数

> **[yiduobo的每日leetcode 367.有效的完全平方数](https://zhuanlan.zhihu.com/p/164883565) · 知乎 · 2020-07-28 · 赞同 0**
> 力扣：[367. 有效的完全平方数](https://leetcode.cn/problems/valid-perfect-square/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

367.有效的完全平方数<https://leetcode-cn.com/problems/valid-perfect-square/>

题目要求不能使用sqrt，因此在这里使用二分或者筛法做因式分解都是可以的。我在这里用的是二分法：

```python
class Solution(object):
    def isPerfectSquare(self, num):
        """
        :type num: int
        :rtype: bool
        """

        left = 1
        right = num
        while left <= right:
            mid = (left + right) / 2
            tmp = mid * mid
            if tmp == num:
                return True
            elif tmp > num:
                right = mid - 1
            else:
                left = mid + 1

        return False
```
