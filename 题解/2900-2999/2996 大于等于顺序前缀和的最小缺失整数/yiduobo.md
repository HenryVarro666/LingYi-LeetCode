---
title: "2996. 大于等于顺序前缀和的最小缺失整数"
aliases: ["yiduobo的每日leetcode 2996.大于等于顺序前缀和的最小缺失整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692678158"
zhihu_id: "692678158"
zhihu_title: "yiduobo的每日leetcode 2996.大于等于顺序前缀和的最小缺失整数"
question_id: "2996"
question: "大于等于顺序前缀和的最小缺失整数"
problem_url: "https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/"
difficulty: "Easy"
created: "2024-04-16T00:51:59+08:00"
updated: "2024-04-16T00:51:59+08:00"
upvotes: 1
comments: 0
---

# 2996. 大于等于顺序前缀和的最小缺失整数

> **[yiduobo的每日leetcode 2996.大于等于顺序前缀和的最小缺失整数](https://zhuanlan.zhihu.com/p/692678158) · 知乎 · 2024-04-16 · 赞同 1**
> 力扣：[2996. 大于等于顺序前缀和的最小缺失整数](https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2996.大于等于顺序前缀和的最小缺失整数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/description/)

题目的数据规模很小，只需从头开始向后一趟遍历，找出最长的顺序前缀，同时计算前缀之和s，然后再从s开始向上遍历，直到当前遍历的值没有出现在数组中为止。

最后附上python代码：

```python
class Solution(object):
    def missingInteger(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = nums[0]
        for index in range(1, len(nums)):
            if nums[index] == nums[index - 1] + 1:
                s += nums[index]
            else:
                break
        
        num_set = set(nums)
        while s in num_set:
            s += 1
        
        return s
```
