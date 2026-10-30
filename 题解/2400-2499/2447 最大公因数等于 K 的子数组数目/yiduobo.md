---
title: "2447. 最大公因数等于K的子数组数目"
aliases: ["yiduobo的每日leetcode 2447.最大公因数等于K的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/number-theory", "leetcode/bao-li", "题单/位运算", "题单/数学算法", "题单/位运算/三-与或-AND/OR-的性质", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584975083"
zhihu_id: "584975083"
zhihu_title: "yiduobo的每日leetcode 2447.最大公因数等于K的子数组数目"
question_id: "2447"
question: "最大公因数等于 K 的子数组数目"
problem_url: "https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/"
difficulty: "Medium"
created: "2022-11-19T22:51:15+08:00"
updated: "2022-11-19T22:51:15+08:00"
upvotes: 0
comments: 0
---

# 2447. 最大公因数等于K的子数组数目

> **[yiduobo的每日leetcode 2447.最大公因数等于K的子数组数目](https://zhuanlan.zhihu.com/p/584975083) · 知乎 · 2022-11-19 · 赞同 0**
> 力扣：[2447. 最大公因数等于 K 的子数组数目](https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/) · Medium · 灵茶山艾府：[两种做法：暴力枚举 / 利用 GCD 的性质](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2447.最大公因数等于K的子数组数目

[力扣](https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/)

看上去像是个变长滑动窗口的问题，但是与常规滑动窗口有所不用，因为当窗口左边界向右移动时，窗口内子数组的最大公约数无法直接计算得到。一个可行的做法是将所有数分解质因数，然后计算质因子数量的变化而不是公约数的变化，实现起来比较麻烦。

由于数据规模比较小，我在这里采用的是O(n^2)的暴力算法。枚举数组的左边界i，然后从i开始向后枚举右边界j并判断当前子数组的最大公约数是否等于k。

最后附上python代码：

```python
class Solution(object):
    def subarrayGCD(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        n = len(nums)

        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        for i in range(n):
            now = nums[i]
            if now % k != 0:
                continue
            
            if now == k:
                res += 1

            for j in range(i + 1, n):
                now = gcd(now, nums[j])
                if now == k:
                    res += 1
                elif now < k:
                    break
        
        return res
```
