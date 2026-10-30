---
title: "4084. 有向网格中的最后访问单元格"
aliases: ["yiduobo的每日leetcode 4084.有向网格中的最后访问单元格"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2095187580685907619"
zhihu_id: "2095187580685907619"
zhihu_title: "yiduobo的每日leetcode 4084.有向网格中的最后访问单元格"
question_id: "4084"
question: "有向网格中的最后访问单元格"
problem_url: "https://leetcode.cn/problems/last-visited-cell-in-a-directional-grid/"
created: "2026-10-18T16:25:19+08:00"
updated: "2026-10-18T16:25:19+08:00"
upvotes: 2
comments: 0
---

# 4084. 有向网格中的最后访问单元格

> **[yiduobo的每日leetcode 4084.有向网格中的最后访问单元格](https://zhuanlan.zhihu.com/p/2095187580685907619) · 知乎 · 2026-10-18 · 赞同 2**
> 力扣：[4084. 有向网格中的最后访问单元格](https://leetcode.cn/problems/last-visited-cell-in-a-directional-grid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4084.有向网格中的最后访问单元格

<https://leetcode.cn/problems/last-visited-cell-in-a-directional-grid/description/>

题目给出一个m \* n的矩阵grid，其中每个单元格包含以下字符之一：

- 'L'：向左移动一格
- 'R'：向右移动一格
- 'U'：向上移动一格
- 'D'：向下移动一格

现在要求从单元格(0, 0)出发，并视为已经访问过(0, 0)，接下来每一步都按照当前单元格中的字符指示，移动到对应的单元格。

若下一次移动将离开网格，或者进入一个已经访问过的单元格，则移动过程结束，且这次移动不会被执行。

要求返回最后访问的单元格所在的行和列。

使用一个哈希表vis记录已经访问过的单元格，然后按照题意不断模拟移动即可。每次移动之前，先检测是否越界或者走到了访问过的单元格，若是，则停止移动，返回当前单元格的下标，否则就继续移动。

最后附上python代码：

```python
class Solution(object):
    def lastVisitedCell(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: List[int]
        """
        
        m = len(grid)
        n = len(grid[0])
        x, y = 0, 0
        
        dx = {'R': 0, 'L': 0, 'U': -1, 'D': 1}
        dy = {'R': 1, 'L': -1, 'U': 0, 'D': 0}
        vis = set([(0, 0)])
        while True:
            d = grid[x][y]
            nxt_x, nxt_y = x + dx[d], y + dy[d]
            if nxt_x < 0 or nxt_x >= m or nxt_y < 0 or nxt_y >= n or (nxt_x, nxt_y) in vis:
                break

            x, y = nxt_x, nxt_y
            vis.add((x, y))
        
        return x, y
```
