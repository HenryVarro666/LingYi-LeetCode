---
title: "3755. 最大平衡异或子数组的长度"
aliases: ["yiduobo的每日leetcode 3755.最大平衡异或子数组的长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976050568746258455"
zhihu_id: "1976050568746258455"
zhihu_title: "yiduobo的每日leetcode 3755.最大平衡异或子数组的长度"
question_id: "3755"
question: "最大平衡异或子数组的长度"
problem_url: "https://leetcode.cn/problems/find-maximum-balanced-xor-subarray-length/"
difficulty: "Medium"
created: "2025-11-25T22:05:04+08:00"
updated: "2025-11-25T22:05:04+08:00"
upvotes: 0
comments: 0
---

# 3755. 最大平衡异或子数组的长度

> **[yiduobo的每日leetcode 3755.最大平衡异或子数组的长度](https://zhuanlan.zhihu.com/p/1976050568746258455) · 知乎 · 2025-11-25 · 赞同 0**
> 力扣：[3755. 最大平衡异或子数组的长度](https://leetcode.cn/problems/find-maximum-balanced-xor-subarray-length/) · Medium · 灵茶山艾府：[前缀和与哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3755.最大平衡异或子数组的长度

[3755. 最大平衡异或子数组的长度 - 力扣（LeetCode）](https://leetcode.cn/problems/find-maximum-balanced-xor-subarray-length/description/)

题目给出一个整数数组nums，要求返回同时满足一下两个条件的最长子数组的长度：

1、子数组的按位异或结果为0

2、子数组中奇数与偶数的数量相等

若不存在合法的子数组，则返回0。

对于一个区间[left, right]，若nums[left: right + 1]的异或值为0，且其中奇数与偶数的数量相同，那么就说明nums[:left]的异或值与nums[:right + 1]的异或值相同，同时这两个前缀数组中偶数与奇数数量之差也相同。

换言之，对于某个下标index，不妨设nums[index + 1]的异或值为xor，其中偶数与奇数的数量之差为diff，那么就只需想办法找出(xor, diff)这个组合第一次出现的位置p，而nums[p + 1: index + 1]就是以index结尾的最长合法子数组。

基于上面的结论，就只需要一趟遍历，使用两个变量xor以及diff分别记录前缀异或值以及前缀中偶数与奇数的数量之差，另外使用一个哈希表first记录每种(xor, diff)的组合首次出现的下标位置。

对于当前遍历到的元素nums[index]，先用其更新xor以及diff，然后对于当前的(xor, diff)，若其在first中出现过，就可以使用index - first[(xor, diff)]来更新答案，否则将first[(xor, diff)]更新为index即可。

最后附上python代码：

```python
class Solution(object):
    def maxBalancedSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        first = {(0, 0): -1}
        diff = 0
        xor = 0
        res = 0
        for index, v in enumerate(nums):
            xor ^= v
            if v % 2 == 0:
                diff += 1
            else:
                diff -= 1
            
            key = (xor, diff)
            if key in first:
                res = max(res, index - first[key])
            else:
                first[key] = index
        
        return res
```
