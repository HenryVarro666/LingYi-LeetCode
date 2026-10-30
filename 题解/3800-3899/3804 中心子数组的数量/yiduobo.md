---
title: "3804. 中心子数组的数量"
aliases: ["yiduobo的每日leetcode 3804.中心子数组的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1993701759726671700"
zhihu_id: "1993701759726671700"
zhihu_title: "yiduobo的每日leetcode 3804.中心子数组的数量"
question_id: "3804"
question: "中心子数组的数量"
problem_url: "https://leetcode.cn/problems/number-of-centered-subarrays/"
difficulty: "Medium"
created: "2026-01-13T02:41:03+08:00"
updated: "2026-01-13T02:41:06+08:00"
upvotes: 1
comments: 0
---

# 3804. 中心子数组的数量

> **[yiduobo的每日leetcode 3804.中心子数组的数量](https://zhuanlan.zhihu.com/p/1993701759726671700) · 知乎 · 2026-01-13 · 赞同 1**
> 力扣：[3804. 中心子数组的数量](https://leetcode.cn/problems/number-of-centered-subarrays/) · Medium · 灵茶山艾府：[枚举所有子数组 + 哈希集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3804.中心子数组的数量

[3804. 中心子数组的数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-centered-subarrays/description/)

题目给出一个整数数组nums，其长度不超过500。

若一个子数组的元素之和恰好等于该子数组中的某个元素，则称该子数组为中心子数组。

要求返回nums中中心子数组的数量。

由于题目的数据规模不大，因此可以直接暴力枚举所有的子数组，使用集合记录子数组中出现了哪些元素，同时计算子数组之和，然后判断子数组之和是否在集合中出现过，就可以确定当前子数组是否为中心子数组了。

在具体实现上，枚举起点和终点，然后一趟遍历计算的时间复杂度为O(n^3)，更常见的处理方式是枚举起点left，然后在此基础上枚举终点right，那么对于以right结尾的子数组，其对应的集合以及子数组之和，都可以在终点为right - 1的子数组的基础上添加nums[right]得到，从而将时间复杂度降低到O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def centeredSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        res = 0
        for left in range(n):
            nums_set = set()
            s = 0
            for right in range(left, n):
                nums_set.add(nums[right])
                s += nums[right]
                if s in nums_set:
                    res += 1
        
        return res
```
