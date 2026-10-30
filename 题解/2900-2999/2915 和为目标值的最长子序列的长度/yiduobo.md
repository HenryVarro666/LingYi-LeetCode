---
title: "2915. 和为目标值的最长子序列"
aliases: ["yiduobo的每日leetcode 2915.和为目标值的最长子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664807231"
zhihu_id: "664807231"
zhihu_title: "yiduobo的每日leetcode 2915.和为目标值的最长子序列"
question_id: "2915"
question: "和为目标值的最长子序列的长度"
problem_url: "https://leetcode.cn/problems/length-of-the-longest-subsequence-that-sums-to-target/"
difficulty: "Medium"
rating: 1659
created: "2023-11-03T04:09:02+08:00"
updated: "2023-11-03T04:09:02+08:00"
upvotes: 2
comments: 0
---

# 2915. 和为目标值的最长子序列

> **[yiduobo的每日leetcode 2915.和为目标值的最长子序列](https://zhuanlan.zhihu.com/p/664807231) · 知乎 · 2023-11-03 · 赞同 2**
> 力扣：[2915. 和为目标值的最长子序列的长度](https://leetcode.cn/problems/length-of-the-longest-subsequence-that-sums-to-target/) · Medium · 灵茶山艾府：[恰好装满型 0-1 背包：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2915.和为目标值的最长子序列

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/length-of-the-longest-subsequence-that-sums-to-target/)

非常标准的背包问题。令f\[i\]\[j\]表示前i个数中选取若干个数使得和为j时最多可以选多少个数，那么对于f\[i\]\[j\]，就有f\[i\]\[j\] \= max(f\[i\]\[j\], f\[i - 1\]\[j - nums\[i\]\])，这里j的取值范围在nums\[i\]到target之间。计算完成后，f\[-1\]\[target\]即为最终答案。

另外，对于这类背包问题，一般都会通过倒序遍历j而不是常规的滚动数组来优化掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def lengthOfLongestSubsequence(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        f = [-1] * (target + 1)
        f[0] = 0
        for v in nums:
            for index in range(target, v - 1, -1):
                if f[index - v] >= 0 and f[index] < f[index - v] + 1:
                    f[index] = f[index - v] + 1
                    
        return f[-1]
```
