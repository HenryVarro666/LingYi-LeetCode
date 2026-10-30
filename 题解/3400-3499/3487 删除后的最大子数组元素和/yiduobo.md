---
title: "3487. 删除后的最大子数组元素和"
aliases: ["yiduobo的每日leetcode 3487.删除后的最大子数组元素和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897434748688765605"
zhihu_id: "1897434748688765605"
zhihu_title: "yiduobo的每日leetcode 3487.删除后的最大子数组元素和"
question_id: "3487"
question: "删除后的最大子数组元素和"
problem_url: "https://leetcode.cn/problems/maximum-unique-subarray-sum-after-deletion/"
difficulty: "Easy"
created: "2025-04-24T22:51:33+08:00"
updated: "2025-04-24T22:51:33+08:00"
upvotes: 1
comments: 0
---

# 3487. 删除后的最大子数组元素和

> **[yiduobo的每日leetcode 3487.删除后的最大子数组元素和](https://zhuanlan.zhihu.com/p/1897434748688765605) · 知乎 · 2025-04-24 · 赞同 1**
> 力扣：[3487. 删除后的最大子数组元素和](https://leetcode.cn/problems/maximum-unique-subarray-sum-after-deletion/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3487.删除后的最大子数组元素和

[3487. 删除后的最大子数组元素和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-unique-subarray-sum-after-deletion/description/)

题目给出一个整数数组nums，现在要求从中删除任意数量的元素，但不能将其变为空数组。执行删除操作后，需要从中选出一个包含元素互不相同的子数组，使得这个子数组元素之和最大。

若nums中没有正数，就应该将nums删得只剩下唯一一个最大的元素，反之则应该将nums中所有的非正数以及重复元素都删除。于是可以一趟遍历，使用一个集合vis记录出现过的元素，同时使用一个变量ma记录nums中最大的元素值。对于对于当前遍历到的v，先使用v来更新ma，接下来若v之前没有出现过且v大于0，那么就将其累加到答案s中，并将v加入到vis中。遍历完成后，若ma非正数，则返回ma，否则返回s。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        vis = set()
        s = 0
        ma = None
        for v in nums:
            if ma is None or ma < v:
                ma = v
            if v > 0 and v not in vis:
                vis.add(v)
                s += v
        
        if ma <= 0:
            return ma
        return s
```
