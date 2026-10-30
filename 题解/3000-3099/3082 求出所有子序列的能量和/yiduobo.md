---
title: "3082. 求出所有子序列的能量和"
aliases: ["yiduobo的每日leetcode 3082.求出所有子序列的能量和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/三-背包", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698547989"
zhihu_id: "698547989"
zhihu_title: "yiduobo的每日leetcode 3082.求出所有子序列的能量和"
question_id: "3082"
question: "求出所有子序列的能量和"
problem_url: "https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences/"
difficulty: "Hard"
rating: 2242
created: "2024-05-18T23:55:50+08:00"
updated: "2024-05-18T23:55:50+08:00"
upvotes: 0
comments: 0
---

# 3082. 求出所有子序列的能量和

> **[yiduobo的每日leetcode 3082.求出所有子序列的能量和](https://zhuanlan.zhihu.com/p/698547989) · 知乎 · 2024-05-18 · 赞同 0**
> 力扣：[3082. 求出所有子序列的能量和](https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences/) · Hard · 灵茶山艾府：[两种方法：从 O(nnk) 到 O(nk)，附题单！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3082.求出所有子序列的能量和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-sum-of-the-power-of-all-subsequences/)

题目给出一个数组nums以及一个整数k，对于数组中的某个子序列s，若这个子序列s有m个子序列之和恰好为k，那么s的能量值就是m，问nums的所有子序列的能量值之和。

注意到题目中k的取值范围较小，那么可以尝试将子序列之和表示到状态中，利用动态规划求解。

令f[i][j]表示前i个数中可以构成的子序列sj数目，这里的sj需要满足sj中的某个子序列之和等于j。那么对于f[i][j]，考虑nums[i]的使用：

1、不加入子序列sj中，那么就有f[i][j] +\= f[i - 1][j]

2、加入子序列sj中，但是不加入sj的和为j的子序列中，那么同样是f[i][j] +\= f[i - 1][j]

3、加入子序列sj中，同时也属于sj的和为j的子序列的一部分，那么就有f\[i\]\[j\] +\= f\[i - 1\]\[j - nums\[i\]\]

计算完成后，f[-1][k]即为最终答案。另外注意到f的每一轮状态只与上一轮有关，因此在这里可以采用倒序遍历的方式省略掉i这一位。

最后附上python代码：

```python
class Solution(object):
    def sumOfPower(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = [0] * (k + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for v in nums:
            for index in range(k, -1, -1):
                f[index] += f[index]
                if f[index] >= mod:
                    f[index] -= mod

                if index >= v:
                    f[index] += f[index - v]
                    if f[index] >= mod:
                        f[index] -= mod

        return f[-1]
```
