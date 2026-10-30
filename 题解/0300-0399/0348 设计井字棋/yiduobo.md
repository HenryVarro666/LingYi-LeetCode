---
title: "348. 设计井字棋"
aliases: ["yiduobo的每日leetcode 348.设计井字棋"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597207426"
zhihu_id: "597207426"
zhihu_title: "yiduobo的每日leetcode 348.设计井字棋"
question_id: "348"
question: "设计井字棋"
problem_url: "https://leetcode.cn/problems/design-tic-tac-toe/"
created: "2023-01-07T01:08:55+08:00"
updated: "2023-01-07T01:08:55+08:00"
upvotes: 0
comments: 0
---

# 348. 设计井字棋

> **[yiduobo的每日leetcode 348.设计井字棋](https://zhuanlan.zhihu.com/p/597207426) · 知乎 · 2023-01-07 · 赞同 0**
> 力扣：[348. 设计井字棋](https://leetcode.cn/problems/design-tic-tac-toe/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

348.设计井字棋

[力扣](https://leetcode.cn/problems/design-tic-tac-toe/)

游戏将在某一行、列或者两条对角线被填上同样的棋子后结束，那么问题就变成了如何高效地判断当某个玩家放置棋子之后是否存在某一行、列或者两条对角线上被填充上了同样的棋子。对于这个问题，可以参考皇后问题的处理方法，利用哈希表储存所有行、列以及两条对角线上已经有多少枚相同的棋子。当相同的棋子到达n枚时，当前玩家就胜利了。

最后附上python代码：

```python
class TicTacToe(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.n = n
        self.row = [0] * n
        self.col = [0] * n
        self.left = self.right = 0

    def move(self, row, col, player):
        """
        :type row: int
        :type col: int
        :type player: int
        :rtype: int
        """
        if player == 1:
            delta = 1
        else:
            delta = -1
        
        self.row[row] += delta
        self.col[col] += delta
        if row == col:
            self.left += delta
        if row == self.n - 1 - col:
            self.right += delta

        if abs(self.row[row]) == self.n or abs(self.col[col]) == self.n or abs(self.left) == self.n or abs(self.right) == self.n:
            return player
        
        return 0

# Your TicTacToe object will be instantiated and called as such:
# obj = TicTacToe(n)
# param_1 = obj.move(row,col,player)
```
