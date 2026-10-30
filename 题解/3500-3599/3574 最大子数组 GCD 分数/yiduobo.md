---
title: "3574. 最大子数组GCD分数"
aliases: ["yiduobo的每日leetcode 3574.最大子数组GCD分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/bao-li", "题单/位运算", "题单/数学算法", "题单/位运算/三-与或-AND/OR-的性质", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936950527712819190"
zhihu_id: "1936950527712819190"
zhihu_title: "yiduobo的每日leetcode 3574.最大子数组GCD分数"
question_id: "3574"
question: "最大子数组 GCD 分数"
problem_url: "https://leetcode.cn/problems/maximize-subarray-gcd-score/"
difficulty: "Hard"
rating: 2300
created: "2025-08-08T01:17:29+08:00"
updated: "2025-08-08T01:17:30+08:00"
upvotes: 1
comments: 0
---

# 3574. 最大子数组GCD分数

> **[yiduobo的每日leetcode 3574.最大子数组GCD分数](https://zhuanlan.zhihu.com/p/1936950527712819190) · 知乎 · 2025-08-08 · 赞同 1**
> 力扣：[3574. 最大子数组 GCD 分数](https://leetcode.cn/problems/maximize-subarray-gcd-score/) · Hard · 灵茶山艾府：[两种方法：暴力枚举 / LogTrick（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3574.最大子数组GCD分数

[3574. 最大子数组 GCD 分数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-subarray-gcd-score/description/)

题目给出一个正整数数组nums，其长度不超过1500。另外给出一个整数k，表示可以执行最多k次翻倍操作，每次操作中，可以选择nums中的一个元素将其翻倍，但是每个元素只能翻倍一次。

定义子数组的分数为其中所有元素的最大公约数与子数组长度的乘积，问修改后可以得到的最大子数组分数。

从题目的数据规模来看，可以暴力枚举nums中所有的子数组，那么问题就变成了如何高效计算每个子数组的最大公约数。

从质因数的角度来讲，翻倍实际上就是新增了一个质因子2，因此在这里可以先将数组中每个元素所有的质因子2都提取出来。不妨记nums[index]的质因子2的数量为p2[index]，那么对于nums中的某个子数组nums[start: end + 1]而言，这一段的最大公约数就是去除掉质因子2之后剩下的元素的最大公约数，即

nums[start] / 2^p2[start]，nums[start + 1] / 2^p2[start + 1]，...，nums[end] / 2^p2[end]

这些元素的最大公约数，再乘以质因子2的最大公约数，即2^min(p2[start], p2[start + 1]，...，p2[end])

题目中的翻倍操作则可以认为是将p2数组中k个不同的元素都加上1。可以发现，基于上面计算最大公约数的式子，这k个1应该用来提升p2[start]到p2[end]中最小的k个元素，这样一来才能使得min(p2[start]，p2[start + 1]，...，p2[end])变大。

更进一步的，在这里只需要知道其中的最小值mi，以及最小值出现的次数mi_cnt，若mi_cnt \<\= k，就可以将最小的mi_cnt个值为mi的元素填补到mi + 1，此时子数组中质因子2的最大公约数就是2^(mi + 1)，否则就是2^mi，再乘以这些元素去除掉质因子2之后的最大公约数，即为子数组在操作后可能得到的最大公约数。暴力枚举所有子数组的起点和终点，然后通过上面的方法计算子数组的最大公约数，取其中的最大值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxGCDScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)
        p2 = [0] * n
        for index, v in enumerate(nums):
            while v % 2 == 0:
                p2[index] += 1
                v //= 2
        
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        res = 0
        for start in range(n):
            for end in range(start, n):
                if start == end:
                    g = nums[end]
                    mi = p2[end]
                    mi_cnt = 1
                else:
                    g = gcd(g, nums[end])
                    if p2[end] < mi:
                        mi = p2[end]
                        mi_cnt = 0
                    if p2[end] == mi:
                        mi_cnt += 1
                
                if mi_cnt <= k:
                    res = max(res, g * 2 * (end - start + 1))
                else:
                    res = max(res, g * (end - start + 1))
        
        return res
```
