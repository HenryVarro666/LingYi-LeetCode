---
title: "2482. 行和列中一和零的差值"
aliases: ["yiduobo的每日leetcode 2482.行和列中一和零的差值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589190087"
zhihu_id: "589190087"
zhihu_title: "yiduobo的每日leetcode 2482.行和列中一和零的差值"
question_id: "2482"
question: "行和列中一和零的差值"
problem_url: "https://leetcode.cn/problems/difference-between-ones-and-zeros-in-row-and-column/"
difficulty: "Medium"
created: "2022-12-04T23:59:39+08:00"
updated: "2022-12-04T23:59:39+08:00"
upvotes: 0
comments: 0
---

# 2482. 行和列中一和零的差值

> **[yiduobo的每日leetcode 2482.行和列中一和零的差值](https://zhuanlan.zhihu.com/p/589190087) · 知乎 · 2022-12-04 · 赞同 0**
> 力扣：[2482. 行和列中一和零的差值](https://leetcode.cn/problems/difference-between-ones-and-zeros-in-row-and-column/) · Medium · 灵茶山艾府：[模拟 + 两个优化](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2482.行和列中一和零的差值

[力扣](https://leetcode.cn/problems/difference-between-ones-and-zeros-in-row-and-column/description/)

由于题目并没有对额外空间使用的要求，那么可以按照题目描述构造四个数组ones_row、ones_col、zeros_row以及zeros_col，接下来遍历grid来更新这四个数组，最后再构造一个大小与grid相同的答案数组res，然后遍历res并使用题目给出的计算方式计算res中每个位置的值。

最后附上python代码：

```python
class Solution(object):
    def onesMinusZeros(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])

        ones_row = [0] * m
        ones_col = [0] * n
        zeros_row = [0] * m
        zeros_col = [0] * n
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    zeros_row[i] += 1
                    zeros_col[j] += 1
                else:
                    ones_row[i] += 1
                    ones_col[j] += 1
        
        res = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = ones_row[i] + ones_col[j] - zeros_row[i] - zeros_col[j]
        
        return res
```
