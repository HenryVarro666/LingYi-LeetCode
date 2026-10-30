---
title: "923. 三数之和的多种可能"
aliases: ["yiduobo的每日leetcode 923.三数之和的多种可能"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356172664"
zhihu_id: "356172664"
zhihu_title: "yiduobo的每日leetcode 923.三数之和的多种可能"
question_id: "923"
question: "三数之和的多种可能"
problem_url: "https://leetcode.cn/problems/3sum-with-multiplicity/"
created: "2021-03-10T23:10:46+08:00"
updated: "2021-03-10T23:10:46+08:00"
upvotes: 1
comments: 0
---

# 923. 三数之和的多种可能

> **[yiduobo的每日leetcode 923.三数之和的多种可能](https://zhuanlan.zhihu.com/p/356172664) · 知乎 · 2021-03-10 · 赞同 1**
> 力扣：[923. 三数之和的多种可能](https://leetcode.cn/problems/3sum-with-multiplicity/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

923.三数之和的多种可能

[力扣](https://leetcode-cn.com/problems/3sum-with-multiplicity/)

首先，很容易想到枚举第一个数，然后在后面的数中利用两数之和的做法进行配对并求解组合数。不过注意到这里的target最大只到300，那么也可以用动态规划来求解。

令f[i][j][k]表示前i个数中选出j个数，和为k有多少种可能，其中j的取值范围在1到3之间。那么对于第i个数：

1、我们可以选择arr[i]，那么就有

f\[i\]\[j\]\[k\] +\= f\[i - 1\]\[j - 1\]\[k - arr\[i\]\]

2、也可以不选择arr[i]，那么就有

f[i][j][k] +\= f[i - 1][j][k]

注意到这里的i每次只与上一轮的状态有关，因此我们可以压缩掉这一维，令f[i][j]表示前若干个数选择i个数，和为j有多少种可能，状态转移方程与上面类似，不过需要注意此时的i就需要从大到小进行遍历防止过早更新掉上一轮次的结果。

动态规划完成后，最终的f[3][target]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def threeSumMulti(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """

        f = [[0] * (target + 1) for _ in range(4)]
        f[0][0] = 1
        mod = 10 ** 9 + 7

        for num in arr:
            for j in range(target, num - 1, -1):
                f[3][j] = (f[3][j] + f[2][j - num]) % mod
                f[2][j] = (f[2][j] + f[1][j - num]) % mod
                f[1][j] = (f[1][j] + f[0][j - num]) % mod

        return f[3][target]
```
