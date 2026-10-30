---
title: "3098. 求出所有子序列的能量和"
aliases: ["yiduobo的每日leetcode 3098.求出所有子序列的能量和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699729916"
zhihu_id: "699729916"
zhihu_title: "yiduobo的每日leetcode 3098.求出所有子序列的能量和"
question_id: "3098"
question: "求出所有子序列的能量和"
problem_url: "https://leetcode.cn/problems/find-the-sum-of-subsequence-powers/"
created: "2024-05-25T01:08:03+08:00"
updated: "2024-05-25T01:08:03+08:00"
upvotes: 1
comments: 0
---

# 3098. 求出所有子序列的能量和

> **[yiduobo的每日leetcode 3098.求出所有子序列的能量和](https://zhuanlan.zhihu.com/p/699729916) · 知乎 · 2024-05-25 · 赞同 1**
> 力扣：[3098. 求出所有子序列的能量和](https://leetcode.cn/problems/find-the-sum-of-subsequence-powers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3098.求出所有子序列的能量和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-sum-of-subsequence-powers/description/)

题目给出一个数组nums以及一个正整数k，要求计算数组中所有长度为k的子序列的能量值。子序列的能力值指的是子序列中两两元素之差的绝对值的最小值。

注意到数组的长度比较小，因此可以先暴力枚举数组中的元素对，使用一个集合记录energy_set这些差值的绝对值，接下来从中枚举子序列的能量值energy，问题就变成了求数组中存在多少个长度为k的子序列，其中各元素之差的绝对值都大于等于energy，且至少存在一个差值为energy。

为了求解这个问题，可以先将数组从小到大进行排序，接下来如果按顺序选取子序列中的元素，就只需要保证选出来的元素与上一个元素之差满足条件就行了，于是可以令f[i][j]表示选出以nums[i]为结尾的长度为j的子序列，且子序列中相邻元素之间的差值大于等于energy的方案数。

需要特别注意的是，这个状态表示是有缺陷的，因为这里的f是无法保证选出来的子序列中存在相邻元素之差恰好等于energy。一个自然的想法是另起一个数组g，令g[i][j]表示选出以nums[i]为结尾的长度为j的子序列，且子序列中相邻元素之间的差值严格大于energy的方案数，那么只需用f减去g，就可以得到所有相邻元素之差都大于等于energy，且至少存在一组相邻元素之差恰好等于energy的方案数了。

由于f和g的状态表示是非常类似的，也就是说状态转移的方式也是一样的，在这里以f的求解为例。

对于f[i][j]，由于nums是排序好的，因此在这里只需找到最大的下标p，满足nums[i] - nums[p] >\= energy，那么就有f[i][j] \= f[i - 1][0] + f[i - 1][1] + ... + f[i - 1][p]。

在这里直接枚举p是O(n)的，但是nums是单调的，因此随着i的向后移动，p也会跟着向后移动，因此在这里可以利用单调性将状态转移优化到均摊O(1)。另一方面，由于f的每一轮之和上一轮有关，因此可以使用滚动数组优化掉i这一维。

计算完当前energy对应的f和g之后，还需要枚举每种子序列的终点index，将f[index] - g[index]累加到方案数中，然后将方案数乘以energy累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumOfPowers(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums.sort()
        energy_set = set()
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                energy_set.add(abs(nums[i] - nums[j]))
        
        res = 0
        mod = 10 ** 9 + 7
        n = len(nums)
        for energy in energy_set:
            f = [1] * n
            g = [1] * n
            for _ in range(2, k + 1):
                pre_f = f[:]
                pre_g = g[:]
                f = [0] * n
                g = [0] * n
                sf = 0
                sg = 0
                p = 0
                q = 0
                for index, v in enumerate(nums):
                    while p < index and v - nums[p] >= energy:
                        sf += pre_f[p]
                        if sf >= mod:
                            sf -= mod
                        p += 1
                    while q < index and v - nums[q] > energy:
                        sg += pre_g[q]
                        if sg >= mod:
                            sg -= mod
                        q += 1

                    f[index] = sf
                    g[index] = sg
        
            tot = 0
            for index in range(n):
                tot += (f[index] - g[index] + mod)
                if tot >= mod:
                    tot -= mod
            
            res = (res + tot * energy) % mod
        
        return res
```
