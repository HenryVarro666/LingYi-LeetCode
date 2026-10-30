---
title: "507. 完美数"
aliases: ["yiduobo的每日leetcode 507.完美数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259364448"
zhihu_id: "259364448"
zhihu_title: "yiduobo的每日leetcode 507.完美数"
question_id: "507"
question: "完美数"
problem_url: "https://leetcode.cn/problems/perfect-number/"
created: "2020-09-25T21:23:07+08:00"
updated: "2020-09-25T21:23:07+08:00"
upvotes: 0
comments: 0
---

# 507. 完美数

> **[yiduobo的每日leetcode 507.完美数](https://zhuanlan.zhihu.com/p/259364448) · 知乎 · 2020-09-25 · 赞同 0**
> 力扣：[507. 完美数](https://leetcode.cn/problems/perfect-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

507.完美数<https://leetcode-cn.com/problems/perfect-number/>

跟约数相关的问题大概有数学方法可以在常数时间内解决这个问题，但是我没什么思路，于是采用的是朴素的O(sqrt(n))的做法，具体就是从1到sqrt(n)循环，若当前数x能被num整数，那么x和num/x都是num的约数，将这两个数累加至sum，最后判断sum是否等于num。

需要注意的是，当num是完全平方数时，对于x \= sqrt(num)而言，x和num/x是同一个数，只能统计一次。

最后附上python代码：

```python
class Solution(object):
    def checkPerfectNumber(self, num):
        """
        :type num: int
        :rtype: bool
        """

        if num <= 1:
            return False

        tmp = 1
        for i in range(2, int(sqrt(num) + 1)):
            if i * i > num:
                break
            elif i * i == num:
                tmp += i
            elif num % i == 0:
                tmp += i + num / i
        return tmp == num
```
