---
title: "LCP 41. 黑白翻转棋"
aliases: ["yiduobo的每日leetcode LCP41.黑白翻转棋"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576073195"
zhihu_id: "576073195"
zhihu_title: "yiduobo的每日leetcode LCP41.黑白翻转棋"
question_id: "LCP 41"
question: "黑白翻转棋"
problem_url: "https://leetcode.cn/problems/fHi6rV/"
difficulty: "Medium"
created: "2022-10-22T02:52:47+08:00"
updated: "2022-10-22T02:52:47+08:00"
upvotes: 1
comments: 0
---

# LCP 41. 黑白翻转棋

> **[yiduobo的每日leetcode LCP41.黑白翻转棋](https://zhuanlan.zhihu.com/p/576073195) · 知乎 · 2022-10-22 · 赞同 1**
> 力扣：[LCP 41. 黑白翻转棋](https://leetcode.cn/problems/fHi6rV/) · Medium · 灵茶山艾府：[暴力枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP41.黑白翻转棋

[力扣](https://leetcode.cn/problems/fHi6rV/)

题目的数据规模很小，那么完全可以枚举放置第一个黑子的位置，然后从这个位置开始进行bfs，模拟整个棋盘的变化过程。

具体来说，就是在bfs的每一轮中，对于当前的黑子，分别从8个方向往外走，直到遇到另一个黑子为止。若没有遇到黑子或者中途遇到了空格，那么说明这个方向上的白子不会变色，否则的话当前黑子和遇到的另一个黑子直接的所有白子都会变色，于是可以将这些白子都加入到bfs的队列中。

最后附上python代码：

```python
class Solution(object):
    def flipChess(self, chessboard):
        """
        :type chessboard: List[str]
        :rtype: int
        """

        res = 0
        n = len(chessboard)
        m = len(chessboard[0])
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]

        board_matrix = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if chessboard[i][j] == '.':
                    board_matrix[i][j] = 0
                elif chessboard[i][j] == 'X':
                    board_matrix[i][j] = 1
                else:
                    board_matrix[i][j] = 2

        res = 0
        for i in range(n):
            for j in range(m):
                if board_matrix[i][j] == 0:
                    tmp = [[board_matrix[x][y] for y in range(m)] for x in range(n)]
                    q = [[i, j]]
                    head = 0
                    tail = 1
                    vis = set([(i, j)])
                    while head < tail:
                        for x, y in q[head : tail]:
                            tmp[x][y] = 1
                        for nowx, nowy in q[head : tail]:
                            for index in range(8):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                black_flag = False
                                while x >= 0 and x < n and y >= 0 and y < m:
                                    if tmp[x][y] == 0:
                                        break
                                    elif tmp[x][y] == 1:
                                        black_flag = True
                                        break
                                    else:
                                        x += dx[index]
                                        y += dy[index]
                                
                                if black_flag:
                                    tx = nowx + dx[index]
                                    ty = nowy + dy[index]
                                    while tx != x or ty != y:
                                        if (tx, ty) not in vis:
                                            q.append([tx, ty])
                                            vis.add((tx, ty))
                                        tx += dx[index]
                                        ty += dy[index]
                                
                        
                        head, tail = tail, len(q)

                    res = max(res, len(q) - 1)
        
        return res
```
