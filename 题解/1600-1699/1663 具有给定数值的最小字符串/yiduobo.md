---
title: "1663. 具有给定数值的最小字符串"
aliases: ["yiduobo的每日leetcode 1663.具有给定数值的最小字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/442494842"
zhihu_id: "442494842"
zhihu_title: "yiduobo的每日leetcode 1663.具有给定数值的最小字符串"
question_id: "1663"
question: "具有给定数值的最小字符串"
problem_url: "https://leetcode.cn/problems/smallest-string-with-a-given-numeric-value/"
created: "2021-12-07T23:58:20+08:00"
updated: "2021-12-07T23:58:20+08:00"
upvotes: 0
comments: 0
---

# 1663. 具有给定数值的最小字符串

> **[yiduobo的每日leetcode 1663.具有给定数值的最小字符串](https://zhuanlan.zhihu.com/p/442494842) · 知乎 · 2021-12-07 · 赞同 0**
> 力扣：[1663. 具有给定数值的最小字符串](https://leetcode.cn/problems/smallest-string-with-a-given-numeric-value/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1663.具有给定数值的最小字符串

[力扣](https://leetcode-cn.com/problems/smallest-string-with-a-given-numeric-value/)

题目要求答案的字典序最小，那么一个很自然的想法就是尽量用a来填充高位，但是有一个前提是当前位使用了a之后，后续位置的值必须能够到k。

对于一个长度为n的字符串而言，其最大的组合为n个z，此时的数值就是26 \* n。如果要将最高位置为a，那么剩下的位最多能够到26 \* (n - 1)，而这些字符需要达成的目标为k - 1，这里的减一代表了最高位这个a的值。也就是说，只有当满足26 \* (n - 1) >\= k - 1时，才能把最高位置为a。

现在就有了一种做法。使用rest记录下当前字符串可能到达的最大数值，初始值自然是26 \* n。接下来从高位到低位一趟遍历。若当前的rest - 26 >\= k - 1时，就将当前位填充上a，并将rest减去26，k减去1，然后继续考察下一位。若不满足这个条件，那么说明当前位已经有了限制。为了让答案的字典序最小，那么也应当让当前位尽可能小，那么如果将后续所有位都填充上z，当前位剩下的值就应该是(rest - 1) % 26 + 1。使用这个值填充当前位，然后将后续位全部填充上z即可。

最后附上python代码：

```python
class Solution(object):
    def getSmallestString(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """

        res = []
        now = 0
        max_rest = 26 * n
        while now < n:
            if max_rest - k > 24:
                res.append('a')
                max_rest -= 26
                k -= 1
            else:
                res.append(chr(97 + (k - 1) % 26))
                break
        
        while len(res) < n:
            res.append('z')
        
        return ''.join(res)
```
