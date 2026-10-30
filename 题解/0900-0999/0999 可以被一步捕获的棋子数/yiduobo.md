---
title: "999. 可以被一步捕获的棋子"
aliases: ["yiduobo的每日leetcode 999.可以被一步捕获的棋子"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365674079"
zhihu_id: "365674079"
zhihu_title: "yiduobo的每日leetcode 999.可以被一步捕获的棋子"
question_id: "999"
question: "可以被一步捕获的棋子数"
problem_url: "https://leetcode.cn/problems/available-captures-for-rook/"
difficulty: "Easy"
created: "2021-04-17T21:00:40+08:00"
updated: "2021-04-17T21:00:40+08:00"
upvotes: 0
comments: 0
---

# 999. 可以被一步捕获的棋子

> **[yiduobo的每日leetcode 999.可以被一步捕获的棋子](https://zhuanlan.zhihu.com/p/365674079) · 知乎 · 2021-04-17 · 赞同 0**
> 力扣：[999. 可以被一步捕获的棋子数](https://leetcode.cn/problems/available-captures-for-rook/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

999.可以被一步捕获的棋子

[力扣](https://leetcode-cn.com/problems/available-captures-for-rook/)

比较基础的题目，从R的位置开始向四个方向探索，直到走出边界或者碰到棋子。若某个方向上是因为碰到棋子p结束，那么就将答案加1。

最后附上python代码：

```python
class Solution(object):
    def numRookCaptures(self, board):
        """
        :type board: List[List[str]]
        :rtype: int
        """

        for i in range(8):
            flag = False
            for j in range(8):
                if board[i][j] == 'R':
                    flag = True
                    break
            if flag:
                break
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        res = 0
        for index in range(4):
            x = i + dx[index]
            y = j + dy[index]
            while x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == '.':
                x += dx[index]
                y += dy[index]
            
            if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == 'p':
                res += 1
        
        return res
```
