---
title: "3283. 吃掉所有兵需要的最多移动次数"
aliases: ["yiduobo的每日leetcode 3283.吃掉所有兵需要的最多移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/game-theory", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/822763662"
zhihu_id: "822763662"
zhihu_title: "yiduobo的每日leetcode 3283.吃掉所有兵需要的最多移动次数"
question_id: "3283"
question: "吃掉所有兵需要的最多移动次数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/"
difficulty: "Hard"
rating: 2473
created: "2024-10-06T00:58:12+08:00"
updated: "2024-10-06T00:58:12+08:00"
upvotes: 1
comments: 0
---

# 3283. 吃掉所有兵需要的最多移动次数

> **[yiduobo的每日leetcode 3283.吃掉所有兵需要的最多移动次数](https://zhuanlan.zhihu.com/p/822763662) · 知乎 · 2024-10-06 · 赞同 1**
> 力扣：[3283. 吃掉所有兵需要的最多移动次数](https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/) · Hard · 灵茶山艾府：[相邻相关排列型状压 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3283.吃掉所有兵需要的最多移动次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/description/)

题目给出一个50 \* 50的国际象棋棋盘，棋盘上有一个马和若干的兵。

接下来给出两个整数kx和ky，表示棋盘的马初始位置在(kx, ky)。另外给出一个二维数组positions，其中positions\[i\] \= \[x\[i\], y\[i\]\]，表示第i个兵位于(x\[i\], y\[i\])。棋盘上兵的数目不超过15个。

alice和bob针对这个棋局在进行一个回合制的游戏，alice先手。

每一次操作，当前玩家都需要选择棋盘上的任意一个兵，然后移动马，通过最少得步数踩掉这个兵。马在移动的过程中可能会踩到其他没有被选择的兵，但是这些兵并不会被吃掉，只有被选择的兵才会被吃掉。

alice的目标是让两名玩家的总移动次数最多，而bob的目标则是让两名玩家的总移动次数最少。若alice和bob都采取最佳策略，问最终可以达到的最大移动次数是多少。

题目中马的移动只会对目标兵产生影响，且一定是按照最少步数来移动的，那么在这里就可以先从马以及每个兵的位置开始分别做bfs，预处理出初始状态下马踩掉每个兵所需的步数knight2pawn，以及马从任意一个兵的位置开始跳到另一个兵所需的最少步数pawn2pawn。

接下来就是二人博弈问题的经典交替式动态规划了，另外为了保留兵的状态，还需要用上状态压缩。

令f[sign][now_state][last]表示当前玩家为sign，当前已经被踩掉的兵的状态表示为now_state，且马当前停留在下标为last的棋子原先的坐标上时的最优步数。当sign为1时，玩家为alice，此时就希望f越大越好，反之当sign为0时，玩家为bob，那么此时就希望f越小越好。

接下来对于f[sign][now_state][last]，若now_state等于max_state，即已经踩掉了所有的兵，那么f[sign][now_state][last] \= 0，否则就遍历所有的兵，对于当前遍历到的第index个兵，若(1 \<\< index)没有出现在now_state中，那么就说明这个兵还没有被踩掉，而踩掉这个兵的代价则为f[1 - sign][now_state | (1 \<\< index)][index] + pawn2pawn[last][index]，即从last出发踩掉index的代价pawn2pawn[last][index]，再加上换手后对手的能操作得到的最优解。

需要注意的是，此时若sign \= 0时，应该取最小的代价作为对应的f值，而当sign \= 1时，则应该取最大的代价作为对应的f值。

以上的过程计算的是从某个兵的位置开始可以得到的最优解，那么还需要在最外层先枚举alice第一步操作时应该让马踩掉哪个兵，具体来说，踩掉index这个兵的代价为f[0][1 \<\< index][index] + knight2pawn[index]，取这里面的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxMoves(self, kx, ky, positions):
        """
        :type kx: int
        :type ky: int
        :type positions: List[List[int]]
        :rtype: int
        """

        dx = [-2, -1, 1, 2, 2, 1, -1, -2]
        dy = [1, 2, 2, 1, -1, -2, -2, -1]

        def bfs(sx, sy):
            q = [[sx, sy]]
            dis = [[None] * 50 for _ in range(50)]
            dis[sx][sy] = 0

            head, tail = 0, 1
            while head < tail:
                for nowx, nowy in q[head : tail]:
                    for d in range(8):
                        x = nowx + dx[d]
                        y = nowy + dy[d]
                        if 0 <= x < 50 and 0 <= y < 50 and dis[x][y] is None:
                            dis[x][y] = dis[nowx][nowy] + 1
                            q.append([x, y])
                
                head, tail = tail, len(q)
            
            dis_list = []
            for x, y in positions:
                dis_list.append(dis[x][y])
            
            return dis_list
        
        knight2pawn = bfs(kx, ky)
        pawn2pawn = []
        for x, y in positions:
            pawn2pawn.append(bfs(x, y))
        
        n = len(positions)
        max_state = (1 << n) - 1
        f = [[[None] * n for _ in range(max_state + 1)] for _ in range(2)]

        def dfs(f, sign, now_state, last):
            if f[sign][now_state][last] is not None:
                return f[sign][now_state][last]
            if now_state == max_state:
                f[sign][now_state][last] = 0
            else:
                best = None
                for index in range(n):
                    if now_state & (1 << index) == 0:
                        nxt_state = now_state | (1 << index)
                        cost = dfs(f, 1 - sign, nxt_state, index) + pawn2pawn[last][index]
                        if best is None:
                            best = cost
                        elif sign == 0:
                            best = min(best, cost)
                        else:
                            best = max(best, cost)
                
                f[sign][now_state][last] = best
            
            return f[sign][now_state][last]

        res = 0
        for index in range(n):
            res = max(res, knight2pawn[index] + dfs(f, 0, (1 << index), index))
        
        return res
```
