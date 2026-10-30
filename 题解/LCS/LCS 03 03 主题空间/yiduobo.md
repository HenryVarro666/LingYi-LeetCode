---
title: "LCS 03. 主题空间"
aliases: ["yiduobo的每日leetcode LCS03.主题空间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/581011208"
zhihu_id: "581011208"
zhihu_title: "yiduobo的每日leetcode LCS03.主题空间"
question_id: "LCS 03"
question: "主题空间"
created: "2022-11-07T01:13:03+08:00"
updated: "2022-11-07T01:13:03+08:00"
upvotes: 0
comments: 0
---

# LCS 03. 主题空间

> **[yiduobo的每日leetcode LCS03.主题空间](https://zhuanlan.zhihu.com/p/581011208) · 知乎 · 2022-11-07 · 赞同 0**
> 力扣：LCS 03. 主题空间

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

LCS03.主题空间

[力扣](https://leetcode.cn/problems/YesdPw/)

经典二维平面求连通块的问题，还是采用floodfill来处理。

遍历每个格子，若当前格子(x, y)没有被处理过，且对应值不是0，那么就从当前格子开始向四个方向进行bfs，遍历与(x, y)数值相同的格子。

若在遍历过程中来到了边界，或者与0相邻，那么说明当前的连通块与走廊相邻。bfs完成后，记录当前连通块的大小，以及其是否与走廊相邻，然后继续遍历其他格子。

全部遍历完成后，就得到了所有连通块的信息，从中找出最大且不与走廊相邻的连通块作为最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestArea(self, grid):
        """
        :type grid: List[str]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        belong = [[None] * n for _ in range(m)]
        part_cnt = 0
        part_len = []
        near_part = set()

        for i in range(m):
            for j in range(n):
                if grid[i][j] != '0' and belong[i][j] is None:
                    belong[i][j] = part_cnt
                    q = [[i, j]]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x < 0 or x == m or y < 0 or y == n or grid[x][y] == '0':
                                near_part.add(part_cnt)
                            elif grid[x][y] == grid[i][j] and belong[x][y] is None:
                                belong[x][y] = part_cnt
                                q.append([x, y])
                                tail += 1

                    part_cnt += 1
                    part_len.append(tail)

        res = 0
        for index, length in enumerate(part_len):
            if index not in near_part:
                res = max(res, length)

        return res
```
