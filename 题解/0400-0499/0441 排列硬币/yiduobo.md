---
title: "441. 排列硬币"
aliases: ["yiduobo的每日leetcode 441.排列硬币"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/204003669"
zhihu_id: "204003669"
zhihu_title: "yiduobo的每日leetcode 441.排列硬币"
question_id: "441"
question: "排列硬币"
problem_url: "https://leetcode.cn/problems/arranging-coins/"
created: "2020-08-29T01:39:16+08:00"
updated: "2020-08-29T01:39:16+08:00"
upvotes: 1
comments: 0
---

# 441. 排列硬币

> **[yiduobo的每日leetcode 441.排列硬币](https://zhuanlan.zhihu.com/p/204003669) · 知乎 · 2020-08-29 · 赞同 1**
> 力扣：[441. 排列硬币](https://leetcode.cn/problems/arranging-coins/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

441.排列硬币<https://leetcode-cn.com/problems/arranging-coins/>

比较基础的数学题。

不妨设可以排成到第k行，那么一定满足

1 + 2 + ... + k - 1 \< n

通过求和公式就有

k \* (k - 1) / 2 \< n，即(k - 1/2) ^2 \< 2n + 1/4

解得k \< sqrt(2n + 1/4) + 1/2

注意到根号里面的2n + 1/4不可能是有理数的平方，因此最终这个式子必然不是整数，那么这里k就应该是int(sqrt(2n + 1/4) + 1/2)

接下来，对于解得的k，还需验证n个硬币是否可以摆满k行，即k \* (k+ 1) / 2是否大于n。若大于，说明无法摆满，那么答案就应该是k - 1，否则就是k。

最后附上python代码：

```python
class Solution(object):
    def arrangeCoins(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = int(sqrt(n * 2 + 1 / 4) + 1 / 2)
        
        if res * (res + 1) / 2 > n:
            res -= 1
        return res
```
