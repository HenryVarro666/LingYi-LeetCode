---
title: "974. 和可被K整除的子数组"
aliases: ["yiduobo的每日leetcode 974.和可被K整除的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362456182"
zhihu_id: "362456182"
zhihu_title: "yiduobo的每日leetcode 974.和可被K整除的子数组"
question_id: "974"
question: "和可被 K 整除的子数组"
problem_url: "https://leetcode.cn/problems/subarray-sums-divisible-by-k/"
difficulty: "Medium"
rating: 1676
created: "2021-04-05T20:19:32+08:00"
updated: "2021-04-05T20:19:32+08:00"
upvotes: 0
comments: 0
---

# 974. 和可被K整除的子数组

> **[yiduobo的每日leetcode 974.和可被K整除的子数组](https://zhuanlan.zhihu.com/p/362456182) · 知乎 · 2021-04-05 · 赞同 0**
> 力扣：[974. 和可被 K 整除的子数组](https://leetcode.cn/problems/subarray-sums-divisible-by-k/) · Medium · 灵茶山艾府：[前缀和与哈希表 + 式子变形（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

974.和可被K整除的子数组

[力扣](https://leetcode-cn.com/problems/subarray-sums-divisible-by-k/)

对于子数组和问题，第一想法就是利用前缀和之差来进行处理，具体来说就是对于i到j这一段，和为s \= A[i] + A[i + 1] + ... + A[j]。令p表示A的前缀和，那么

p[j] \= A[0] + A[1] + ... + A[j]

p[i - 1] \= A[0] + A[1] + ... + A[i - 1]

于是有p[j] \= (A[0] + A[1] + ... + A[i - 1]) + (A[i] + ... + A[j]) \= p[i - 1] + s

即可以通过p[j] - p[i - 1]很快计算出s

而这里需要的是s为K的倍数，转化到前缀和就是p[j]与p[i - 1]模K同余数。于是可以在计算前缀和的过程中使用一个dict维护当前前缀和模K的余数出现的次数，然后对于当前的前缀和s，检测s mod K之前出现的次数并更新答案，然后将s mod K也加入到dict中。

最后附上python代码：

```python
class Solution(object):
    def subarraysDivByK(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        f = [0] * K
        f[0] = 1

        s = 0
        res = 0
        for num in A:
            s += num
            s %= K
            res += f[s]
            f[s] += 1
        
        return res
```
