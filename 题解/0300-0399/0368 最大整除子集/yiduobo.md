---
title: "368. 最大整除子集"
aliases: ["yiduobo的每日leetcode 368.最大整除子集"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165141597"
zhihu_id: "165141597"
zhihu_title: "yiduobo的每日leetcode 368.最大整除子集"
question_id: "368"
question: "最大整除子集"
problem_url: "https://leetcode.cn/problems/largest-divisible-subset/"
difficulty: "Medium"
rating: 1800
created: "2020-07-29T22:08:55+08:00"
updated: "2020-07-29T22:08:55+08:00"
upvotes: 0
comments: 0
---

# 368. 最大整除子集

> **[yiduobo的每日leetcode 368.最大整除子集](https://zhuanlan.zhihu.com/p/165141597) · 知乎 · 2020-07-29 · 赞同 0**
> 力扣：[368. 最大整除子集](https://leetcode.cn/problems/largest-divisible-subset/) · Medium · 灵茶山艾府：[三种方法：记忆化搜索/递推/最优性优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

368.最大整除子集<https://leetcode-cn.com/problems/largest-divisible-subset/>

设当前某个整除子集S，其中最大的元素为S_max，那么一定满足S_max % Sk \= 0，其中Sk为S中的任意元素。

那么对于新来的一个x，若x % S_max \= 0，那么对于任意的Sk，一定有x % Sk \= 0，这就意味着将x加入S之后一定也是整除子集。当x % S_max !\= 0时，显然将x加入S之后就不再是整除子集了。

于是一个自然的想法就是将nums按从小到大的顺序先排好序，然后设f[i]为以nums[i]为最大元素的整除子集中，元素数量最多的那一个。

对于f[i]，有f[i] \= f[j] + 1，其中j \< i且nums[i] % nums[j] \= 0。

由于题目要求找出具体的子集元素，那么还需要使用一个fa数组，表示在当前元素加入最大子集之前，最大子集中最大的元素是多少。

排序的复杂度为O(nlogn)，dp的时间复杂度为O(n^2)，因此最终的时间复杂度为O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def largestDivisibleSubset(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        nums = sorted(nums)
        f = [1] * len(nums)
        fa = [None] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] % nums[j] == 0 and f[j] + 1 > f[i]:
                    f[i] = f[j] + 1
                    fa[i] = j

        pos = None
        for i in range(len(nums)):
            if pos is None or f[i] > f[pos]:
                pos = i

        res = []
        while pos is not None:
            res.append(nums[pos])           
            pos = fa[pos]

        return res
```
