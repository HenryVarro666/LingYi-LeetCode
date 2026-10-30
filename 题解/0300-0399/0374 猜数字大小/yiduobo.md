---
title: "374. 猜数字大小"
aliases: ["yiduobo的每日leetcode 374.猜数字大小"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165643115"
zhihu_id: "165643115"
zhihu_title: "yiduobo的每日leetcode 374.猜数字大小"
question_id: "374"
question: "猜数字大小"
problem_url: "https://leetcode.cn/problems/guess-number-higher-or-lower/"
created: "2020-07-31T22:11:34+08:00"
updated: "2020-07-31T22:11:34+08:00"
upvotes: 0
comments: 0
---

# 374. 猜数字大小

> **[yiduobo的每日leetcode 374.猜数字大小](https://zhuanlan.zhihu.com/p/165643115) · 知乎 · 2020-07-31 · 赞同 0**
> 力扣：[374. 猜数字大小](https://leetcode.cn/problems/guess-number-higher-or-lower/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

374.猜数字大小<https://leetcode-cn.com/problems/guess-number-higher-or-lower/>

经典的问题，直接二分答案即可。

最后附上python代码：

```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num):

class Solution(object):
    def guessNumber(self, n):
        """
        :type n: int
        :rtype: int
        """

        l = 1
        r = n
        while True:
            mid = (l + r) / 2
            res = guess(mid)
            if res == 0:
                return mid
            elif res > 0:
                l = mid + 1
            else:
                r = mid - 1
```
