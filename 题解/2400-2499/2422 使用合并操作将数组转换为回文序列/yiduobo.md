---
title: "2422. 使用合并操作将数组转换为回文序列"
aliases: ["yiduobo的每日leetcode 2422.使用合并操作将数组转换为回文序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631414962"
zhihu_id: "631414962"
zhihu_title: "yiduobo的每日leetcode 2422.使用合并操作将数组转换为回文序列"
question_id: "2422"
question: "使用合并操作将数组转换为回文序列"
problem_url: "https://leetcode.cn/problems/merge-operations-to-turn-array-into-a-palindrome/"
created: "2023-05-23T02:46:25+08:00"
updated: "2023-05-23T02:46:25+08:00"
upvotes: 0
comments: 0
---

# 2422. 使用合并操作将数组转换为回文序列

> **[yiduobo的每日leetcode 2422.使用合并操作将数组转换为回文序列](https://zhuanlan.zhihu.com/p/631414962) · 知乎 · 2023-05-23 · 赞同 0**
> 力扣：[2422. 使用合并操作将数组转换为回文序列](https://leetcode.cn/problems/merge-operations-to-turn-array-into-a-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2422.使用合并操作将数组转换为回文序列

[力扣](https://leetcode.cn/problems/merge-operations-to-turn-array-into-a-palindrome/)

由于数组中的数都为正数，那么合并操作只能让数组中的数变得更大。基于这一点，不妨从两侧开始向中间考虑。

对于当前剩余数组的最左侧nums[left]以及nums[right]，若二者相等，那么就将left和right都向中间移动一位；若二者不相等，那么较小的那一侧必须要进行一次合并，也就是当nums[left] \< nums[right]时，需要将nums[left]与nums[left + 1]合并，反之则需要将nums[right]与nums[right - 1]合并。

重复上面的过程直到left与right相遇为止。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        left = 0
        right = len(nums) - 1
        while left < right:
            while nums[left] != nums[right]:
                res += 1
                if nums[left] < nums[right]:
                    left += 1
                    nums[left] += nums[left - 1]
                else:
                    right -= 1
                    nums[right] += nums[right + 1]
                
            left += 1
            right -= 1
        
        return res
```
