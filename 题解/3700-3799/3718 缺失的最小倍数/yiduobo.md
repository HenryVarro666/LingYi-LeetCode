---
title: "3718. 损失的最小倍数"
aliases: ["yiduobo的每日leetcode 3718.损失的最小倍数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1963356685847491746"
zhihu_id: "1963356685847491746"
zhihu_title: "yiduobo的每日leetcode 3718.损失的最小倍数"
question_id: "3718"
question: "缺失的最小倍数"
problem_url: "https://leetcode.cn/problems/smallest-missing-multiple-of-k/"
difficulty: "Easy"
created: "2025-10-19T21:34:49+08:00"
updated: "2025-10-19T21:35:01+08:00"
upvotes: 2
comments: 0
---

# 3718. 损失的最小倍数

> **[yiduobo的每日leetcode 3718.损失的最小倍数](https://zhuanlan.zhihu.com/p/1963356685847491746) · 知乎 · 2025-10-19 · 赞同 2**
> 力扣：[3718. 缺失的最小倍数](https://leetcode.cn/problems/smallest-missing-multiple-of-k/) · Easy · 灵茶山艾府：[O(n) 哈希集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3718.损失的最小倍数

<https://leetcode.cn/problems/smallest-missing-multiple-of-k/description/>

题目给出一个整数数组nums以及一个整数k，要求找出不在nums中，且值为k的倍数的最小值。

先将nums转化为集合，然后从k开始，以步长k向上迭代，迭代过程中首个不在集合中的元素即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def missingMultiple(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        num_set = set(nums)
        res = k
        while res in num_set:
            res += k
        return res
```
