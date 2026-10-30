---
title: "3678. 大于平均值的最小未出现正整数"
aliases: ["yiduobo的每日leetcode 3678.大于平均值的最小未出现正整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952901652349691545"
zhihu_id: "1952901652349691545"
zhihu_title: "yiduobo的每日leetcode 3678.大于平均值的最小未出现正整数"
question_id: "3678"
question: "大于平均值的最小未出现正整数"
problem_url: "https://leetcode.cn/problems/smallest-absent-positive-greater-than-average/"
difficulty: "Easy"
created: "2025-09-23T23:37:38+08:00"
updated: "2025-09-23T23:37:39+08:00"
upvotes: 0
comments: 0
---

# 3678. 大于平均值的最小未出现正整数

> **[yiduobo的每日leetcode 3678.大于平均值的最小未出现正整数](https://zhuanlan.zhihu.com/p/1952901652349691545) · 知乎 · 2025-09-23 · 赞同 0**
> 力扣：[3678. 大于平均值的最小未出现正整数](https://leetcode.cn/problems/smallest-absent-positive-greater-than-average/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3678.大于平均值的最小未出现正整数

[3678. 大于平均值的最小未出现正整数 - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-absent-positive-greater-than-average/description/)

题目给出一个整数数组nums，其中元素的取值范围在-100到100之间。要求找出其中严格大于nums中所有元素平均值的最小未出现正整数。

由于题目中存在负数，因此平均值可能小于1，此时答案的下界target就是1，反之target则应该取sum(nums) // len(nums) + 1，理由是若平均值刚好为整数，那么target就相当于平均值加上1，否则target就代表了平均值向上取整。

接下来，只需从target开始向上遍历，找出第一个没出现在nums中的正整数即可。

最后附上python代码：

```python
class Solution(object):
    def smallestAbsent(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = sum(nums)
        target = max(1, s // len(nums) + 1)
        
        nums_set = set(nums)
        while target in nums_set:
            target += 1
        return target
```
