---
title: "2771. 构造最长非递减子数组"
aliases: ["yiduobo的每日leetcode 2771.构造最长非递减子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655463930"
zhihu_id: "655463930"
zhihu_title: "yiduobo的每日leetcode 2771.构造最长非递减子数组"
question_id: "2771"
question: "构造最长非递减子数组"
problem_url: "https://leetcode.cn/problems/longest-non-decreasing-subarray-from-two-arrays/"
difficulty: "Medium"
rating: 1792
created: "2023-09-11T05:03:26+08:00"
updated: "2023-09-11T05:03:26+08:00"
upvotes: 0
comments: 0
---

# 2771. 构造最长非递减子数组

> **[yiduobo的每日leetcode 2771.构造最长非递减子数组](https://zhuanlan.zhihu.com/p/655463930) · 知乎 · 2023-09-11 · 赞同 0**
> 力扣：[2771. 构造最长非递减子数组](https://leetcode.cn/problems/longest-non-decreasing-subarray-from-two-arrays/) · Medium · 灵茶山艾府：[动态规划：从记忆化搜索到递推，再到空间优化](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2771.构造最长非递减子数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/longest-non-decreasing-subarray-from-two-arrays/)

动态规划的题目，令f[i]和g[i]分别表示由nums1[i]和nums2[i]结尾的最长递减子数组长度。

首先可以初始化f[0] \= g[0] \= 1，接下来从下标1开始向后遍历。

对于当前遍历到的f[i]和g[i]，若nums1[i] >\= nums1[i - 1]，就可以在f[i - 1]的基础上加入nums1[i]，那么就有f[i] \= max(f[i], f[i - 1] + 1)。另一方面，若nums1[i] >\= nums2[i - 1]，就可以在g[i - 1]的基础上加入nums1[i]，那么就有f[i] \= max(f[i], g[i - 1] + 1)。若都不满足，就只能是f[i] \= 1，表示这个子数组中只有nums1[i]这一个数。

对于g[i]，转移方程与f[i]类似，检测的应该是nums2[i]与nums1[i - 1]以及nums2[i - 1]的大小关系。

在计算过程中，每一轮都使用当前的f[i]和g[i]更新最终答案。

另外由于f和g每一轮都只与上一轮有关，因此可以使用变量迭代省去数组的空间开销。

最后附上python代码：

```python
class Solution(object):
    def maxNonDecreasingLength(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        f = g = res = 1
        for index in range(1, len(nums1)):
            pre_f, pre_g = f, g
            
            f = g = 1

            if nums1[index] >= nums1[index - 1]:
                f = max(pre_f + 1, f)
            if nums1[index] >= nums2[index - 1]:
                f = max(pre_g + 1, f)
            
            if nums2[index] >= nums2[index - 1]:
                g = max(pre_g + 1, g)
            if nums2[index] >= nums1[index - 1]:
                g = max(pre_f + 1, g)
        
            res = max(res, f, g)
        
        return res
```
