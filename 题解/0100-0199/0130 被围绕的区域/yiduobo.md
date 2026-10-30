---
title: "130. 被围绕的区域"
aliases: ["yiduobo的每日leetcode 130.被围绕的区域"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140952199"
zhihu_id: "140952199"
zhihu_title: "yiduobo的每日leetcode 130.被围绕的区域"
question_id: "130"
question: "被围绕的区域"
problem_url: "https://leetcode.cn/problems/surrounded-regions/"
created: "2020-05-14T23:04:41+08:00"
updated: "2020-05-14T23:04:41+08:00"
upvotes: 1
comments: 0
---

# 130. 被围绕的区域

> **[yiduobo的每日leetcode 130.被围绕的区域](https://zhuanlan.zhihu.com/p/140952199) · 知乎 · 2020-05-14 · 赞同 1**
> 力扣：[130. 被围绕的区域](https://leetcode.cn/problems/surrounded-regions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

130.被围绕的区域<https://leetcode-cn.com/problems/surrounded-regions/>

种子染色法(floodfill)的某种变形。我们只需要从边界上的O开始做BFS或者DFS，找出所有未被标记过的相连的O，将其做好标记。最后扫描这个矩阵的所有字符，未标记的置为X，否则置为O即可。

我在这里用的是BFS，然后每次遇到边界上或者与边界相连的O，我都先将其置为P，然后在最后的扫描中再判断是否为P来决定这里应该是O还是X。

另外，python是有先进先出队列、双向队列以及优先队列这些东西的，不过我在这里还是用list来做的朴素实现，性能可能会稍差一些。

最后附上python代码：

```python
class Solution(object):
    def solve(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """

        if not board:
            return 

        m = len(board)
        n = len(board[0])

        q = []
        for index in range(m):
            if board[index][0] == 'O':
                q.append((index, 0))
                board[index][0] = 'P'
            if board[index][n - 1] == 'O':
                q.append((index, n - 1))
                board[index][n - 1] = 'P'

        for index in range(n):
            if board[0][index] == 'O':
                q.append((0, index))
                board[0][index] = 'P'
            if board[m - 1][index] == 'O':
                q.append((m - 1, index))
                board[m - 1][index] = 'P'

        left = 0
        right = len(q)
        dx = [0, -1, 0, 1]
        dy = [1, 0, -1, 0]
        while left < right:
            x, y = q[left]
            left += 1

            for index in range(4):
                new_x = x + dx[index]
                new_y = y + dy[index]
                if new_x >= 0 and new_x < m and new_y >= 0 and new_y < n and board[new_x][new_y] == 'O':
                    q.append((new_x, new_y))
                    board[new_x][new_y] = 'P'
                    right += 1

        for i in range(m):
            for j in range(n):
                if board[i][j] != 'P':
                    board[i][j] = 'X'
                else:
                    board[i][j] = 'O'
```
