---
title: "200. 岛屿数量"
aliases: ["yiduobo的每日leetcode 200.岛屿数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/网格图/一-网格图-DFS", "题单/LeetCode-热题-100/图论", "题单/面试经典-150-题/图"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146198826"
zhihu_id: "146198826"
zhihu_title: "yiduobo的每日leetcode 200.岛屿数量"
question_id: "200"
question: "岛屿数量"
problem_url: "https://leetcode.cn/problems/number-of-islands/"
difficulty: "Medium"
created: "2020-06-05T22:57:01+08:00"
updated: "2020-06-05T22:57:01+08:00"
upvotes: 1
comments: 0
---

# 200. 岛屿数量

> **[yiduobo的每日leetcode 200.岛屿数量](https://zhuanlan.zhihu.com/p/146198826) · 知乎 · 2020-06-05 · 赞同 1**
> 力扣：[200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/) · Medium · 灵茶山艾府：[把访问过的格子插上旗子🚩（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

200.岛屿数量<https://leetcode-cn.com/problems/number-of-islands/>

又是经典的种子染色法。具体做法为扫描整个地图，若当前单元格颜色为初始颜色1，那么从当前单元格开始做bfs，并将bfs遍历到的所有单元格染上新的颜色。染色完毕后更换新的颜色，然后继续遍历其他的单元格。

我在这里的处理方法是第一次bfs先将遍历到的1染色成2，然后后续每次bfs一次染上3、4、5等等，于是最后的答案就是下一次准备染的颜色减2。

最后附上python代码：

```python
class Solution(object):
    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """

        if not grid:
            return 0

        m = len(grid)
        n = len(grid[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        now = 2
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    grid[i][j] = str(now)
                    q = [[i, j]]
                    l = 0
                    r = 1
                    while l < r:
                        x, y = q[l]
                        l += 1
                        for index in range(4):
                            new_x = x + dx[index]
                            new_y = y + dy[index]
                            if new_x >= 0 and new_x < m and new_y >= 0 and new_y < n and grid[new_x][new_y] == '1':
                                grid[new_x][new_y] = str(now)
                                q.append([new_x, new_y])
                                r += 1
                    now += 1

        return now - 2
```
