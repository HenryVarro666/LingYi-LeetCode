---
title: "2926. 平衡子序列的最大和"
aliases: ["yiduobo的每日leetcode 2926.平衡子序列的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690271921"
zhihu_id: "690271921"
zhihu_title: "yiduobo的每日leetcode 2926.平衡子序列的最大和"
question_id: "2926"
question: "平衡子序列的最大和"
problem_url: "https://leetcode.cn/problems/maximum-balanced-subsequence-sum/"
difficulty: "Hard"
rating: 2448
created: "2024-04-02T02:00:32+08:00"
updated: "2024-04-02T02:00:32+08:00"
upvotes: 1
comments: 0
---

# 2926. 平衡子序列的最大和

> **[yiduobo的每日leetcode 2926.平衡子序列的最大和](https://zhuanlan.zhihu.com/p/690271921) · 知乎 · 2024-04-02 · 赞同 1**
> 力扣：[2926. 平衡子序列的最大和](https://leetcode.cn/problems/maximum-balanced-subsequence-sum/) · Hard · 灵茶山艾府：[树状数组优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2926.平衡子序列的最大和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-balanced-subsequence-sum/description/)

首先观察题目中对于平衡子序列的定义，要求的事nums[i] - nums[j] >\= i - j。对于这类数值和下标同时相减的式子，一个经典的处理方法就是将数值和下标归类到一起，也就是将式子变形成nums[i] - i >\= nums[j] - j。到了这里，就可以得到一个差值数组diff，题目就变成了从diff中找出一个不降子序列，要求这个子序列对应的原nums项的数值之和最大。

对于不降子序列问题，如果是求最长，那么可以利用贪心加二分来处理，但是本题要求的是对应原nums数值之和最大的子序列，那么只能先考虑经典的动态规划。

令f[i]表示以diff[i]结尾的最大子序列之和，那么对于f[i]，就需要从0遍历到i - 1，找出其中满足diff[j] \<\= diff[i]中最大的f[j]，然后用这个f[j] + nums[i]来更新f[i]。

上面这个做法是O(n^2)的，在本题的数据规模下显然是行不通的，需要进行优化。

可以发现，上面做法在状态转移时需要高效获取到所有diff值满足条件的f\[j\]，那么在这里不妨直接将状态改成diff值，也就是说令g\[j\]表示以diff值为j结尾的子序列的最大和。在这里由于diff的取值范围过大，因此需要先将其离散化之后映射到序上，也就是说将diff的取值范围收紧到1到n之间，接下来对于当前的diff\[i\]，就可以用max(g\[1\], g\[1\], ..., g\[diff\[i\]\]) + nums\[j\]来更新答案了。

这个做法看上去依然是O(n^2)的，不过状态转移中max(g\[1\], ..., g\[diff\[i\]\])这一段是一个标准的动态前缀最大值，利用树状数组就可以很便捷地优化到O(logn)。

到了这里，就得到了一种O(nlogn)的做法：

首先，利用nums[i] - i计算出diff数组，然后将其中的数值排序后建立diff数组到序的映射mapping。

接下来遍历原数组，对于当前的diff\[i\]和nums\[i\]，通过树状数组求解出之前所有diff序小于等于mapping\[diff\[i\]\]的子序列的最大值left_max，利用left_max + nums\[i\]更新答案以及树状数组即可。

另外在具体实现上，对于负数可以做一些特殊处理。如果nums中全都是负数，那么最终答案显然就是最大的那个负数，可以直接返回；反之，最终答案中一定不会包含负数，也就是说在求解过程中可以无视nums中的负数。

最后附上python代码：

```python
class Solution(object):
    def maxBalancedSubsequenceSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set()
        flag = False
        for index, v in enumerate(nums):
            if v > 0:
                flag = True
                num_set.add(v - index)
        
        mapping = {}
        num_list = sorted(list(num_set))
        for index, v in enumerate(num_list):
            mapping[v] = index + 1
        
        if not flag:
            return max(nums)

        f = [0] * (len(num_list) + 1)

        def add(x, v):
            while x <= len(num_list):
                f[x] = max(f[x], v)
                x += x & -x
        
        def get(x):
            ma = 0
            while x:
                ma = max(ma, f[x])
                x -= x & -x
            return ma

        res = 0
        for index, v in enumerate(nums):
            if v > 0:
                left_max = get(mapping[v - index])
                res = max(res, left_max + v)
                add(mapping[v - index], left_max + v)
        
        return res
```
