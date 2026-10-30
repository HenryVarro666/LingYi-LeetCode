---
title: "793. 阶乘函数后K个零"
aliases: ["yiduobo的每日leetcode 793.阶乘函数后K个零"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341867137"
zhihu_id: "341867137"
zhihu_title: "yiduobo的每日leetcode 793.阶乘函数后K个零"
question_id: "793"
question: "阶乘函数后K个零"
problem_url: "https://leetcode.cn/problems/preimage-size-of-factorial-zeroes-function/"
created: "2021-01-04T22:46:39+08:00"
updated: "2021-01-04T22:46:39+08:00"
upvotes: 1
comments: 0
---

# 793. 阶乘函数后K个零

> **[yiduobo的每日leetcode 793.阶乘函数后K个零](https://zhuanlan.zhihu.com/p/341867137) · 知乎 · 2021-01-04 · 赞同 1**
> 力扣：[793. 阶乘函数后K个零](https://leetcode.cn/problems/preimage-size-of-factorial-zeroes-function/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

793.阶乘函数后K个零

[力扣](https://leetcode-cn.com/problems/preimage-size-of-factorial-zeroes-function/)

对于一个数X，要求X！的末尾有多少个零是比较简单的，只需要统计其中因子5的数量，而统计方法则是对X不断除以5。

根据上面这个计算方式，也可以很快得到一个性质：若X是5的倍数，那么X！末尾零的数量与(X + 1)！、(X + 2)！、(X + 3)！、(X + 4)！末尾零的数量一样多。于是本题就变成了求是否存在自然数X，满足X！阶乘末尾零的个数等于K。若存在，那么答案就是5，即X到X + 4，否则答案为0。

另一方面，当X越大时，X！末尾零的个数就越多，换言之，这里满足二分的性质。那么对着本题，就可以直接二分X，然后计算X！末尾零的数量来调整二分的上下界。

最后附上python代码：

```python
class Solution(object):
    def preimageSizeFZF(self, K):
        """
        :type K: int
        :rtype: int
        """

        l = 0
        r = K * 5
        while l <= r:
            mid = (l + r) >> 1
            tmp = mid
            cnt = 0
            while tmp:
                cnt += tmp / 5
                tmp /= 5
            if cnt == K:
                return 5
            elif cnt > K:
                r = mid - 1
            else:
                l = mid + 1
        
        return 0
```
