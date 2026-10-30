---
title: "2639. 查询网格图中每一列的宽度"
aliases: ["yiduobo的每日leetcode 2639.查询网格图中每一列的宽度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646402737"
zhihu_id: "646402737"
zhihu_title: "yiduobo的每日leetcode 2639.查询网格图中每一列的宽度"
question_id: "2639"
question: "查询网格图中每一列的宽度"
problem_url: "https://leetcode.cn/problems/find-the-width-of-columns-of-a-grid/"
difficulty: "Easy"
created: "2023-07-27T23:39:12+08:00"
updated: "2023-07-27T23:39:12+08:00"
upvotes: 0
comments: 0
---

# 2639. 查询网格图中每一列的宽度

> **[yiduobo的每日leetcode 2639.查询网格图中每一列的宽度](https://zhuanlan.zhihu.com/p/646402737) · 知乎 · 2023-07-27 · 赞同 0**
> 力扣：[2639. 查询网格图中每一列的宽度](https://leetcode.cn/problems/find-the-width-of-columns-of-a-grid/) · Easy · 灵茶山艾府：[多种方法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2639.查询网格图中每一列的宽度

[力扣](https://leetcode.cn/problems/find-the-width-of-columns-of-a-grid/)

直接遍历网格中的每个位置，对于grid[i][j]，若其为负数，则需要先将其变为正数，同时将其对应的长度加上1，也就是负号的长度。接下来通过不断除10的方法更新这个数的长度，然后用这个长度去更新答案数组中下标为j的答案即可。

最后附上python代码：

```python
class Solution(object):
    def findColumnWidth(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[int]
        """

        m = len(grid)
        n = len(grid[0])
        res = [0] * n
        for i in range(m):
            for j in range(n):
                v = grid[i][j]
                length = 0
                if v < 0:
                    length += 1
                    v = -v
                
                if v == 0:
                    length += 1
                else:
                    while v > 0:
                        length += 1
                        v //= 10
                
                res[j] = max(res[j], length)
        
        return res
```
