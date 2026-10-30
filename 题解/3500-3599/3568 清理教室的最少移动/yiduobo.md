---
title: "3568. 清理教室的最少移动"
aliases: ["yiduobo的每日leetcode 3568.清理教室的最少移动"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/breadth-first-search", "题单/网格图", "题单/动态规划", "题单/网格图/五-综合应用", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936201428977836610"
zhihu_id: "1936201428977836610"
zhihu_title: "yiduobo的每日leetcode 3568.清理教室的最少移动"
question_id: "3568"
question: "清理教室的最少移动"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-clean-the-classroom/"
difficulty: "Medium"
rating: 2143
created: "2025-08-05T23:31:30+08:00"
updated: "2025-08-05T23:31:30+08:00"
upvotes: 0
comments: 0
---

# 3568. 清理教室的最少移动

> **[yiduobo的每日leetcode 3568.清理教室的最少移动](https://zhuanlan.zhihu.com/p/1936201428977836610) · 知乎 · 2025-08-05 · 赞同 0**
> 力扣：[3568. 清理教室的最少移动](https://leetcode.cn/problems/minimum-moves-to-clean-the-classroom/) · Medium · 灵茶山艾府：[BFS + 优化，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3568.清理教室的最少移动

[3568. 清理教室的最少移动 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-clean-the-classroom/description/)

题目给出一个m \* n的网格图，其中m和n的大小都不超过20，现在有一个学生需要清理散布在教室中的垃圾。

网格图中的每个单元格是以下字符之一：

'S'：学生的起始位置

'L'：需要收集的垃圾，在收集后，单元格将变为空白。垃圾的总数不超过10个。

'R'：休息区，可以让学生的能量恢复到最大值。每个休息区都可以使用多次。

'X'：障碍物，无法通过

'.'：空白空间

另外给出给出一个整数energy，表示学生的最大能量容量，其大小不超过50。学生从'S'开始，带着energy的能量开始收集垃圾。每一轮，学生都可以移动到上下左右四个相邻的单元格之一，需要消耗1单位能量。若能量变为0，学生只能在休息区恢复能量才能继续移动。

问收集所有垃圾所需的最少移动次数，若无法收集全部的垃圾，则返回-1。

首先可以明确的是，收集垃圾的顺序肯定是有讲究的，而且也没有明显的贪心方案，因此在这里大概率需要用到动态规划。又注意到垃圾的总数不超过10个，因此在这里可以通过状态压缩将目前已经收集了的垃圾表示出来。

另一方面，学生的行动方案也受能量值的影响，因此在这里就可以用f[x][y][e][s]表示当学生处于单元格(x, y)，还剩下e的能量值，已经收集了状态表示为s的垃圾所需的最少移动次数。

每一次行动只能走到四个相邻的单元格，因此在这里可以直接通过bfs来完成状态转移。具体来说，对于当前状态f[now_x][now_y][now_e][now_s]，可以枚举其四个相邻单元格，对于当前枚举到的(nxt_x, nxt_y)，首先需要保证这个单元格不能是障碍物，接下来需要计算走到该单元格后nxt_e和nxt_s：

1、若(nxt_x, nxt_y)是休息区，那么nxt_e将回复到energy，而nxt_s则保持为now_s不变

2、若(nxt_x, nxt_y)是未收集的垃圾，那么nxt_e等于now_e减1，而nxt_s则需要在now_s的基础上添加当前单元格上的垃圾对应的状态

3、其他情况下，nxt_e等于now_e减1，而nxt_s保持now_s不变

得到nxt_e和nxt_s之后，若f[nxt_x][nxt_y][nxt_e][nxt_s]还没有被访问过，那么就是用f[now_x][now_y][now_e][now_s] + 1来更新f[nxt_x][nxt_y][nxt_e][nxt_s]，然后将其加入到bfs的队列中。

粗略计算来看，状态空间为m \* n \* energy \* 2^count_L，极限情况下可以达到20 \* 20 \* 50 \* 1024，还是比较微妙的，需要进行一些优化。

最直观的想法自然是全部收集完时直接退出，以及能量归0时无需将当前状态加入队列。

另一方面，也需要尽量保证不要反复横跳，但是就bfs的形式而言，很难避免这种情况发生。实际上，并非所有的反复横跳都是无意义的，因为可能在这个过程中完成了能量的补充或者垃圾的收集。基于这一点，可以使用一个最优化数组best_energy[x][y][s]表示处于(x, y)且已经收集了状态表示为s的垃圾时可以剩下的最大体力，那么在bfs过程中，如果f[nxt_x][nxt_y][nxt_e][nxt_s]中的nxt_e小于等于best_energy[nxt_x][nxt_y][nxt_s]，那么就没有必要更新这个状态了，因为之前某一次走到(nxt_x, nxt_y)且收集了nxt_s的垃圾时剩余的体力更多，此时如果再走到(nxt_x, nxt_y)的话就意味着此间的所有操作都是无用功，显然是不优的。反之，则需要使用nxt_e来更新best_energy[nxt_x][nxt_y][nxt_s]，然后再继续进行bfs。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, classroom, energy):
        """
        :type classroom: List[str]
        :type energy: int
        :rtype: int
        """

        m = len(classroom)
        n = len(classroom[0])

        sx, sy = None, None
        garbadge_id = {}

        for i in range(m):
            for j in range(n):
                if classroom[i][j] == 'L':
                    garbadge_id[(i, j)] = len(garbadge_id)
                elif classroom[i][j] == 'S':
                    sx = i
                    sy = j

        if not garbadge_id:
            return 0

        max_state = (1 << len(garbadge_id)) - 1

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        f = [[[[None] * (max_state + 1) for _ in range(energy + 1)] for _ in range(n)] for _ in range(m)]
        best_energy = [[[None] * (max_state + 1) for _ in range(n)] for _ in range(m)]
        q = deque()
        q.append((sx, sy, energy, 0))
        f[sx][sy][energy][0] = 0
        best_energy[sx][sy][0] = energy

        while q:
            now_x, now_y, now_e, now_s = q.popleft()
            for d in range(4):
                nxt_x = now_x + dx[d]
                nxt_y = now_y + dy[d]
                if 0 <= nxt_x < m and 0 <= nxt_y < n and classroom[nxt_x][nxt_y] != 'X':
                    if classroom[nxt_x][nxt_y] == 'R':
                        nxt_e = energy
                        nxt_s = now_s
                    else:
                        nxt_e = now_e - 1
                        if classroom[nxt_x][nxt_y] == 'L':
                            delta_s = 1 << garbadge_id[(nxt_x, nxt_y)]
                            nxt_s = now_s | delta_s
                        else:
                            nxt_s = now_s
                    
                    if f[nxt_x][nxt_y][nxt_e][nxt_s] is None and (best_energy[nxt_x][nxt_y][nxt_s] is None or best_energy[nxt_x][nxt_y][nxt_s] < nxt_e):
                        best_energy[nxt_x][nxt_y][nxt_s] = nxt_e
                        if nxt_e > 0:
                            q.append((nxt_x, nxt_y, nxt_e, nxt_s))
                        f[nxt_x][nxt_y][nxt_e][nxt_s] = f[now_x][now_y][now_e][now_s] + 1
                        if nxt_s == max_state:
                            return f[nxt_x][nxt_y][nxt_e][nxt_s]
    
        return -1
```
