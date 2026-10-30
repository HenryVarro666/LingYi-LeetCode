---
title: "3423. 循环数组中相邻元素的最大差值"
aliases: ["yiduobo的每日leetcode 3423.循环数组中相邻元素的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1888704147999683290"
zhihu_id: "1888704147999683290"
zhihu_title: "yiduobo的每日leetcode 3423.循环数组中相邻元素的最大差值"
question_id: "3423"
question: "循环数组中相邻元素的最大差值"
problem_url: "https://leetcode.cn/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/"
difficulty: "Easy"
created: "2025-03-27T21:49:13+08:00"
updated: "2025-03-27T21:49:13+08:00"
upvotes: 0
comments: 0
---

# 3423. 循环数组中相邻元素的最大差值

> **[yiduobo的每日leetcode 3423.循环数组中相邻元素的最大差值](https://zhuanlan.zhihu.com/p/1888704147999683290) · 知乎 · 2025-03-27 · 赞同 0**
> 力扣：[3423. 循环数组中相邻元素的最大差值](https://leetcode.cn/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3423.循环数组中相邻元素的最大差值

[3423. 循环数组中相邻元素的最大差值 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/description/)

题目给出一个循环数组nums，要求找出相邻元素间的最大绝对差值。注意循环数组中的第一个元素与最后一个元素是相邻的。

对于下标在index的元素，其下一个元素的下标为(index + 1) % len(nums)，那么只需遍历数组，对于当前遍历到的元素nums[index]，计算其与nums[(index + 1) % len(nums)]的差的绝对值并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxAdjacentDistance(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for index in range(len(nums)):
            res = max(res, abs(nums[index] - nums[(index + 1) % len(nums)]))
            
        return res
```
