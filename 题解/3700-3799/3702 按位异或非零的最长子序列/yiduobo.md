---
title: "3702. 按位异或非零的最长子序列"
aliases: ["yiduobo的每日leetcode 3702.按位异或非零的最长子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/brainteaser", "题单/位运算", "题单/贪心算法", "题单/位运算/二-异或-XOR-的性质", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1958247667579725715"
zhihu_id: "1958247667579725715"
zhihu_title: "yiduobo的每日leetcode 3702.按位异或非零的最长子序列"
question_id: "3702"
question: "按位异或非零的最长子序列"
problem_url: "https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/"
difficulty: "Medium"
rating: 1489
created: "2025-10-06T22:45:44+08:00"
updated: "2025-10-06T22:45:45+08:00"
upvotes: 0
comments: 0
---

# 3702. 按位异或非零的最长子序列

> **[yiduobo的每日leetcode 3702.按位异或非零的最长子序列](https://zhuanlan.zhihu.com/p/1958247667579725715) · 知乎 · 2025-10-06 · 赞同 0**
> 力扣：[3702. 按位异或非零的最长子序列](https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3702.按位异或非零的最长子序列

[3702. 按位异或非零的最长子序列 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-subsequence-with-non-zero-bitwise-xor/description/)

题目给出一个整数数组nums。要求返回nums中按位异或计算结果非零的最长子序列的长度。若不存在这样的子序列，返回0。

题目要求找出尽量长的子序列，那么最理想的情况自然就是选取整个nums数组，当然前提是按位异或的结果不为0。若按位异或的结果为0，则需要去掉其中某一个非零的元素，这样一来异或结果就会变为非零，因此这种情况下答案应该是nums的长度减一。

需要特别注意的是，有一种特殊情况是nums中全为0，这种情况下数组异或结果为0，且找不出非零元素，不过对于这种情况，选出来的任意子序列都是由全0组成的，其异或结果必然为0，根据题意，此时可以直接返回0。而对于其他情况，则只需按照上面的结论进行处理即可。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequence(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        xor = 0
        all_zero = True
        for v in nums:
            xor ^= v
            if v > 0:
                all_zero = False
        
        if xor > 0:
            return len(nums)
        
        if all_zero:
            return 0
            
        return len(nums) - 1
```
