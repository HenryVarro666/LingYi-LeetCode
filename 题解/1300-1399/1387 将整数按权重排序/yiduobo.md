---
title: "1387. 将整数按权重排序"
aliases: ["yiduobo的每日leetcode 1387.将整数按权重排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/其他", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403217713"
zhihu_id: "403217713"
zhihu_title: "yiduobo的每日leetcode 1387.将整数按权重排序"
question_id: "1387"
question: "将整数按权重排序"
problem_url: "https://leetcode.cn/problems/sort-integers-by-the-power-value/"
difficulty: "Medium"
rating: 1507
created: "2021-08-24T22:32:35+08:00"
updated: "2021-08-24T22:32:35+08:00"
upvotes: 0
comments: 0
---

# 1387. 将整数按权重排序

> **[yiduobo的每日leetcode 1387.将整数按权重排序](https://zhuanlan.zhihu.com/p/403217713) · 知乎 · 2021-08-24 · 赞同 0**
> 力扣：[1387. 将整数按权重排序](https://leetcode.cn/problems/sort-integers-by-the-power-value/) · Medium · 灵茶山艾府：[冰雹猜想，记忆化搜索（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1387.将整数按权重排序

[力扣](https://leetcode-cn.com/problems/sort-integers-by-the-power-value/)

由于题目中给出的lo和high范围都很小，那么可以对每个数字计算出变换的步数，然后一趟排序即可。当然，使用记忆化之类的方式是可以起到一定的优化作用的，但是我在这里就是直接暴力计算的。

最后附上python代码：

```python
class Solution(object):
    def getKth(self, lo, hi, k):
        """
        :type lo: int
        :type hi: int
        :type k: int
        :rtype: int
        """

        return sorted([[self.calc(x), x] for x in range(lo, hi + 1)], key=lambda d:(d[0], d[1]))[k - 1][1]
    
    def calc(self, now):
        step = 0
        while now != 1:
            if now % 2 == 0:
                now /= 2
            else:
                now = now * 3 + 1

            step += 1

        return step
```
