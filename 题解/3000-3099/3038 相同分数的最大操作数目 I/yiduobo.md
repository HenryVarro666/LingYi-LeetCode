---
title: "3038. 相同分数的最大操作数目I"
aliases: ["yiduobo的每日leetcode 3038.相同分数的最大操作数目I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695747635"
zhihu_id: "695747635"
zhihu_title: "yiduobo的每日leetcode 3038.相同分数的最大操作数目I"
question_id: "3038"
question: "相同分数的最大操作数目 I"
problem_url: "https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-i/"
difficulty: "Easy"
created: "2024-05-03T02:35:56+08:00"
updated: "2024-05-03T02:35:56+08:00"
upvotes: 1
comments: 0
---

# 3038. 相同分数的最大操作数目I

> **[yiduobo的每日leetcode 3038.相同分数的最大操作数目I](https://zhuanlan.zhihu.com/p/695747635) · 知乎 · 2024-05-03 · 赞同 1**
> 力扣：[3038. 相同分数的最大操作数目 I](https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-i/) · Easy · 灵茶山艾府：[简单模拟（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3038.相同分数的最大操作数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-i/description/)

由于题目中的操作只能针对剩余数组的前两个元素进行，因此在这里只需先计算出数组中前两个元素之和v，然后从下标2开始以步长2向后遍历，每次检测当前元素与下一个元素之和是否等于v即可。

最后附上python代码：

```python
class Solution(object):
    def maxOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        v = nums[0] + nums[1]
        res = 1
        for index in range(2, len(nums), 2):
            if index + 1 == len(nums) or nums[index] + nums[index + 1] != v:
                break
            res += 1
        
        return res
```
