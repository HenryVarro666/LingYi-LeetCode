---
title: "3550. 数位和等于下标的最小下标"
aliases: ["yiduobo的每日leetcode 3550.数位和等于下标的最小下标"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909440628728763380"
zhihu_id: "1909440628728763380"
zhihu_title: "yiduobo的每日leetcode 3550.数位和等于下标的最小下标"
question_id: "3550"
question: "数位和等于下标的最小下标"
problem_url: "https://leetcode.cn/problems/smallest-index-with-digit-sum-equal-to-index/"
difficulty: "Easy"
created: "2025-05-24T02:51:15+08:00"
updated: "2025-05-24T02:51:15+08:00"
upvotes: 1
comments: 0
---

# 3550. 数位和等于下标的最小下标

> **[yiduobo的每日leetcode 3550.数位和等于下标的最小下标](https://zhuanlan.zhihu.com/p/1909440628728763380) · 知乎 · 2025-05-24 · 赞同 1**
> 力扣：[3550. 数位和等于下标的最小下标](https://leetcode.cn/problems/smallest-index-with-digit-sum-equal-to-index/) · Easy · 灵茶山艾府：[优化：只需枚举到 i=27（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3550.数位和等于下标的最小下标

[3550. 数位和等于下标的最小下标 - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-index-with-digit-sum-equal-to-index/description/)

题目给出一个整数数组nums，要求返回满足nums[index]的数位和恰好等于index的最小下标index。若不存在，则返回-1。

直接一趟遍历，对于当前遍历到的元素nums[index]，通过模10除10的方法计算其数位和s。若s与index相等，则直接返回index。若遍历完整个数组都找不到合法的index，则返回-1。

最后附上python代码：

```python
class Solution(object):
    def smallestIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        for index, v in enumerate(nums):
            s = 0
            while v:
                s += v % 10
                v //= 10
            
            if s == index:
                return index
        
        return -1
```
