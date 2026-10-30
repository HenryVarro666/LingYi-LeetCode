---
title: "3353. 最小总操作数"
aliases: ["yiduobo的每日leetcode 3353.最小总操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26656713192"
zhihu_id: "26656713192"
zhihu_title: "yiduobo的每日leetcode 3353.最小总操作数"
question_id: "3353"
question: "最小总操作数"
problem_url: "https://leetcode.cn/problems/minimum-total-operations/"
created: "2025-02-27T00:18:11+08:00"
updated: "2025-02-27T00:18:11+08:00"
upvotes: 0
comments: 0
---

# 3353. 最小总操作数

> **[yiduobo的每日leetcode 3353.最小总操作数](https://zhuanlan.zhihu.com/p/26656713192) · 知乎 · 2025-02-27 · 赞同 0**
> 力扣：[3353. 最小总操作数](https://leetcode.cn/problems/minimum-total-operations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3353.最小总操作数

[3353. 最小总操作数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-total-operations/description/)

给出一个整数数组nums，可以在这个数组上进行任意次操作，每次操作中，都可以选择数组中的一个前缀，将前缀中的所有元素加上k，k可以为负。问最少需要执行多少次操作，才能使得数组中每个元素相等。

首先可以明确的是，对于同一个前缀最多只能执行一次操作，因为如果对同一个前缀执行多次操作，那么完全可以将所有操作对应的k加起来变为一次操作。另一方面，对于nums中的某个元素nums[index]，若其与nums[index - 1]不同，那么无论怎么修改，都至少需要对前缀nums[0]到nums[index - 1]执行一次操作，因为只有修改这个前缀才能仅修改到nums[index - 1]且没有修改到nums[index]。

根据以上两点，就可以得到一种贪心算法。从下标1开始遍历nums中的元素，对于当前遍历到的nums[index]，若其与nums[index - 1]不同，那么就通过依次操作将nums[0]到nums[index - 1]都修改成nums[index]，同时更新答案。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for index in range(1, len(nums)):
            if nums[index] != nums[index - 1]:
                res += 1
        return res
```
