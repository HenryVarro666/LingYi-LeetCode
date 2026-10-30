---
title: "289. 生命游戏"
aliases: ["yiduobo的每日leetcode 289.生命游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/156066905"
zhihu_id: "156066905"
zhihu_title: "yiduobo的每日leetcode 289.生命游戏"
question_id: "289"
question: "生命游戏"
problem_url: "https://leetcode.cn/problems/game-of-life/"
created: "2020-07-04T19:24:02+08:00"
updated: "2020-07-04T19:24:02+08:00"
upvotes: 1
comments: 0
---

# 289. 生命游戏

> **[yiduobo的每日leetcode 289.生命游戏](https://zhuanlan.zhihu.com/p/156066905) · 知乎 · 2020-07-04 · 赞同 1**
> 力扣：[289. 生命游戏](https://leetcode.cn/problems/game-of-life/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

289.生命游戏<https://leetcode-cn.com/problems/game-of-life/>

题目要求使用原地算法解决问题，那么就需要想办法处理一个问题，如果一个细胞，其周围的胞在之前的操作中变换过了状态应该怎么办。

注意到这里的状态只有0和1两种，于是一个自然的想法就是使用额外的状态标记来表示细胞在这一次操作中死去或者在这一次操作中复活。

我在这里使用的是2表示细胞在这一次操作中死去，3表示细胞在这一次操作中复活。之后一趟扫描，根据周围细胞的状态处理当前细胞的状态即可。最后对于所有状态值大于等于2的细胞，将其状态值减去2即可。

最后附上python代码：

```python
class Solution(object):
    def gameOfLife(self, board):
        """
        :type board: List[List[int]]
        :rtype: None Do not return anything, modify board in-place instead.
        """

        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        for i in range(len(board)):
            for j in range(len(board[0])):
                death = live = 0
                for index in range(8):
                    x = i + dx[index]
                    y = j + dy[index]
                    if x < 0 or x == len(board) or y < 0 or y == len(board[0]):
                        continue

                    if board[x][y] == 0 or board[x][y] == 3:
                        death += 1
                    else:
                        live += 1

                if board[i][j] == 0:
                    if live == 3:
                        board[i][j] = 3
                else:
                    if live < 2 or live > 3:
                        board[i][j] = 2

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] >= 2:
                    board[i][j] -= 2
```
