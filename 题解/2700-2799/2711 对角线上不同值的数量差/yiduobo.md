---
title: "2711. 对角线上不同值的数量差"
aliases: ["yiduobo的每日leetcode 2711.对角线上不同值的数量差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/bao-li", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651240972"
zhihu_id: "651240972"
zhihu_title: "yiduobo的每日leetcode 2711.对角线上不同值的数量差"
question_id: "2711"
question: "对角线上不同值的数量差"
problem_url: "https://leetcode.cn/problems/difference-of-number-of-distinct-values-on-diagonals/"
difficulty: "Medium"
rating: 1429
created: "2023-08-21T02:29:07+08:00"
updated: "2023-08-21T02:29:07+08:00"
upvotes: 0
comments: 0
---

# 2711. 对角线上不同值的数量差

> **[yiduobo的每日leetcode 2711.对角线上不同值的数量差](https://zhuanlan.zhihu.com/p/651240972) · 知乎 · 2023-08-21 · 赞同 0**
> 力扣：[2711. 对角线上不同值的数量差](https://leetcode.cn/problems/difference-of-number-of-distinct-values-on-diagonals/) · Medium · 灵茶山艾府：[三种方法：暴力 / 前后缀分解 / 位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2711.对角线上不同值的数量差

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/difference-of-number-of-distinct-values-on-diagonals/)

题目的数据规模很小，因此可以直接枚举矩阵中的每个位置，然后从这个位置出发分别向左上和右下不断行走直到来到矩阵边界上。在行走过程中分别使用两个集合记录遇到的数，最后用这两个集合大小差的绝对值更新当前位置对应的答案就行了。

最后附上python代码：

```python
class Solution(object):
    def differenceOfDistinctValues(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])

        res = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                x, y = i - 1, j - 1
                up_set = set()
                while x >= 0 and y >= 0:
                    up_set.add(grid[x][y])
                    x -= 1
                    y -= 1
                
                x, y = i + 1, j + 1
                down_set = set()
                while x < m and y < n:
                    down_set.add(grid[x][y])
                    x += 1
                    y += 1
                
                res[i][j] = abs(len(up_set) - len(down_set))
        
        return res
```
