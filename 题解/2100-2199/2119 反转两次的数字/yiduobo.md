---
title: "2119. 反转两次的数字"
aliases: ["yiduobo的每日leetcode 2119.反转两次的数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524631413"
zhihu_id: "524631413"
zhihu_title: "yiduobo的每日leetcode 2119.反转两次的数字"
question_id: "2119"
question: "反转两次的数字"
problem_url: "https://leetcode.cn/problems/a-number-after-a-double-reversal/"
difficulty: "Easy"
created: "2022-06-06T00:07:46+08:00"
updated: "2022-06-06T00:07:46+08:00"
upvotes: 0
comments: 0
---

# 2119. 反转两次的数字

> **[yiduobo的每日leetcode 2119.反转两次的数字](https://zhuanlan.zhihu.com/p/524631413) · 知乎 · 2022-06-06 · 赞同 0**
> 力扣：[2119. 反转两次的数字](https://leetcode.cn/problems/a-number-after-a-double-reversal/) · Easy · 灵茶山艾府：[Go 一行](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2119.反转两次的数字

[力扣](https://leetcode.cn/problems/a-number-after-a-double-reversal/)

题目要求对数字进行两次翻转，在翻转时将去掉前导0，问最终得到的数字是否和原数字一样。

可以发现，只有去除前导0再翻转这种情况可能使得数字发生改变，由于原数字是没有前导0的，因此翻转后就没有后缀0，再次翻转也不会有前导0，所以只有一种情况，就是原数字有后缀0，第一次翻转后出现了前导0被去除了。因此只需检测原数字是否有后缀0，即检测原数字模10是否等于0就行了。

另外还需要特别注意0这个特殊情况，其两次翻转后并不会产生变化。

最后附上python代码：

```python
class Solution(object):
    def isSameAfterReversals(self, num):
        """
        :type num: int
        :rtype: bool
        """

        if num == 0:
            return True

        return num % 10 != 0
```
