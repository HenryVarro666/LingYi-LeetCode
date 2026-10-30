---
title: "3689. 最大子数组总值I"
aliases: ["yiduobo的每日leetcode 3689.最大子数组总值I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955348170805588333"
zhihu_id: "1955348170805588333"
zhihu_title: "yiduobo的每日leetcode 3689.最大子数组总值I"
question_id: "3689"
question: "最大子数组总值 I"
problem_url: "https://leetcode.cn/problems/maximum-total-subarray-value-i/"
difficulty: "Medium"
rating: 1371
created: "2025-09-28T21:34:46+08:00"
updated: "2025-09-28T21:34:48+08:00"
upvotes: 1
comments: 0
---

# 3689. 最大子数组总值I

> **[yiduobo的每日leetcode 3689.最大子数组总值I](https://zhuanlan.zhihu.com/p/1955348170805588333) · 知乎 · 2025-09-28 · 赞同 1**
> 力扣：[3689. 最大子数组总值 I](https://leetcode.cn/problems/maximum-total-subarray-value-i/) · Medium · 灵茶山艾府：[脑筋急转弯，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3689.最大子数组总值I

[3689. 最大子数组总值 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-subarray-value-i/description/)

题目给出一个长度为n的整数数组nums以及一个整数k。现在要求从nums中选出恰好k个非空子数组，这些子数组可以重叠，同一个子数组可以被选择多次。

对于一个子数组，其值被定义为子数组中最大值与最小值之差。

问选出的k个子数组的值之和最大可能是多少。

为了使得这些子数组的值之和最大，就应该让每个子数组的值都尽可能的大，也就是说应该让子数组中的最大值尽可能大，最小值尽可能小，那么一个简单的思路就是直接取原数组，此时的最大值就是原数组的最大值，也就是所有子数组可能取到的最大值的上限，而最小值就是原数组的最小值，也就是所有子数组可能取到的最小值的下限。

另一方面，由于题目可以重复取同一个子数组，因此在这里直接取k次原数组就行，最终的答案就是原数组中最大值与最小值之差，再乘以k。

最后附上python代码：

```python
class Solution(object):
    def maxTotalValue(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        return (max(nums) - min(nums)) * k
```
