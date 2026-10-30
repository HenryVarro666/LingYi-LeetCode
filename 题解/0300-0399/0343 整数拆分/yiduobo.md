---
title: "343. 整数拆分"
aliases: ["yiduobo的每日leetcode 343.整数拆分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163262675"
zhihu_id: "163262675"
zhihu_title: "yiduobo的每日leetcode 343.整数拆分"
question_id: "343"
question: "整数拆分"
problem_url: "https://leetcode.cn/problems/integer-break/"
created: "2020-07-23T20:43:43+08:00"
updated: "2020-07-23T20:43:43+08:00"
upvotes: 0
comments: 0
---

# 343. 整数拆分

> **[yiduobo的每日leetcode 343.整数拆分](https://zhuanlan.zhihu.com/p/163262675) · 知乎 · 2020-07-23 · 赞同 0**
> 力扣：[343. 整数拆分](https://leetcode.cn/problems/integer-break/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

343.整数拆分<https://leetcode-cn.com/problems/integer-break/>

经典的数学题，具体原理不知道应该怎么证明，总而言之就是尽量拆3，不过对于4的情况则是拆成2\*2更好。

最后附上python代码：

```python
class Solution(object):
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 2:
            return 1
        elif n == 3:
            return 2
        else:
            pow3 = n / 3
            n %= 3
            res = 1
            if n == 1:
                pow3 -= 1
                res = 4
            elif n == 2:
                res = 2

            res *= 3 ** pow3
            return res
```
