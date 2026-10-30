---
title: "488. 祖玛游戏"
aliases: ["yiduobo的每日leetcode 488.祖玛游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/253373327"
zhihu_id: "253373327"
zhihu_title: "yiduobo的每日leetcode 488.祖玛游戏"
question_id: "488"
question: "祖玛游戏"
problem_url: "https://leetcode.cn/problems/zuma-game/"
created: "2020-09-18T23:29:00+08:00"
updated: "2020-09-18T23:29:00+08:00"
upvotes: 0
comments: 0
---

# 488. 祖玛游戏

> **[yiduobo的每日leetcode 488.祖玛游戏](https://zhuanlan.zhihu.com/p/253373327) · 知乎 · 2020-09-18 · 赞同 0**
> 力扣：[488. 祖玛游戏](https://leetcode.cn/problems/zuma-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

488.祖玛游戏<https://leetcode-cn.com/problems/zuma-game/>

题目保证桌上的球不超过20个，且手上的球不超过5个，乍一看以为还是状态压缩动态规划的题目，不过仔细一想不是太好做。如果使用1 \<\< index表示第index位上的球是否被消去，那么这种编码方式就无法处理新插入球的情况。如果对于每种颜色分别编码，那么状态空间就过大了。于是在这里无法使用状态压缩动态规划。

那么是否可以使用普通的区间形式的动态规划呢？答案也是否定的，同样是由于这里存在插入操作，所以可以先插入几个球形成套路，然后再一次性全部消除，此时的f[l][r]是无法表示插入新球的操作的。

于是最后就只能老老实实使用dfs来做了。具体来说就是枚举手上的各类不同的球，尝试将其插入到每一个位置。过程中应该有很多可以优化的地方，我实现的时候是加入了判断当前某个颜色的球是否存在且数量不足3个这一优化，对于插入的策略上已经还可以做一些类似我们玩祖玛时的启发式搜索方案。

另外，我在判断消除的时候是每次都从头开始往后扫描，判断是否存在长度超过3的连续同色球，但是实际上可以从最新一次插入的位置开始往两侧逐步检测，这样效率会更高。

最后附上python代码：

```python
class Solution(object):
    def findMinStep(self, board, hand):
        """
        :type board: str
        :type hand: str
        :rtype: int
        """

        hold_dict = {}
        for ball in hand:
            hold_dict[ball] = hold_dict.get(ball, 0) + 1

        board_dict = {}
        for ball in board:
            board_dict[ball] = board_dict.get(ball, 0) + 1
        
        for ball in board_dict:
            if board_dict[ball] + hold_dict.get(ball, 0) < 3:
                return -1

        self.res = len(hand) + 1
        self.dfs(board, hold_dict, 1)
        if self.res == len(hand) + 1:
            return -1
        return self.res

    def dfs(self, board, hold_dict, depth):
        if depth >= self.res:
            return

        if not hold_dict:
            return

        board_dict = {}
        for ball in board:
            board_dict[ball] = board_dict.get(ball, 0) + 1
        for ball in board_dict:
            if board_dict[ball] + hold_dict.get(ball, 0) < 3:
                return

        for ball in hold_dict:
            if hold_dict[ball] > 0:
                for index in range(0, len(board) + 1):
                    new_board = board[:index] + ball + board[index:]
                    new_board = self.clear_same(new_board)
                    if not new_board:
                        if depth < self.res:
                            self.res = depth
                            return
                    hold_dict[ball] -= 1
                    self.dfs(new_board, hold_dict, depth + 1)
                    hold_dict[ball] += 1

    def clear_same(self, board):
        now = None
        cnt = 0
        for index, ball in enumerate(board):
            if ball == now:
                cnt += 1
            elif cnt >= 3:
                return self.clear_same(board[:index - cnt] + board[index:])
            else:
                now = ball
                cnt = 1
        if cnt >= 3:
            return self.clear_same(board[:len(board) - cnt])
        return board
```
