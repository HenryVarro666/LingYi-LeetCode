---
title: "LCP 22. 黑白方格画"
aliases: ["yiduobo的每日leetcode LCP22.黑白方格画"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/572696012"
zhihu_id: "572696012"
zhihu_title: "yiduobo的每日leetcode LCP22.黑白方格画"
question_id: "LCP 22"
question: "黑白方格画"
problem_url: "https://leetcode.cn/problems/ccw6/"
created: "2022-10-12T02:43:13+08:00"
updated: "2022-10-12T02:43:13+08:00"
upvotes: 0
comments: 0
---

# LCP 22. 黑白方格画

> **[yiduobo的每日leetcode LCP22.黑白方格画](https://zhuanlan.zhihu.com/p/572696012) · 知乎 · 2022-10-12 · 赞同 0**
> 力扣：[LCP 22. 黑白方格画](https://leetcode.cn/problems/ccw6/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP22.黑白方格画

[力扣](https://leetcode.cn/problems/ccw6C7/)

不妨设最终涂黑了x行、y列，那么一共就有(x + y) \* n - x \* y个格子被涂黑，这里减去x \* y的理由是一共有x \* y个格子是在行和列涂黑时都被计算了的。

那么就有(x + y) \* n - x \* y \= k。由于题目中n的规模很小，那么可以直接枚举x，并判断对于当前的x而言，y是否存在整数解。得到一组x和y之后，就是简单的组合数学问题了，即从n行里选出x行，n列里选出y列有多少中选法，对应的就是C(n, x) \* C(n, y)。

对于每一组x和y都计算这个组合数，并累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def paintingPlan(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        if k == n * n:
            return 1

        C = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 10, 6, 1]]

        res = 0
        for x in range(n):
            if k >= x * n and (k - x * n) % (n - x) == 0:
                y = (k - x * n) / (n - x)
                res += C[n][x] * C[n][y]
        
        return res
```
