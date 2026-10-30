---
title: "1275. 找出井字棋的获胜者"
aliases: ["yiduobo的每日leetcode 1275.找出井字棋的获胜者"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387956255"
zhihu_id: "387956255"
zhihu_title: "yiduobo的每日leetcode 1275.找出井字棋的获胜者"
question_id: "1275"
question: "找出井字棋的获胜者"
problem_url: "https://leetcode.cn/problems/find-winner-on-a-tic-tac-toe-game/"
created: "2021-07-08T23:28:15+08:00"
updated: "2021-07-08T23:28:15+08:00"
upvotes: 2
comments: 0
---

# 1275. 找出井字棋的获胜者

> **[yiduobo的每日leetcode 1275.找出井字棋的获胜者](https://zhuanlan.zhihu.com/p/387956255) · 知乎 · 2021-07-08 · 赞同 2**
> 力扣：[1275. 找出井字棋的获胜者](https://leetcode.cn/problems/find-winner-on-a-tic-tac-toe-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1275.找出井字棋的获胜者

[力扣](https://leetcode-cn.com/problems/find-winner-on-a-tic-tac-toe-game/)

比较基础的题目，直接遍历moves，模拟下棋的过程。每一轮放置好棋子之后，都检测当前棋子所在的行、列上的棋子是否一样。另外，若当前位置在左右对角线上，则还需要额外检测对角线上的棋子是否一致。

对于对角线的检测，左对角线上的点都满足横纵坐标之和为2，而右对角线上的点则满足横纵坐标相等。

遍历完成后，若仍未分出胜负，那么就根据moves的长度是否等于9来决定答案是draw还是pending。

最后附上python代码：

```python
class Solution(object):
    def tictactoe(self, moves):
        """
        :type moves: List[List[int]]
        :rtype: str
        """
        
        g = [[None] * 3 for _ in range(3)]
        for index in range(len(moves)):
            x, y = moves[index]
            g[x][y] = index % 2
            if g[x][0] == g[x][1] and g[x][0] == g[x][2]:
                return chr(65 + index % 2)
            if g[0][y] == g[1][y] and g[0][y] == g[2][y]:
                return chr(65 + index % 2)
            if x + y == 2 and g[0][2] == g[1][1] and g[0][2] == g[2][0]:
                return chr(65 + index % 2)
            if x == y and g[0][0] == g[1][1] and g[0][0] == g[2][2]:
                return chr(65 + index % 2)
        
        if len(moves) == 9:
            return "Draw"
        
        return "Pending"
```
