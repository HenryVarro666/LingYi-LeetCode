---
title: "3825. 按位与结果非零的最长上升子序列"
aliases: ["yiduobo的每日leetcode 3825.按位与结果非零的最长上升子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2001441411271267929"
zhihu_id: "2001441411271267929"
zhihu_title: "yiduobo的每日leetcode 3825.按位与结果非零的最长上升子序列"
question_id: "3825"
question: "按位与结果非零的最长上升子序列"
problem_url: "https://leetcode.cn/problems/longest-strictly-increasing-subsequence-with-non-zero-bitwise-and/"
difficulty: "Medium"
rating: 1846
created: "2026-02-03T00:23:31+08:00"
updated: "2026-02-03T00:23:35+08:00"
upvotes: 1
comments: 0
---

# 3825. 按位与结果非零的最长上升子序列

> **[yiduobo的每日leetcode 3825.按位与结果非零的最长上升子序列](https://zhuanlan.zhihu.com/p/2001441411271267929) · 知乎 · 2026-02-03 · 赞同 1**
> 力扣：[3825. 按位与结果非零的最长上升子序列](https://leetcode.cn/problems/longest-strictly-increasing-subsequence-with-non-zero-bitwise-and/) · Medium · 灵茶山艾府：[枚举比特位 + LIS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3825.按位与结果非零的最长上升子序列

<https://leetcode.cn/problems/longest-strictly-increasing-subsequence-with-non-zero-bitwise-and/description/>

题目给出一个非负整数数组nums，其长度不超过10^5，其中的元素大小不超过10^9。要求找出nums中按位与结果非零的最长严格递增子序列的长度。

题目要求找出一个单调递增子序列，这个子序列的元素按位与结果非零，且长度最长。

子序列中的元素按位与结果非零，说明至少存在一个二进制位，子序列中的所有元素在这个位上都为1。由于其中元素的大小不超过10^9，也就是说所有元素的二进制表示长度都不超过30，因此可以先遍历具体的二进制位，将nums中所有在这个位上为1的元素提取出来，然后对于提取出来的数组，计算其中最长上升子序列的长度并更新答案就行了。

对于最长上升子序列的计算，则可以使用经典的贪心加二分法，在这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequence(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = max(nums)
        p2 = [1]
        while p2[-1] < ma:
            p2.append(p2[-1] + p2[-1])
        
        res = 0
        for v in p2:
            f = []
            for x in nums:
                if (x & v) == v:
                    if not f or f[-1] < x:
                        f.append(x)
                    else:
                        left = 0
                        right = len(f) - 1
                        while left < right:
                            mid = (left + right) // 2
                            if f[mid] < x:
                                left = mid + 1
                            else:
                                right = mid
                        f[left] = x
            
            res = max(res, len(f))
        
        return res
```
