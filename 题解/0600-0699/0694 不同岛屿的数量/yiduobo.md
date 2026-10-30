---
title: "694. 不同岛屿的数量"
aliases: ["yiduobo的每日leetcode 694.不同岛屿的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604071207"
zhihu_id: "604071207"
zhihu_title: "yiduobo的每日leetcode 694.不同岛屿的数量"
question_id: "694"
question: "不同岛屿的数量"
problem_url: "https://leetcode.cn/problems/number-of-distinct-islands/"
created: "2023-02-07T02:20:21+08:00"
updated: "2023-02-07T02:20:21+08:00"
upvotes: 0
comments: 0
---

# 694. 不同岛屿的数量

> **[yiduobo的每日leetcode 694.不同岛屿的数量](https://zhuanlan.zhihu.com/p/604071207) · 知乎 · 2023-02-07 · 赞同 0**
> 力扣：[694. 不同岛屿的数量](https://leetcode.cn/problems/number-of-distinct-islands/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

694.不同岛屿的数量

[力扣](https://leetcode.cn/problems/number-of-distinct-islands/)

题目要求找出不同岛屿的数量，这里的不同指的是两个岛屿无法通过平移重叠到一起，也就是岛屿间各个格子的相对空间位置要完全相同。

一个自然的想法是选择一个基准单元格，计算其他单元格到这个格子的横纵坐标距离，并将这些距离编码作为哈希表的key来进行去重。这里有一个不太优美的地方是由于地图有一定规模，因此坐标间的距离可能是两位数，为编码带来了一定的困扰。

另一个想法则是同样选择一个基准单元格，模拟从这个单元格开始遍历得到整个岛屿的行走过程。在这里如果按照先行后列的顺序遍历没有走到过的单元格，那么行走过程相同也就意味着生成的到岛屿也必然相同。需要注意的是，在这里如果选择使用bfs，那么就需要对每个单元格生成的行走操作做一个划分，否则可能混淆；相对的，如果使用dfs，则可以通过dfs序的方式得到唯一的生成序列，是更符合题目需求的。这里的dfs指的是从当前格子向哪个方向进行了移动。

具体实现上，我采用的是0到3作为基准的前进方向，而4到7则作为回溯后的dfs序闭合标记。

最后附上python代码：

```python
class Solution(object):
    def numDistinctIslands(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        vis = set()
        path_set = set()

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def dfs(nowx, nowy):
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                    grid[x][y] = 0
                    path.append(index)
                    dfs(x, y)
                    path.append(index + 4)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    path = []
                    dfs(i, j)
                    path_set.add(''.join([str(x) for x in path]))

        return len(path_set)
```
