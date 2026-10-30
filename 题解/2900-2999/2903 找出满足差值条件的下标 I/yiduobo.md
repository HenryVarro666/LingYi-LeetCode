---
title: "2903. 找出满足差值条件的下标I"
aliases: ["yiduobo的每日leetcode 2903.找出满足差值条件的下标I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/two-pointers"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663784725"
zhihu_id: "663784725"
zhihu_title: "yiduobo的每日leetcode 2903.找出满足差值条件的下标I"
question_id: "2903"
question: "找出满足差值条件的下标 I"
problem_url: "https://leetcode.cn/problems/find-indices-with-index-and-value-difference-i/"
difficulty: "Easy"
created: "2023-10-28T02:58:21+08:00"
updated: "2023-10-28T02:58:21+08:00"
upvotes: 0
comments: 0
---

# 2903. 找出满足差值条件的下标I

> **[yiduobo的每日leetcode 2903.找出满足差值条件的下标I](https://zhuanlan.zhihu.com/p/663784725) · 知乎 · 2023-10-28 · 赞同 0**
> 力扣：[2903. 找出满足差值条件的下标 I](https://leetcode.cn/problems/find-indices-with-index-and-value-difference-i/) · Easy · 灵茶山艾府：[O(n) 做法：双指针+维护最大最小（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2903.找出满足差值条件的下标I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-indices-with-index-and-value-difference-i/)

题目的数据规模很小，因此可以直接枚举下标i和j，然后检测下标差和数值差是否符合条件即可。

最后附上python代码：

```python
class Solution(object):
    def findIndices(self, nums, indexDifference, valueDifference):
        """
        :type nums: List[int]
        :type indexDifference: int
        :type valueDifference: int
        :rtype: List[int]
        """

        for i in range(len(nums)):
            for j in range(i, len(nums)):
                if abs(i - j) >= indexDifference and abs(nums[i] - nums[j]) >= valueDifference:
                    return [i, j]
        
        return [-1, -1]
```
