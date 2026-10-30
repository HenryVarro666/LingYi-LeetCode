---
title: "967. 连续差相同的数字"
aliases: ["yiduobo的每日leetcode 967.连续差相同的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361725059"
zhihu_id: "361725059"
zhihu_title: "yiduobo的每日leetcode 967.连续差相同的数字"
question_id: "967"
question: "连续差相同的数字"
problem_url: "https://leetcode.cn/problems/numbers-with-same-consecutive-differences/"
created: "2021-04-01T23:09:15+08:00"
updated: "2021-04-01T23:09:15+08:00"
upvotes: 0
comments: 0
---

# 967. 连续差相同的数字

> **[yiduobo的每日leetcode 967.连续差相同的数字](https://zhuanlan.zhihu.com/p/361725059) · 知乎 · 2021-04-01 · 赞同 0**
> 力扣：[967. 连续差相同的数字](https://leetcode.cn/problems/numbers-with-same-consecutive-differences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

967.连续差相同的数字

[力扣](https://leetcode-cn.com/problems/numbers-with-same-consecutive-differences/)

动态规划的题目，令f[i][j]表示i位数，最后一位为j时有哪些合法的答案，那么对于f[i][j]而言：

1、若j + k \<\= 9，那么对于f[i][j]中的所有数而言，将这个数乘以10再加上j + k必然符合要求的i + 1位数，

2、若j - k >\= 9，同理，对于f[i][j]中的所有数而言，将这个数乘以10再加上j - k必然也是符合要求的i + 1位数

全部计算完成后，将f[n][0]到f[n][9]全部收集起来就是最终答案。

注意到这里每一轮状态只与上一轮有关，于是也可以使用滚动数组来进行优化。

最后附上python代码：

```python
class Solution(object):
    def numsSameConsecDiff(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[int]
        """

        f = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
        for i in range(2, n + 1):
            tmp = [set() for _ in range(10)]
            for last in range(10):
                if last + k <= 9:
                    for x in f[last]:
                        tmp[last + k].add(x * 10 + last + k)
                if last - k >= 0:
                    for x in f[last]:
                        tmp[last - k].add(x * 10 + last - k)
            f = tmp[:]

        res = []
        for last in range(10):
            res += f[last]
        
        return res
```
