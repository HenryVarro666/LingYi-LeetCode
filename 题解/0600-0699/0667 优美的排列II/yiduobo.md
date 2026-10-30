---
title: "667. 优美的排列II"
aliases: ["yiduobo的每日leetcode 667.优美的排列II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/292228351"
zhihu_id: "292228351"
zhihu_title: "yiduobo的每日leetcode 667.优美的排列II"
question_id: "667"
question: "优美的排列II"
problem_url: "https://leetcode.cn/problems/beautiful-arrangement-ii/"
created: "2020-11-13T22:37:01+08:00"
updated: "2020-11-13T22:37:01+08:00"
upvotes: 0
comments: 0
---

# 667. 优美的排列II

> **[yiduobo的每日leetcode 667.优美的排列II](https://zhuanlan.zhihu.com/p/292228351) · 知乎 · 2020-11-13 · 赞同 0**
> 力扣：[667. 优美的排列II](https://leetcode.cn/problems/beautiful-arrangement-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

667.优美的排列II

[力扣](https://leetcode-cn.com/problems/beautiful-arrangement-ii/)

题目要求生成出一个排列，排列中的数两两之间的差都在1到k之间，且覆盖了1到k。由于题目并没有其他要求，因此可以使用构造法来做。

让这些差落在1到k之间是比较容易的，例如之间按升序排好，所有的差就都是1，现在主要的难点在于如何构造1到k的差值。

一个想法的折线构造，即按照

1，k + 1，2，k，3，k - 1，...，(k +1) / 2

这种方式进行构造，这里的除以2为整除。

可以发现，这里使用了1到k + 1之间所有的数，而两项之间的差值分别为k，k - 1，k - 2，...，1，已经覆盖住了1到k。此时还剩下k + 2到n这些数，那么只需要想办法这些数加入答案后，依然满足两两之间的差值在1到k之间即可。

我们可以将上面的构造调换一下顺序，变成

k + 1，1，k，2，k - 1，3，...，(k + 1) / 2

这种形式，依然是使用1到k + 1之间的数，差值覆盖住了1到k。此时如果我们按照n到k + 2到降序插入到k + 1前面，那么这些项两两之间的差值就是1。

此时就得到了一种合法的构造，即

n，n - 1，n - 2，...，k + 2，k + 1，1，k，2，k - 1，3，...，(k + 1) / 2

最后附上python代码：

```python
class Solution(object):
    def constructArray(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[int]
        """

        res = [x for x in range(n, k, -1)]
        low = 1
        high = k
        while low <= high:
            res.append(low)
            low += 1
            if low <= high:
                res.append(high)
                high -= 1

        return res
```
