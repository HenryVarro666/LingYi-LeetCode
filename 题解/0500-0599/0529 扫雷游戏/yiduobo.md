---
title: "529. 扫雷游戏"
aliases: ["yiduobo的每日leetcode 529.扫雷游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261167414"
zhihu_id: "261167414"
zhihu_title: "yiduobo的每日leetcode 529.扫雷游戏"
question_id: "529"
question: "扫雷游戏"
problem_url: "https://leetcode.cn/problems/minesweeper/"
created: "2020-10-03T20:29:53+08:00"
updated: "2020-10-03T20:29:53+08:00"
upvotes: 0
comments: 0
---

# 529. 扫雷游戏

> **[yiduobo的每日leetcode 529.扫雷游戏](https://zhuanlan.zhihu.com/p/261167414) · 知乎 · 2020-10-03 · 赞同 0**
> 力扣：[529. 扫雷游戏](https://leetcode.cn/problems/minesweeper/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

529.扫雷游戏<https://leetcode-cn.com/problems/minesweeper/>

如果点击的位置是地雷，那么直接炸了返回即可。

如果点击的位置不是地雷，那么就将其加入到队列中开始进行bfs。

对于bfs队列的头部，首先统计其周围八个格子中地雷的个数。若地雷数量大于0，那么将其标记为对应的数量，继续bfs。若地雷的数量等于0，那么将其标记为E，同时将周围八个格子中，没有被翻开且不在队列中的格子加入到队列尾部，继续bfs。

bfs完成后返回答案即可。

最后附上python代码，其中两个for循环分别是统计周围地雷的数量以及当地雷数量为0时将周围板子加入到队列：

```python
class Solution(object):
    def updateBoard(self, board, click):
        """
        :type board: List[List[str]]
        :type click: List[int]
        :rtype: List[List[str]]
        """

        x = click[0]
        y = click[1]
        if board[x][y] == 'M':
            board[x][y] = 'X'
        else:
            dx = [0, 1, 1, 1, 0, -1, -1, -1]
            dy = [1, 1, 0, -1, -1, -1, 0, 1]
            used = [[False] * len(board[0]) for _ in range(len(board))]
            q = [(x, y)]
            l = 0
            r = 1
            while l < r:
                x, y = q[l]
                l += 1
                cnt = 0
                for index in range(8):
                    near_x = x + dx[index]
                    near_y = y + dy[index]
                    if near_x >= 0 and near_x < len(board) and near_y >= 0 and near_y < len(board[0]) and board[near_x][near_y] == 'M':
                        cnt += 1

                if cnt > 0:
                    board[x][y] = str(cnt)
                else:
                    board[x][y] = 'B'
                    for index in range(8):
                        near_x = x + dx[index]
                        near_y = y + dy[index]
                        if near_x >= 0 and near_x < len(board) and near_y >= 0 and near_y < len(board[0]) and not used[near_x][near_y] and board[near_x][near_y] == 'E':
                            q.append((near_x, near_y))
                            used[near_x][near_y] = True
                            r += 1

        return board
```
