---
title: "3584. 子序列首尾元素的最大乘积"
aliases: ["yiduobo的每日leetcode 3584.子序列首尾元素的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/enumeration", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1938730106588726924"
zhihu_id: "1938730106588726924"
zhihu_title: "yiduobo的每日leetcode 3584.子序列首尾元素的最大乘积"
question_id: "3584"
question: "子序列首尾元素的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/"
difficulty: "Medium"
rating: 1763
created: "2025-08-12T22:48:53+08:00"
updated: "2025-08-12T22:48:53+08:00"
upvotes: 2
comments: 0
---

# 3584. 子序列首尾元素的最大乘积

> **[yiduobo的每日leetcode 3584.子序列首尾元素的最大乘积](https://zhuanlan.zhihu.com/p/1938730106588726924) · 知乎 · 2025-08-12 · 赞同 2**
> 力扣：[3584. 子序列首尾元素的最大乘积](https://leetcode.cn/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/) · Medium · 灵茶山艾府：[脑筋急转弯 + 枚举右维护左，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3584.子序列首尾元素的最大乘积

[3584. 子序列首尾元素的最大乘积 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/description/)

题目给出一个整数数组nums以及一个整数m，现在要求返回nums的所有大小为m的子序列中，首尾元素乘积的最大值。

对于nums中所有的子序列而言，其最后一个元素的下标必然在m - 1到n - 1之间，其中n为nums的长度，那么在这里就可以对这些下标进行一趟遍历，检测以当前遍历到的下标index为最后一个元素时的子序列的首尾元素乘积的最大值。

对于当前遍历到的下标index，如果子序列中至少有m个元素，那么其左边界的下标p必然小于等于index - m + 1，也就是说在这里应该从0到index - m + 1之间选出一个最合适的元素作为子序列的起点。为了使得其与nums[index]的乘积最大，那么当nums[index]为正数时，就应该选择nums[0]到nums[index - m + 1]之间的最大值作为起点，反之则应该选择nums[0]到nums[index - m + 1]之间的最小值作为起点。

基于这个结论，就可以使用两个变量mi和ma分别维护nums[0]到nums[index - m + 1]之间的最小值和最大值，对于当前遍历到的nums[index]，先使用nums[index - m + 1]来更新ma和mi，然后使用ma \* nums[index]和mi \* nums[index]中的较大值来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumProduct(self, nums, m):
        """
        :type nums: List[int]
        :type m: int
        :rtype: int
        """
        
        res = None
        mi = nums[0]
        ma = nums[0]
        for index, v in enumerate(nums[m - 1:], m - 1):
            mi = min(mi, nums[index - m + 1])
            ma = max(ma, nums[index - m + 1])
            
            best = max(v * ma, v * mi)
            if res is None or res < best:
                res = best
        
        return res
```
