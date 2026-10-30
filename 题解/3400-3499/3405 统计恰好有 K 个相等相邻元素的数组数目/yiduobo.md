---
title: "3405. 统计恰好有K个相等相邻元素的数组数目"
aliases: ["yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31401526455"
zhihu_id: "31401526455"
zhihu_title: "yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目"
question_id: "3405"
question: "统计恰好有 K 个相等相邻元素的数组数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/"
difficulty: "Hard"
rating: 2310
created: "2025-03-19T23:02:21+08:00"
updated: "2025-03-19T23:02:21+08:00"
upvotes: 0
comments: 0
---

# 3405. 统计恰好有K个相等相邻元素的数组数目

> **[yiduobo的每日leetcode 3405.统计恰好有K个相等相邻元素的数组数目](https://zhuanlan.zhihu.com/p/31401526455) · 知乎 · 2025-03-19 · 赞同 0**
> 力扣：[3405. 统计恰好有 K 个相等相邻元素的数组数目](https://leetcode.cn/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/) · Hard · 灵茶山艾府：[纯数学题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3405.统计恰好有K个相等相邻元素的数组数目

[3405. 统计恰好有 K 个相等相邻元素的数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/description/)

题目给出三个整数n、m、k，另外定义长度为n的好数组arr为：

1、arr中所有元素的大小都在1到m之间

2、arr中恰好有k个下标i（其中1 \<\= i \< n）满足arr[i - 1] \= arr[i]

问对于给出的n、m、k，可以构造出多少个好数组。由于答案可能会很大，需要对p \= 10^9 + 7取模。

根据题目的要求，首先需要从1到n - 1这些下标中选出k个下标，这些下标上的元素与前一个元素相同。这样一来，一共有C(n - 1, k)种选择的方案。

另一方面，对于其他位置上的元素，其不能与上一个元素相同。对于arr[0]而言，可以从1到m之间选择任意数字填充，而对于后续的元素，为了不与上一个元素相同，则只有m - 1种可行的选择。由于一共有n - k个其他位置上的元素，去除掉arr[0]之外还需要填充n - k - 1个，因此一共有(m - 1)^(n - k - 1)种填充的方案。再考虑上arr[0]，一共的方案就是m \* ((m - 1)^(n - k - 1))。

综合上面的结论，最终答案就是C(n - 1, k) \* m \* ((m - 1)^(n - k - 1))。

在具体计算时，由于组合数的存在，因此还需要先计算1到k对于mod的乘法逆元。关于乘法逆元的计算，我在之前都是靠费马小定理和欧拉定理来算的，不过前不久新学到了一种O(n)求1到n的乘法逆元的算法，看上去很优美。具体来说，对于质数p而言，不妨设1到n对于p的乘法逆元分别为inv[1]到inv[n]，接下来从1遍历到n，对于当前遍历到的v而言：

1、若v \= 1：

显然有inv[v] \= 1

2、对于v >\= 2的情况：

不妨设x \= p // v，y \= p % v，那么就有p \= x \* v + y，在模p的意义下就是x \* v + y ≡ 0 (mod p)。

接下来，在x \* v + y ≡ 0 (mod p)两边同时乘以inv[v] \* inv[y]，就有x \* inv[y] + inv[v] ≡ 0 (mod p)，从而有inv[v] ≡ -x \* inv[y] (mod p)。需要注意的是，这一步成立的前提是p是质数，才能保证inv[v]和inv[y]是存在的。

另一方面，由于y是模v得到的，必然小于v，而inv是从1到n按顺序枚举计算的，因此对于当前计算的inv[v]，可以认为inv[y]在之前就已经算出来了，此时只需将其带入到上面的式子就行了。

最后附上python代码：

```python
class Solution(object):
    def countGoodArrays(self, n, m, k):
        """
        :type n: int
        :type m: int
        :type k: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7
        fact = [1]
        inv = [1]

        def quick_pow(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p >> 1, mod)
            res *= res
            res %= mod
            if p & 1:
                res *= base
                res %= mod
            return res

        inv = [1, 1]
        for v in range(2, k + 1):
            inv.append(-(mod // v) * inv[mod % v] % mod)
        
        res = 1
        for v in range(1, k + 1):
            res *= n - v
            res %= mod
            res *= inv[v]
            res %= mod

        res *= m
        res %= mod
        res *= quick_pow(m - 1, n - k - 1, mod)
        return res % mod
```
