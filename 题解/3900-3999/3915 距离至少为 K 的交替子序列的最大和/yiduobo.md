---
title: "3915. 距离至少为K的交替子序列的最大和"
aliases: ["yiduobo的每日leetcode 3915.距离至少为K的交替子序列的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2033287328995743499"
zhihu_id: "2033287328995743499"
zhihu_title: "yiduobo的每日leetcode 3915.距离至少为K的交替子序列的最大和"
question_id: "3915"
question: "距离至少为 K 的交替子序列的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-alternating-subsequence-with-distance-at-least-k/"
difficulty: "Hard"
rating: 2288
created: "2026-04-30T21:03:24+08:00"
updated: "2026-04-30T21:03:28+08:00"
upvotes: 1
comments: 0
---

# 3915. 距离至少为K的交替子序列的最大和

> **[yiduobo的每日leetcode 3915.距离至少为K的交替子序列的最大和](https://zhuanlan.zhihu.com/p/2033287328995743499) · 知乎 · 2026-04-30 · 赞同 1**
> 力扣：[3915. 距离至少为 K 的交替子序列的最大和](https://leetcode.cn/problems/maximum-sum-of-alternating-subsequence-with-distance-at-least-k/) · Hard · 灵茶山艾府：[值域树状数组优化状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3915.距离至少为K的交替子序列的最大和

<https://leetcode.cn/problems/maximum-sum-of-alternating-subsequence-with-distance-at-least-k/description/>

题目给出一个长度为n的整数数组nums，其长度以及其中元素的大小都不超过10^5。另外给出一个整数k。

现在要求找出一个子序列，要求

- 任意两项的下标之差必须大于等于k
- 所选的值必须构成严格交替的子序列，即
   - nums[index0] \< nums[index1] > nums[index2] \< nums[index3] > ...，或者
   - nums[index0] > nums[index1] \< nums[index2] > nums[index3] \< ...

长度为1的子序列也被认为是严格交替的。另外一个有效的子序列的得分为其所选元素值的总和。

现在要求返回一个整数，表示有效子序列可能取得的最大得分。

以题目的数据规模来看，只能考虑贪心或者动态规划。贪心在这里看上去不太行，因此将目标聚焦在动态规划上。令f[index]以nums[index]结尾，且nums[index]是峰值的子序列的最大和，而g[index]则表示以nums[index]结尾，且nums[index]为谷值的子序列的最大和。

那么对于f[index]和g[index]，很容易写出转移方程：

f[index] \= max(g[p]) + nums[index]，这里的p必须满足index - p >\= k，且nums[p] \< nums[index]

g[index] \= max(f[p]) + nums[index]，这里的p必须满足index - p >\= k，且nums[p] > nums[index]

这样一来，就得到了一种O(n^2)的算法，接下来需要想办法进行优化。

注意到nums中元素的大小不超过10^5，而转移方程中出现的实际上是一个受到值域限制的前缀最大值，那么在这里就可以使用两个树状数组分别维护g和f的前缀最大值，其中f对应的树状数组记录的是大于某个值的最大值，而g对应的树状数组记录的则是小于某个值的最大值。

当index向后移动时，先使用f[index - p]以及g[index - p]更新这两个树状数组，然后反过来，使用另一个树状数组来更新f[index]以及g[index]即可。

最后附上python代码：

```python
class Solution(object):
    def maxAlternatingSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)
        ma = max(nums) + 1
        f = []
        g = []
        tf = [0] * (ma + 1)
        tg = [0] * (ma + 1)

        res = 0

        for v in nums[:k]:
            f.append(v)
            g.append(v)
            res = max(res, v)
        
        def update(p, v, t):
            while p <= ma:
                t[p] = max(t[p], v)
                p += p & -p
        
        def get(p, t):
            res = 0
            while p > 0:
                res = max(res, t[p])
                p -= p & -p
            return res

        for index, v in enumerate(nums[k:], k):
            update(ma - nums[index - k], f[index - k], tf)
            update(nums[index - k] + 1, g[index - k], tg)
            f.append(get(v, tg) + v)
            g.append(get(ma - v - 1, tf) + v)
            res = max(res, f[-1], g[-1])
        
        return res
```
