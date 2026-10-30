---
title: "3125. 使得按位与结果为0的最大数字"
aliases: ["yiduobo的每日leetcode 3125.使得按位与结果为0的最大数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701868199"
zhihu_id: "701868199"
zhihu_title: "yiduobo的每日leetcode 3125.使得按位与结果为0的最大数字"
question_id: "3125"
question: "使得按位与结果为0的最大数字"
problem_url: "https://leetcode.cn/problems/maximum-number-that-makes-result-of-bitwise-and-zero/"
created: "2024-06-05T22:26:57+08:00"
updated: "2024-06-05T22:26:57+08:00"
upvotes: 1
comments: 0
---

# 3125. 使得按位与结果为0的最大数字

> **[yiduobo的每日leetcode 3125.使得按位与结果为0的最大数字](https://zhuanlan.zhihu.com/p/701868199) · 知乎 · 2024-06-05 · 赞同 1**
> 力扣：[3125. 使得按位与结果为0的最大数字](https://leetcode.cn/problems/maximum-number-that-makes-result-of-bitwise-and-zero/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3125.使得按位与结果为0的最大数字

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-that-makes-result-of-bitwise-and-zero/description/)

对于任意正整数n，其二进制形式都可以写成1XXXX...XXX，即其必然有一个最高位的1。为了使得按位与的结果为0，那么至少需要一个在最高位上为0的数，即0YYYY...YYY。

而对于1XXXX...XXX到0YYYY...YYY之间的整数，其中必然存在10000...000以及01111...111，二者按位与结果就已经为0了，换言之只需将n低位的1全部去除，然后再减去1即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxNumber(self, n):
        """
        :type n: int
        :rtype: int
        """

        while n & (n - 1):
            n &= (n - 1)
        return n - 1
```
