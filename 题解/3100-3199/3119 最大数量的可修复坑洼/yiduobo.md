---
title: "3119. 最大数量的可修复坑洼"
aliases: ["yiduobo的每日leetcode 3119.最大数量的可修复坑洼"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701438320"
zhihu_id: "701438320"
zhihu_title: "yiduobo的每日leetcode 3119.最大数量的可修复坑洼"
question_id: "3119"
question: "最大数量的可修复坑洼"
problem_url: "https://leetcode.cn/problems/maximum-number-of-potholes-that-can-be-fixed/"
created: "2024-06-03T20:34:20+08:00"
updated: "2024-06-03T20:34:20+08:00"
upvotes: 0
comments: 0
---

# 3119. 最大数量的可修复坑洼

> **[yiduobo的每日leetcode 3119.最大数量的可修复坑洼](https://zhuanlan.zhihu.com/p/701438320) · 知乎 · 2024-06-03 · 赞同 0**
> 力扣：[3119. 最大数量的可修复坑洼](https://leetcode.cn/problems/maximum-number-of-potholes-that-can-be-fixed/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3119.最大数量的可修复坑洼

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-potholes-that-can-be-fixed/description/)

题目给出一个由'x'和'.'组成的字符串，将连续出现的n的'x'变为'.'的代价为n + 1。现在给出总代价budget，问最多可以将多少个'x'变为'.'。

对于长度为n的'x'，修复单个'x'的评价代价为1 + 1 / n，换言之，n越大，评价的修改代价就越小，也就是说在这里应该先尽量修复较长的连续'x'。于是只需一趟遍历，先统计字符串中连续的'x'的长度，接下来将这些长度从大到小排序，然后一趟遍历，逐段修复直到budget为0或者全部修复完成为止。

最后附上python代码：

```python
class Solution(object):
    def maxPotholes(self, road, budget):
        """
        :type road: str
        :type budget: int
        :rtype: int
        """

        cnt = []
        p = 0
        while p < len(road):
            while p < len(road) and road[p] == '.':
                p += 1
            
            if p == len(road):
                break
            
            q = p
            while q < len(road) and road[q] == 'x':
                q += 1
            
            cnt.append(q - p)
            p = q
        
        cnt.sort(reverse=True)
        res = 0
        for v in cnt:
            if budget > v + 1:
                res += v
                budget -= v + 1
            else:
                res += budget - 1
                break
        
        return res
```
