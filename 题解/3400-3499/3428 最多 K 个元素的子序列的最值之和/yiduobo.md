---
title: "3428. 最多K个元素的子序列的最值之和"
aliases: ["yiduobo的每日leetcode 3428.最多K个元素的子序列的最值之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889803332366869748"
zhihu_id: "1889803332366869748"
zhihu_title: "yiduobo的每日leetcode 3428.最多K个元素的子序列的最值之和"
question_id: "3428"
question: "最多 K 个元素的子序列的最值之和"
problem_url: "https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/"
difficulty: "Medium"
created: "2025-03-30T22:44:06+08:00"
updated: "2025-03-30T22:44:06+08:00"
upvotes: 1
comments: 0
---

# 3428. 最多K个元素的子序列的最值之和

> **[yiduobo的每日leetcode 3428.最多K个元素的子序列的最值之和](https://zhuanlan.zhihu.com/p/1889803332366869748) · 知乎 · 2025-03-30 · 赞同 1**
> 力扣：[3428. 最多 K 个元素的子序列的最值之和](https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/) · Medium · 灵茶山艾府：[贡献法+组合数学+递推优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3428.最多K个元素的子序列的最值之和

[3428. 最多 K 个元素的子序列的最值之和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/description/)

题目给出一个整数数组nums和一个正整数k，其中nums的长度n可达10^5，k不超过nums的长度并且小于等于100。现在要求返回所有长度最多为k的子序列中最大值与最小值之和的总和。

最终答案可能很大，需要对10^9 + 7取模。

题目需要计算的是所有满足条件的子序列的最大值与最小值之和，那么在这里使用贡献法是比较合适的。另一方面，由于是子序列，那么在这里就可以先将nums排序。

接下来对于nums中的某个元素nums[index]，若其为子序列中的最大值，那么子序列中剩下的所有元素都应该从从nums[0]到nums[index - 1]之间选取；同样的，若其为子序列中的最小值，那么子序列中剩下的所有元素则都应该从nums[index + 1]到nums[-1]之间选择。

由于这两种情况是对称的，那么在这里对nums[index]作为子序列中最大值的情况进行分析。这种情况下，可以从左侧的index个元素中选取0、1、2、...、k - 1个其他元素构成子序列，因此选取的方案数就是

sum_c[index] \= C(index, 0) + C(index, 1) + C(index, 2) + ... + C(index, k - 1)

由于nums长度以及k的取值范围不小，使用O(nk)的复杂度先预处理出所有的sum_c在时间复杂度方面是比较微妙的，在这里最好还是优化一下。

根据组合数C(i, j) \= C(i - 1, j - 1) + C(i - 1, j)的式子，可以尝试将sum_c中的相邻项进行合并。具体来说

sum_c[index] \* 2 \= C(index, 0) + (C(index, 0) + C(index, 1)) + ... + (C(index, k - 2) + C(index, k - 1)) + C(index, k - 1)

合并后就有

sum_c[index] \* 2 \= C(index, 0) + C(index + 1, 1) + C(index + 1, 2) + ... + C(index + 1, k - 1) + C(index, k - 1)

由于C(index, 0)和C(index + 1, 0)都等于，那么将其改写为C(index + 1, 0)之后，除最后一项之外的项恰好就是sum_c[index + 1]，即

sum_c[index] \* 2 \= sum_c[index + 1] + C(index, k - 1)

于是就有

sum_c[index + 1] \= sum_c[index] \* 2 - C(index, k - 1)

而对于C(index, k - 1)的计算，可以先预处理出n - 1内所有的阶乘以及阶乘的逆元，就可以在O(1)的时间内计算得到了。乘法逆元相关的内容可以参考之前的3405题：

[yiduobo：yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目](https://zhuanlan.zhihu.com/p/31401526455)

对于nums[index]作为子序列中最小值的情况可以如法炮制，合法的子序列数目为sum_c[n - index - 1]。

那么对于nums中的每个元素nums[index]，其贡献为nums[index] \* (sum_c[index] + sum_c[n - index - 1])，将所有的贡献累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minMaxSums(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7

        n = len(nums)

        fac = [1, 1]
        inv = [None, 1]
        inv_fac = [1, 1]
        for v in range(2, n):
            fac.append(fac[-1] * v % mod)
            inv.append(-(mod // v) * inv[mod % v] % mod)
            inv_fac.append(inv_fac[-1] * inv[-1] % mod)

        def comb(n, k):
            if n < k:
                return 0
            return fac[n] * inv_fac[k] % mod * inv_fac[n - k] % mod

        sum_c = [1]
        for v in range(1, n):
            sum_c.append((sum_c[-1] * 2 - comb(v - 1, k - 1) + mod) % mod)

        res = 0
        nums.sort()
        for index, v in enumerate(nums):
            res = (res + v * (sum_c[index] + sum_c[n - index - 1]) % mod) % mod
        
        return res
```
