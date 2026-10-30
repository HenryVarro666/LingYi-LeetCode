---
title: "3892. 产生至少K个峰值的最少操作次数"
aliases: ["yiduobo的每日leetcode 3892.产生至少K个峰值的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/五-堆-优先队列", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2024599133869077877"
zhihu_id: "2024599133869077877"
zhihu_title: "yiduobo的每日leetcode 3892.产生至少K个峰值的最少操作次数"
question_id: "3892"
question: "产生至少 K 个峰值的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-achieve-at-least-k-peaks/"
difficulty: "Hard"
rating: 2280
created: "2026-04-07T22:34:56+08:00"
updated: "2026-04-07T22:34:56+08:00"
upvotes: 1
comments: 0
---

# 3892. 产生至少K个峰值的最少操作次数

> **[yiduobo的每日leetcode 3892.产生至少K个峰值的最少操作次数](https://zhuanlan.zhihu.com/p/2024599133869077877) · 知乎 · 2026-04-07 · 赞同 1**
> 力扣：[3892. 产生至少 K 个峰值的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-achieve-at-least-k-peaks/) · Hard · 灵茶山艾府：[环形打家劫舍：记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3892.产生至少K个峰值的最少操作次数

<https://leetcode.cn/problems/minimum-operations-to-achieve-at-least-k-peaks/description/>

题目给出一个长度为n的循环整数数组nums。

若下标index对应的值严格大于其相邻元素，则该下标是一个峰值。需要注意，这里的nums是循环数组，因此对于所有的index > 0，其前一个相邻元素是nums[index - 1]，否则是nums[n - 1]。同理，若index \< n - 1，那么其后一个相邻元素是nums[index + 1]，否则是nums[0]。

现在可以执行任意次操作，每次操作中，可以选择任意下标index，并将nums[index]加上1。

问使得数组包含至少k个峰值所需的最小操作次数。若不可能，则返回-1。

本题中峰值的定义和上一题的特殊下标其实是一样的，同时可以执行的操作也是一样的，因此将nums[index]变成峰值所需操作次数的计算方式也一样，即

cost[index] \= max(max(nums[(index - 1 + n) % n], nums[(index + 1) % n]) + 1 - nums[index], 0)

这里需要处理循环数组的下标循环。

不过与上一题不同的是，本题中需要计算的是至少k个峰值，而不是峰值尽量多，因此不能再使用贪心的做法，必须使用动态规划进行求解。

在正式开始之前，可以先处理边界情况。

首先，若k为0，那么无需任何操作，此时答案必然为0。

接下来，由于本题中是循环数组，因此可以形成的峰值的数量上限应该是n // 2，若k大于n // 2，那么答案就是-1。

接下来再考虑一般情况。由于循环的存在，如果选择了让0成为峰值，那么n - 1就不能再成为峰值，这一点会影响到动态规划的执行，因此才这里可以分情况进行讨论。

令f[index][p]和g[index][p]分别表示让0成为峰值/不让0成为峰值时，前index个下标中至少具有p个峰值所需的最小操作次数，那么对于f[index][p]以及g[index][p]，可以先设置f[0][0]、f[1][0]、g[0][0]、g[1][0]都为0，同时设置f[1][1]为cost[0]，表示将nums中的第一个元素，也就是nums[0]变为峰值的代价。

接下来index从2到n遍历，p从0到k遍历，对于当前遍历到的f[index][p]以及g[index][p]：

1、若p为0：

此时显然有f[index][p] \= 0以及g[index][p] \= 0

2、若p > 0：

首先可以初始化f[index][p]为f[index - 1][p]，g[index][p]为g[index - 1][p]，表示不操作nums[index - 1]这个元素。

另外，如果要将nums[index - 1]变为峰值，那么就不能操作nums[index - 2]，因此只有当f[index - 2][p - 1]存在时，才能用f[index - 2][p - 1] + cost[index - 1]来更新f[index][p]，g[index][p]同理，只有当g[index - 2][p - 1]存在时，才能使用g[index - 2][p - 1] + cost[index - 1]来更新g[index][p]。

需要注意的是，根据上面的定义，对于f数组不能操作下标1和下标n - 1，因此只有当index不为n也不为2时，才能使用上面的转移方程更新f[index][p]。

全部计算完成后，min(f[-1][k], g[-1][k])即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        if k == 0:
            return 0

        n = len(nums)
        if k > n // 2:
            return -1
        
        f = [[None] * (k + 1) for _ in range(n + 1)]
        g = [[None] * (k + 1) for _ in range(n + 1)]

        cost = [max(max(nums[(index - 1 + n) % n], nums[(index + 1) % n]) + 1 - nums[index], 0) for index in range(n)]
        f[0][0] = 0
        g[0][0] = 0
        f[1][0] = 0
        f[1][1] = cost[0]
        g[1][0] = 0

        for index in range(2, n + 1):
            for p in range(k + 1):
                if p == 0:
                    f[index][p] = 0
                    g[index][p] = 0
                else:
                    f[index][p] = f[index - 1][p]
                    g[index][p] = g[index - 1][p]

                    if g[index - 2][p - 1] is not None and (g[index][p] is None or g[index][p] > g[index - 2][p - 1] + cost[index - 1]):
                        g[index][p] = g[index - 2][p - 1] + cost[index - 1]
                    if index != n and index != 2 and f[index - 2][p - 1] is not None and (f[index][p] is None or f[index][p] > f[index - 2][p - 1] + cost[index - 1]):
                        f[index][p] = f[index - 2][p - 1] + cost[index - 1]
        
        return min(f[-1][k], g[-1][k])
```
