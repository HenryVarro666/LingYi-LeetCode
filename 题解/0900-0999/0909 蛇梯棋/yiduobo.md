---
title: "909. 蛇梯棋"
aliases: ["yiduobo的每日leetcode 909.蛇梯棋"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "题单/网格图", "题单/面试经典-150-题", "题单/网格图/二-网格图-BFS", "题单/面试经典-150-题/图的广度优先搜索"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354424579"
zhihu_id: "354424579"
zhihu_title: "yiduobo的每日leetcode 909.蛇梯棋"
question_id: "909"
question: "蛇梯棋"
problem_url: "https://leetcode.cn/problems/snakes-and-ladders/"
difficulty: "Medium"
rating: 2020
created: "2021-03-03T23:53:31+08:00"
updated: "2021-03-03T23:53:31+08:00"
upvotes: 0
comments: 0
---

# 909. 蛇梯棋

> **[yiduobo的每日leetcode 909.蛇梯棋](https://zhuanlan.zhihu.com/p/354424579) · 知乎 · 2021-03-03 · 赞同 0**
> 力扣：[909. 蛇梯棋](https://leetcode.cn/problems/snakes-and-ladders/) · Medium · 灵茶山艾府：[BFS，注意可能有环（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

909.蛇梯棋

[力扣](https://leetcode-cn.com/problems/snakes-and-ladders/)

经典的bfs问题。

首先观察棋盘，对于某一行某一列，若当前行的奇偶性与n的奇偶性一致，那么说明当前行为逆序排列，否则为顺序排列。根据这个性质，可以很快得到棋盘上每个格子上数字是多少。在计算的同时，也就可以得知所有的蛇和梯子对应的哪个数字到哪个数字的映射了，使用一个跳跃dict将其储存起来。

接下来，从数字1开始进行bfs。对于当前的数字now，枚举下一步的位置next，范围为now + 1到now + 6。若next在跳跃dict中，那么将next重新置为其跳跃后的值。若next没有被访问过，那么就将其加入到队列中。

当某一轮bfs时发现到达了n \* n，那么当前的轮次就是最终答案，否则说明无解，返回-1。

最后附上python代码：

```python
class Solution(object):
    def snakesAndLadders(self, board):
        """
        :type board: List[List[int]]
        :rtype: int
        """

        jump = {}
        n = len(board)
        for i in range(n):
            for j in range(n):
                if board[i][j] != -1:
                    now = (n - i - 1) * n
                    if i % 2 == n % 2:
                        now += n - j
                    else:
                        now += j + 1
                    jump[now] = board[i][j]
        
        q = [1]
        l = 0
        r = 1
        used = set([1])
        step = 0
        while l < r:
            step += 1
            for now in q[l : r]:
                for next in range(now + 1, now + 7):
                    if next <= n * n:
                        next = jump.get(next, next)
                        if next not in used:
                            used.add(next)
                            q.append(next)
                            if next == n * n:
                                return step
            l, r = r, len(q)

        return -1
```
