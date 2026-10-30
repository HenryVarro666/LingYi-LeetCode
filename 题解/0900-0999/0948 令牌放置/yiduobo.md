---
title: "948. 令牌放置"
aliases: ["yiduobo的每日leetcode 948.令牌放置"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359400497"
zhihu_id: "359400497"
zhihu_title: "yiduobo的每日leetcode 948.令牌放置"
question_id: "948"
question: "令牌放置"
problem_url: "https://leetcode.cn/problems/bag-of-tokens/"
created: "2021-03-23T23:58:12+08:00"
updated: "2021-03-23T23:58:12+08:00"
upvotes: 0
comments: 0
---

# 948. 令牌放置

> **[yiduobo的每日leetcode 948.令牌放置](https://zhuanlan.zhihu.com/p/359400497) · 知乎 · 2021-03-23 · 赞同 0**
> 力扣：[948. 令牌放置](https://leetcode.cn/problems/bag-of-tokens/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

948.令牌放置

[力扣](https://leetcode-cn.com/problems/bag-of-tokens/)

由于这里的令牌在最终计分的时候都是等价的，因此在初始选取令牌的时候，显然应当优先选取那些能量消耗比较低的。因此可以先对令牌按能量从小到大进行排序，接下来：

1、尽量多的选取头部的令牌直到能量不足，此时可以用现有的令牌数去更新答案

2、此时应当使用一个令牌来换取最大的能量，也就是从排序后的另一侧开始进行交换，然后重复步骤一直到令牌全部用完

最后附上python代码：

```python
class Solution(object):
    def bagOfTokensScore(self, tokens, P):
        """
        :type tokens: List[int]
        :type P: int
        :rtype: int
        """

        sorted_tokens = sorted(tokens)

        l = 0
        r = len(sorted_tokens) - 1
        res = 0
        now = 0
        while l <= r:
            while l <= r and sorted_tokens[l] <= P:
                now += 1
                P -= sorted_tokens[l]
                l += 1

            res = max(res, now)
            if r > l and now > 0:
                P += sorted_tokens[r]
                r -= 1
                now -= 1
            else:
                break

        return res
```
