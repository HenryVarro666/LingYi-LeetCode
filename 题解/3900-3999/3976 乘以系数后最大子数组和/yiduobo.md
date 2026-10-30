---
title: "3976. 乘以系数后最大子数组和"
aliases: ["yiduobo的每日leetcode 3976.乘以系数后最大子数组和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054649031750693494"
zhihu_id: "2054649031750693494"
zhihu_title: "yiduobo的每日leetcode 3976.乘以系数后最大子数组和"
question_id: "3976"
question: "乘以系数后最大子数组和"
problem_url: "https://leetcode.cn/problems/maximum-subarray-sum-after-multiplier/"
difficulty: "Medium"
rating: 1981
created: "2026-06-29T21:31:38+08:00"
updated: "2026-06-29T21:31:42+08:00"
upvotes: 0
comments: 0
---

# 3976. 乘以系数后最大子数组和

> **[yiduobo的每日leetcode 3976.乘以系数后最大子数组和](https://zhuanlan.zhihu.com/p/2054649031750693494) · 知乎 · 2026-06-29 · 赞同 0**
> 力扣：[3976. 乘以系数后最大子数组和](https://leetcode.cn/problems/maximum-subarray-sum-after-multiplier/) · Medium · 灵茶山艾府：[状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3976.乘以系数后最大子数组和

<https://leetcode.cn/problems/maximum-subarray-sum-after-multiplier/>

题目给出一个整数数组nums以及一个正整数k。

现在要求选择nums中的一个子数组并执行一下操作之一：

1、将所选子数组中的每个数字都乘以k

2、将所选子数组中的每个数字都除以k，其中正数除以k时结果向下取整，负数除以k时结果向上取整

问最终可能得到的非空子数组和最大是多少。

乍一看感觉可以用贪心，但是仔细分析发现贪心需要处理的情况非常复杂，并不好些。

首先，如果选择乘法操作，那么当原数组中的最大子段和大于0时，显然就应该乘在这个最大子段和上。若小于0，那么就不应该执行乘法操作。

而对于除法操作则复杂得到，不妨先考虑下为什么选择执行除法而不是执行乘法——理由就是，通过除法操作，可以有效减少连接段中负数的负面作用，从而以较小的代价连接起两侧的正子段和。

以数组[2, -1, -1, -1, 2, -1, -1, -1, 2, -1, -1, -1, 2, -1, -1, -1, 2, -100, 3]，k \= 2为例。

对于这个数组，先考虑原数组的最大子段和。由于中间都是三个连续的-1，因此选择连结2是不划算的，最大子段和就是最后的3，选择乘法操作此时得到的答案就是3 \* 2 \= 6。

然而对于中间的连续-1，在选择除法的前提下，这些-1都将变为0，如果选择第一个2与最后一个2之间的部分执行除法操作，那么得到的就是[2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 2, -100, 3]，显然在这里应该选择第一个2和最后一个2之间的部分，最终答案就是7。

可以发现，除法操作生效的部分是非常不好界定的，因此贪心具体应该怎么贪是很难确定的。

贪心不好使，那么就自然考虑使用动态规划。动态规划的状态切分显然是按前若干个元素进行的，而对于题目中的操作，可以分为四种，因此可以令f[index]、m[index]、d[index]、g[index]分别表示对于nums[0]到nums[index]：

- f[index]表示目前还没有执行操作的最大子段和。这意味着接下来可以继续保持不执行操作，也可以选择执行乘法或除法操作中的任意一种。
- m[index]表示已经执行了乘法操作，且nums[index]是最后一个执行乘法操作的元素。这意味着接下来不能执行除法操作。
- d[index]表示已经执行了除法操作，且nums[index]是最后一个执行除法操作的元素。这意味着接下来不能执行乘法操作。
- g[index]表示已经执行了乘法或者除法操作，且执行的子段已经结束，nums[index]回归到了不执行操作。这意味着接下来只能选择不执行操作。

根据上面的转移限制，对于这四种状态就有：

- f[index] \= max(0, f[index - 1]) + nums[index]
- m[index] \= max(0, f[index - 1], m[index - 1]) + nums[index] \* k
- d[index] \= max(0, f[index - 1], d[index - 1]) + nums[index] // k
- g[index] \= max(m[index - 1], d[index - 1], g[index - 1]) + nums[index]

需要注意，每一轮都需要使用f[index]、m[index]、d[index]、g[index]中的最大值更新答案。

另外注意到转移方程每一轮都只与上一轮有关，因此可以使用变量迭代省去数组的开销。

最后附上python代码：

```python
class Solution(object):
    def maxSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        def div(x):
            if x >= 0:
                return x // k
            return -(-x // k)
        
        f = nums[0]
        m = nums[0] * k
        d = div(nums[0])
        g = None

        res = max(f, m, d)

        for v in nums[1:]:
            nxt_f = max(f, 0) + v
            nxt_m = max(f, m, 0) + v * k
            nxt_d = max(f, d, 0) + div(v)
            nxt_g = max(m, d) + v
            if g is not None:
                nxt_g = max(nxt_g, g + v)
            f, m, d, g = nxt_f, nxt_m, nxt_d, nxt_g
            res = max(res, f, m, d, g)
        
        return res
```
