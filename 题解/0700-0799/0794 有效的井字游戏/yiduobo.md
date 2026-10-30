---
title: "794. 有效的井字游戏"
aliases: ["yiduobo的每日leetcode 794.有效的井字游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341868326"
zhihu_id: "341868326"
zhihu_title: "yiduobo的每日leetcode 794.有效的井字游戏"
question_id: "794"
question: "有效的井字游戏"
problem_url: "https://leetcode.cn/problems/valid-tic-tac-toe-state/"
created: "2021-01-04T22:55:11+08:00"
updated: "2021-01-04T22:55:11+08:00"
upvotes: 0
comments: 0
---

# 794. 有效的井字游戏

> **[yiduobo的每日leetcode 794.有效的井字游戏](https://zhuanlan.zhihu.com/p/341868326) · 知乎 · 2021-01-04 · 赞同 0**
> 力扣：[794. 有效的井字游戏](https://leetcode.cn/problems/valid-tic-tac-toe-state/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

794.有效的井字游戏

[力扣](https://leetcode-cn.com/problems/valid-tic-tac-toe-state/)

题目本身难度并不大，但是需要注意的细节比较多。

首先，合法的最终状态可能是X赢、O赢、胜负未分，那么对于这三种状态：

1、X赢。此时X必须有三连，X的数量必须比O的数量多1，且O此时没有达成三连。

2、O赢。此时O必须有三连，O的数量必须等于X的数量，且X此时没有达成三连。

3、胜负未分。此时X和O的数量可以相等，或者X比O多一个，且X和O都没有达成三连。

根据上面的结论，我们可以统计X和O的数量，并判断X和O是否达成三连。需要注意的是，当有5个X和4个O时，X是有可能达成两组三连的，此时为合法状态。其他情况下的两组三连都是不合法的，但是都可以通过X和O的数量进行排除，因此无需进行判断。

需要注意对角线上的三连不要忘了判断。

有了X和O的数量，以及三连情况，就可以根据之前的结论进行判断：

1、若X的数量比O数量少，或者X的数量比O的数量多出超过1，那么不合法

2、若X和O同时达成了三连，那么不合法

3、若X达成了三连，且X和O的数量相同，那么不合法

4、若O达成了三连，且X的数量多于O的数量，那么不合法

5、其他情况下，都是合法的

最后附上python代码：

```python
class Solution(object):
    def validTicTacToe(self, board):
        """
        :type board: List[str]
        :rtype: bool
        """

        cnt_x = cnt_o = 0
        col_x = [0, 0, 0]
        col_o = [0, 0, 0]
        row_x = [0, 0, 0]
        row_o = [0, 0, 0]
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'X':
                    cnt_x += 1
                    row_x[i] += 1
                    col_x[j] += 1
                elif board[i][j] == 'O':
                    cnt_o += 1
                    row_o[i] += 1
                    col_o[j] += 1

        delta = cnt_x - cnt_o
        if delta < 0 or delta > 1:
            return False

        win_x = win_o = False
        for i in range(3):
            if row_x[i] == 3 or col_x[i] == 3:
                win_x = True
            if row_o[i] == 3 or col_o[i] == 3:
                win_o = True
        
        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'O':
                win_o = True
            elif board[0][0] == 'X':
                win_x = True
        
        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == 'O':
                win_o = True
            elif board[0][2] == 'X':
                win_x = True

        if win_x and win_o:
            return False

        if delta == 0 and win_x:
            return False

        if delta == 1 and win_o:
            return False

        return True
```
