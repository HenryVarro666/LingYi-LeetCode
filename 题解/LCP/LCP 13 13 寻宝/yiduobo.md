---
title: "LCP 13. 寻宝"
aliases: ["yiduobo的每日leetcode LCP13.寻宝"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571327655"
zhihu_id: "571327655"
zhihu_title: "yiduobo的每日leetcode LCP13.寻宝"
question_id: "LCP 13"
question: "寻宝"
problem_url: "https://leetcode.cn/problems/xun-bao/"
created: "2022-10-08T00:00:54+08:00"
updated: "2022-10-08T00:00:54+08:00"
upvotes: 0
comments: 0
---

# LCP 13. 寻宝

> **[yiduobo的每日leetcode LCP13.寻宝](https://zhuanlan.zhihu.com/p/571327655) · 知乎 · 2022-10-08 · 赞同 0**
> 力扣：[LCP 13. 寻宝](https://leetcode.cn/problems/xun-bao/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP13.寻宝

[力扣](https://leetcode.cn/problems/xun-bao/)

非常典型的状态压缩动态规划问题，但是由于数据规模的原因，需要做大量的前置准备工作。

首先，最常规的状态为f[x][y][state]表示走到位置(x, y)，已经打开了state中的机关时最少需要走多少步。本题的地图大小为100 \* 100，state的状态值最大可以达到2^16，即使不谈后续的状态转移，光状态表示的复杂度都已经超出限制了，必须进行优化。

注意到本题的格子没有各种花里胡哨的行走和访问限制，且每一块石头可以用无数次，那么在没有机关的地图上，最短的路径就是从起点出发向终点做bfs得到的路径，而在有机关的地图上，行动顺序必然是

起点->石头->机关->石头->机关->...->石头->机关->终点

由于原始的状态f[x][y][state]中state与机关有关系，那么对于上面的行动顺序，可以将到达机关作为里程碑来构造更好的状态表示，即f[state][last]表示在上面的行动顺序中已经打开了state中的机关，且此时停留在last这个机关上时最少需要走多少步。这样一来，状态表示就优化到了一个可以接受的程度。

接下来再来看状态转移。对于f[state][last]，有f[state][last] \= min(f[prev_state][i] + dis(i, stone[k]) + dis(last, stone[k]))。在这里prev_state是state中去除last得到的前置状态，而i是prev_state中的某个机关，dis则表示机关到石头的距离。

对于上面这个转移方程，最后的两项dis在确定了k时可以通过预处理提前计算处理。即从每一个机关或者每一块石头出发进行bfs，找出机关到特定石头的最短距离。更进一步的，在得到这个预处理的距离后，可以两两枚举机关，再枚举作为中继点的石头k，提前预处理出从一个机关走到某个石头，再走到另一个机关的最短距离，并使用数组mech_to_mech保存下来，其中mech_to_mech[i][j]表示从机关i走到某个石头，再走到机关j的最短距离。这样一来，上面的状态转移方程就变成了f[state][last] \= min(f[prev_state][i] + mech_to_mech[last][i])，从而将状态转移的时间复杂度优化到了O(mech_cnt)，这里的mech_cnt为机关的总数。

到了这里，还有两个地方需要进行处理，即起点->石头这一步的距离以及机关->终点这一步的距离。

对于前者，可以认为是动态规划时的某种边界情况，即对于f[state][last]，若其前置状态prev_state为0，说明当前情况是从起点走到某块石头，再走到机关last。对于这种情况，可以参考上面mech_to_mech的做法，也提前预处理出起点走到某块石头，再走到机关的最短距离，使用数组start_to_mech记录下来。

对于后者，则可以在动态规划结束后，遍历每一个机关last，那么此时所需的总步数就是f[-1][last] + dis(last, target)。对于最后这个dis(last, target)，同样可以先从target开始进行bfs预处理出来，并使用数组mech_to_target记录下来。

到了这里，就得到了一个完整的算法。

首先，遍历整张地图，将起点、终点、石头、机关这些特殊位置分别记录下来。

接下来，遍历每一块石头，从这块石头开始进行bfs，找出石头到达机关的最短路径长度，记为mech_to_stone，其中mech_to_stone[i][j]表示从机关i到石头j的最短路径长度。顺带的，在bfs过程中也可以得到从起点到每块石头的距离，即为start_to_stone，其中start_to_stone[i]表示从起点到石头i的最短路径长度。

到了这里，就可以通过中继点石头完成两个数组的预处理，分别为枚举中继点石头，计算出起点到石头，再到某个机关的最短路径长度，记为start_to_mech，其中start_to_mech[i]表示起点到机关i的最短路径距离。另外，还可以两两枚举机关，然后枚举中继点石头，计算出从第一个机关到石头，再到第二个机关的最短路径长度，记为mech_to_mech，其中mech_to_mech[i][j]表示从机关i到某块石头，再到机关j的最短路径长度。

最后，还需要从终点开始进行bfs，计算出起点到终点的距离start_to_target，以及每个机关到终点的最短路径距离，记为mech_to_target，其中mech_to_target[i]表示从机关i到终点的最短路径长度。

至此，预处理工作就全部完成了，接下来开始进行动态规划。

在正式开始之前先处理特殊情况。当地图中没有机关时，答案自然就是start_to_target，否则就可以使用机关的数目mech_cnt计算出最大的状态max_state \= (1 \<\< mech_cnt) - 1，以此来初始化f数组。

接下来枚举每一个机关last，从f[max_state][last]开始进行记忆化搜索。

对于当前的f[state][last]，若f[state][last]不为空，说明之前已经计算过这个状态，直接返回f[state][last]。否则先通过state^(1 \<\< last)计算出state的前置状态prev_state。

若prev_state为0，说明当前是一个边界状态，f[state][last]就等于start_to_mech[last]，否则需要枚举prev_state中的机关i，先递归求解f[prev_state][i]，然后使用f[prev_state][i]和mech_to_mech[i][last]来更新f[state][last]。

最后，不要忘了在得到一个f[max_state][last]后，还需要与mech_to_target[last]相加来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimalSteps(self, maze):
        """
        :type maze: List[str]
        :rtype: int
        """

        mechs = []
        stones = []
        m = len(maze)
        n = len(maze[0])

        for i in range(m):
            for j in range(n):
                if maze[i][j] == 'S':
                    sx = i
                    sy = j
                elif maze[i][j] == 'T':
                    tx = i
                    ty = j
                elif maze[i][j] == 'M':
                    mechs.append([i, j])
                elif maze[i][j] == 'O':
                    stones.append([i, j])
        
        def bfs(x, y, dis):
            dis[x][y] = 0
            q = [[x, y]]
            dx = [0, 1, 0, -1]
            dy = [1, 0, -1, 0]
            head, tail = 0, 1
            while head < tail:
                nowx, nowy = q[head]
                head += 1
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and maze[x][y] != '#' and dis[x][y] == -1:
                        dis[x][y] = dis[nowx][nowy] + 1
                        q.append([x, y])
                        tail += 1

        mech_cnt = len(mechs)
        stone_cnt = len(stones)

        start_to_stone = [-1] * stone_cnt
        mech_to_stone = [[-1] * stone_cnt for _ in range(mech_cnt)]

        for i, stone_pos in enumerate(stones):
            stone_x, stone_y = stone_pos
            dis = [[-1] * n for _ in range(m)]
            bfs(stone_x, stone_y, dis)
            start_to_stone[i] = dis[sx][sy]
            for j, mech_pos in enumerate(mechs):
                mech_x, mech_y = mech_pos
                mech_to_stone[j][i] = dis[mech_x][mech_y]
        
        start_to_mech = [-1] * mech_cnt
        for i in range(mech_cnt):
            for j in range(stone_cnt):
                if start_to_stone[j] == -1 or mech_to_stone[i][j] == -1:
                    continue
                if start_to_mech[i] == -1 or start_to_mech[i] > start_to_stone[j] + mech_to_stone[i][j]:
                    start_to_mech[i] = start_to_stone[j] + mech_to_stone[i][j]
        
        mech_to_mech = [[-1] * mech_cnt for _ in range(mech_cnt)]
        for i in range(mech_cnt - 1):
            for j in range(i + 1, mech_cnt):
                for k in range(stone_cnt):
                    if mech_to_stone[i][k] == -1 or mech_to_stone[j][k] == -1:
                        continue
                    if mech_to_mech[i][j] == -1 or mech_to_mech[i][j] > mech_to_stone[i][k] + mech_to_stone[j][k]:
                        mech_to_mech[i][j] = mech_to_stone[i][k] + mech_to_stone[j][k]
                
                mech_to_mech[j][i] = mech_to_mech[i][j]

        dis = [[-1] * n for _ in range(m)]
        bfs(tx, ty, dis)
        start_to_target = dis[sx][sy]
        mech_to_target = [-1] * mech_cnt
        for i, mech_pos in enumerate(mechs):
            mech_x, mech_y = mech_pos
            mech_to_target[i] = dis[mech_x][mech_y]

        if mech_cnt == 0:
            return start_to_target
        
        res = -1
        max_state = (1 << mech_cnt) - 1
        f = [[None] * mech_cnt for _ in range(max_state + 1)]

        def dfs(state,last, f):
            if f[state][last] is not None:
                return f[state][last]

            prev_state = (state ^ (1 << last))
            if prev_state == 0:
                f[state][last] = start_to_mech[last]
                return f[state][last]
            else:
                f[state][last] = -1
                for i in range(mech_cnt):
                    if mech_to_mech[last][i] == -1:
                        continue
                    if (prev_state & (1 << i)) == (1 << i):
                        dfs(prev_state, i, f)
                        if f[prev_state][i] != -1:
                            if f[state][last] == -1 or f[state][last] > f[prev_state][i] + mech_to_mech[last][i]:
                                f[state][last] = f[prev_state][i] + mech_to_mech[last][i]
                return f[state][last]

        for i in range(mech_cnt):
            if mech_to_target[i] != -1:
                dfs(max_state, i, f)
                if f[max_state][i] is not None and f[max_state][i] != -1 and (res == -1 or res > f[max_state][i] + mech_to_target[i]):
                    res = f[max_state][i] + mech_to_target[i]
            
        return res
```
