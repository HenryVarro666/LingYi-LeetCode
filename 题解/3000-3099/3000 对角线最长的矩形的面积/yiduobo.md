---
title: "3000. 对角线最长的矩形的面积"
aliases: ["yiduobo的每日leetcode 3000.对角线最长的矩形的面积"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693088630"
zhihu_id: "693088630"
zhihu_title: "yiduobo的每日leetcode 3000.对角线最长的矩形的面积"
question_id: "3000"
question: "对角线最长的矩形的面积"
problem_url: "https://leetcode.cn/problems/maximum-area-of-longest-diagonal-rectangle/"
difficulty: "Easy"
created: "2024-04-18T00:35:18+08:00"
updated: "2024-04-18T00:35:18+08:00"
upvotes: 1
comments: 0
---

# 3000. 对角线最长的矩形的面积

> **[yiduobo的每日leetcode 3000.对角线最长的矩形的面积](https://zhuanlan.zhihu.com/p/693088630) · 知乎 · 2024-04-18 · 赞同 1**
> 力扣：[3000. 对角线最长的矩形的面积](https://leetcode.cn/problems/maximum-area-of-longest-diagonal-rectangle/) · Easy · 灵茶山艾府：[简洁写法，O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3000.对角线最长的矩形的面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-area-of-longest-diagonal-rectangle/description/)

矩形对角线的长度可以通过边长以及勾股定理计算出来，那么就只需一趟遍历，在保证边长平方和最大的前提下，计算最大的矩形面积即可。

最后附上python代码：

```python
class Solution(object):
    def areaOfMaxDiagonal(self, dimensions):
        """
        :type dimensions: List[List[int]]
        :rtype: int
        """

        res = 0
        ma = 0
        for x, y in dimensions:
            t = x ** 2 + y ** 2
            if t > ma:
                ma = t
                res = x * y
            elif t == ma:
                res = max(res, x * y)
        
        return res
```
