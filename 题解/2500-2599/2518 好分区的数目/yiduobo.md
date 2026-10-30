---
title: "2518. 好分区的数目"
aliases: ["yiduobo的每日leetcode 2518.好分区的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/数学算法", "题单/动态规划/三-背包", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634860255"
zhihu_id: "634860255"
zhihu_title: "yiduobo的每日leetcode 2518.好分区的数目"
question_id: "2518"
question: "好分区的数目"
problem_url: "https://leetcode.cn/problems/number-of-great-partitions/"
difficulty: "Hard"
rating: 2415
created: "2023-06-08T23:52:59+08:00"
updated: "2023-06-08T23:52:59+08:00"
upvotes: 0
comments: 0
---

# 2518. 好分区的数目

> **[yiduobo的每日leetcode 2518.好分区的数目](https://zhuanlan.zhihu.com/p/634860255) · 知乎 · 2023-06-08 · 赞同 0**
> 力扣：[2518. 好分区的数目](https://leetcode.cn/problems/number-of-great-partitions/) · Hard · 灵茶山艾府：[逆向思维 + 01 背包方案数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2518.好分区的数目

[力扣](https://leetcode.cn/problems/number-of-great-partitions/)

题目要求将数组中的数分成两个部分，且每个部分中的数值之和都不小于k，问可行的划分方案数量。

这是一个非常标准的01背包问题，但是数组中数的取值范围很大，因此不能直接使用常规的动态规划进行求解。注意到题目中的k取值范围比较小，因此可以考虑逆向求解，也就是求出所有不合法的划分方法，然后使用划分的总方案数减去不合法的划分方法得到最终答案。

题目中所有划分的总方案数为2^n，这里的n为数组的长度，而不合法的划分方案数则可以通过动态规划进行求解。令f[i][j]表示前i个数，从中选择若干个数的和为j的方案数，这里j的取值范围在0到k - 1之间。那么就有

f\[i\]\[j\] \= f\[i - 1\]\[j\] + f\[i - 1\]\[j - nums\[i - 1\]\]

需要特别注意的是，在这里可能会出现重复计算的情况，例如满足p \< k且q \< k的f[n - 1][p]和f[n - 1][q]，其中p的构成可能和q的构成恰好互补，也就是构成q的这些数恰好就是原数组中去除掉构成p的这些数，此时就产生了重复的计数。不过对于这种情况处理方法也很简单，因为这种情况下p和q都小于k，说明原始数组之和小于2k的，是不存在合法的划分的，对于这种情况可以直接返回0。而对于原始数组之和大于等于2k的情况，若其中的某个划分之和p小于k，那么剩余数之和必然是大于k的，同样不会出现上面p和q重复计数的情况。

具体实现时，由于f的每一轮计算只与上一轮有关，因此可以通过滚动数组以及倒序计算省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def countPartitions(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        if sum(nums) < k + k:
            return 0
        
        f = [0] * k
        f[0] = 1
        mod = 10 ** 9 + 7
        for num in nums:
            for index in range(k - 1, num - 1, -1):
                f[index] += f[index - num]
                if f[index] >= mod:
                    f[index] -= mod
        
        def quickPow(base, x):
            if x == 1:
                return base
            
            p = quickPow(base, x / 2)
            p *= p
            if x & 1:
                p *= base
            return p % mod

        res = quickPow(2, len(nums))
        for index in range(k):
            res -= f[index]
            if res < 0:
                res += mod
            
            res -= f[index]
            if res < 0:
                res += mod
        
        return res
```
