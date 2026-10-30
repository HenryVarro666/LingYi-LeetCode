---
title: "3566. 等积子集的划分方案"
aliases: ["yiduobo的每日leetcode 3566.等积子集的划分方案"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/hash-table", "leetcode/math", "leetcode/backtracking", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1935829576346469605"
zhihu_id: "1935829576346469605"
zhihu_title: "yiduobo的每日leetcode 3566.等积子集的划分方案"
question_id: "3566"
question: "等积子集的划分方案"
problem_url: "https://leetcode.cn/problems/partition-array-into-two-equal-product-subsets/"
difficulty: "Medium"
rating: 1459
created: "2025-08-04T22:36:00+08:00"
updated: "2025-08-04T22:36:00+08:00"
upvotes: 0
comments: 0
---

# 3566. 等积子集的划分方案

> **[yiduobo的每日leetcode 3566.等积子集的划分方案](https://zhuanlan.zhihu.com/p/1935829576346469605) · 知乎 · 2025-08-04 · 赞同 0**
> 力扣：[3566. 等积子集的划分方案](https://leetcode.cn/problems/partition-array-into-two-equal-product-subsets/) · Medium · 灵茶山艾府：[三种方法：递归 / 二进制枚举 / 折半枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3566.等积子集的划分方案

[3566. 等积子集的划分方案 - 力扣（LeetCode）](https://leetcode.cn/problems/partition-array-into-two-equal-product-subsets/description/)

题目给出一个整数数组nums，其中元素互不相同，且个数不超过12个。另外给出一个整数target，问能否将这些数划分成两个非空的两部分，每部分的乘积都恰好为target。

由于nums中的元素个数较少，因此可以直接一趟dfs，找出所有的划分方案并判断是否合法即可。

在具体实现上，可以在每次划分完成时立马判断是否合法，若合法就可以直接返回了。

最后附上python代码：

```python
class Solution(object):
    def checkEqualPartitions(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: bool
        """

        def find(level, x, y):
            if level == len(nums):
                return x == target and y == target
            
            return find(level + 1, x * nums[level], y) or find(level + 1, x, y * nums[level])
        
        return find(0, 1, 1)
```
