---
title: "883. 三维形体投影面积"
aliases: ["yiduobo的每日leetcode 883.三维形体投影面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351338708"
zhihu_id: "351338708"
zhihu_title: "yiduobo的每日leetcode 883.三维形体投影面积"
question_id: "883"
question: "三维形体投影面积"
problem_url: "https://leetcode.cn/problems/projection-area-of-3d-shapes/"
created: "2021-02-19T00:12:51+08:00"
updated: "2021-02-19T00:12:51+08:00"
upvotes: 0
comments: 0
---

# 883. 三维形体投影面积

> **[yiduobo的每日leetcode 883.三维形体投影面积](https://zhuanlan.zhihu.com/p/351338708) · 知乎 · 2021-02-19 · 赞同 0**
> 力扣：[883. 三维形体投影面积](https://leetcode.cn/problems/projection-area-of-3d-shapes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

883.三维形体投影面积

[力扣](https://leetcode-cn.com/problems/projection-area-of-3d-shapes/)

分别考察从上面、前后、左右这几个方向看这个三维形体是什么样的：

1、从上面来看，所有高度非0的格子都会形成投影，因此对于grid中所有非0值，都应该将答案加上1

2、从左侧和右侧来看，每一行的投影面积是当前行高度最高的立方体形成的投影，因此只需要计算每一行的最大值，然后将这些最大值加到答案中

3、从前方和后方来看，每一列的投影面积是当前列高度最高的立方体形成的投影，因此只需要计算每一列的最大值，然后将这些最大值加到答案中

最后附上python代码：

```python
class Solution(object):
    def projectionArea(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        max_row = [0] * m
        max_col = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    res += 1
                    max_row[i] = max(max_row[i], grid[i][j])
                    max_col[j] = max(max_col[j], grid[i][j])
        
        return res + sum(max_col) + sum(max_row)
```
