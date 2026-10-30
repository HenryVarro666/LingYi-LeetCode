---
title: "2441. 与对应负数同时存在的最大正整数"
aliases: ["yiduobo的每日leetcode 2441.与对应负数同时存在的最大正整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584119682"
zhihu_id: "584119682"
zhihu_title: "yiduobo的每日leetcode 2441.与对应负数同时存在的最大正整数"
question_id: "2441"
question: "与对应负数同时存在的最大正整数"
problem_url: "https://leetcode.cn/problems/largest-positive-integer-that-exists-with-its-negative/"
difficulty: "Easy"
rating: 1168
created: "2022-11-17T00:14:11+08:00"
updated: "2022-11-17T00:14:11+08:00"
upvotes: 0
comments: 0
---

# 2441. 与对应负数同时存在的最大正整数

> **[yiduobo的每日leetcode 2441.与对应负数同时存在的最大正整数](https://zhuanlan.zhihu.com/p/584119682) · 知乎 · 2022-11-17 · 赞同 0**
> 力扣：[2441. 与对应负数同时存在的最大正整数](https://leetcode.cn/problems/largest-positive-integer-that-exists-with-its-negative/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2441.与对应负数同时存在的最大正整数

[力扣](https://leetcode.cn/problems/largest-positive-integer-that-exists-with-its-negative/)

比较基础的题目，做法也是多种多样。我在这里采用的是先一趟遍历，使用哈希表记录所有出现的负数，然后再一趟遍历，若当前遍历到的数num，且相反数-num出现在了哈希表中，那么就用num来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxK(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        neg_set = set()
        for num in nums:
            if num < 0:
                neg_set.add(num)
        
        res = -1
        for num in nums:
            if -num in neg_set:
                res = max(res, num)
        
        return res
```
