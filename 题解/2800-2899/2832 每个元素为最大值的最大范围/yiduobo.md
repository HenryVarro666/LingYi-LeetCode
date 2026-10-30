---
title: "2832. 每个元素为最大值的最大范围"
aliases: ["yiduobo的每日leetcode 2832.每个元素为最大值的最大范围"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659360427"
zhihu_id: "659360427"
zhihu_title: "yiduobo的每日leetcode 2832.每个元素为最大值的最大范围"
question_id: "2832"
question: "每个元素为最大值的最大范围"
problem_url: "https://leetcode.cn/problems/maximal-range-that-each-element-is-maximum-in-it/"
created: "2023-10-02T23:26:52+08:00"
updated: "2023-10-02T23:26:52+08:00"
upvotes: 0
comments: 0
---

# 2832. 每个元素为最大值的最大范围

> **[yiduobo的每日leetcode 2832.每个元素为最大值的最大范围](https://zhuanlan.zhihu.com/p/659360427) · 知乎 · 2023-10-02 · 赞同 0**
> 力扣：[2832. 每个元素为最大值的最大范围](https://leetcode.cn/problems/maximal-range-that-each-element-is-maximum-in-it/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2832.每个元素为最大值的最大范围

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximal-range-that-each-element-is-maximum-in-it/)

题目实际上是要对于每个nums\[i\]，找出其左侧最大的满足nums\[left\[i\]\]大于nums\[i\]的下标left\[i\]，以及其右侧最小的满足nums\[right\[i\]\]大于nums\[i\]的下标right\[i\]，那么其对应的res\[i\]就是right\[i\] - left\[i\] - 1。

对于left和right的求解，则是经典的单调栈问题，具体可以参考之前的496题

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

最后附上python代码：

```python
class Solution(object):
    def maximumLengthOfRanges(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        left = [-1] * n
        right = [n] * n

        stack = []
        for index in range(n):
            while stack and nums[stack[-1]] < nums[index]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        stack = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[index]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        return [right[index] - left[index] - 1 for index in range(n)]
```
