---
title: "3552. 网络传送门旅游"
aliases: ["yiduobo的每日leetcode 3552.网络传送门旅游"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/queue", "leetcode/shortest-path", "题单/网格图", "题单/网格图/三-网格图-0-1-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909678077769908704"
zhihu_id: "1909678077769908704"
zhihu_title: "yiduobo的每日leetcode 3552.网络传送门旅游"
question_id: "3552"
question: "网格传送门旅游"
problem_url: "https://leetcode.cn/problems/grid-teleportation-traversal/"
difficulty: "Medium"
rating: 2036
created: "2025-05-24T18:42:01+08:00"
updated: "2025-05-24T18:42:01+08:00"
upvotes: 0
comments: 1
---

# 3552. 网络传送门旅游

> **[yiduobo的每日leetcode 3552.网络传送门旅游](https://zhuanlan.zhihu.com/p/1909678077769908704) · 知乎 · 2025-05-24 · 赞同 0**
> 力扣：[3552. 网格传送门旅游](https://leetcode.cn/problems/grid-teleportation-traversal/) · Medium · 灵茶山艾府：[0-1 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3552.网络传送门旅游

[3552. 网格传送门旅游 - 力扣（LeetCode）](https://leetcode.cn/problems/grid-teleportation-traversal/)

题目给出一个大小为m \* n的二维字符网格matrix，其中matrix[i][j]可能有以下几种可能：

'.' 表示一个空的单元格

'\#' 表示一个障碍物

'A'到'Z'之间的大写字母，表示一个传送门

现在要求从左上角(0, 0)出发，目标是到达右下角(m - 1, n - 1)，每次可以向上下左右四个方向移动，但是不能越界也不能走到障碍物上。

另外对于大写字母的单元格，如果之前没有使用过该字母对应的传送门，那么就可以通过该传送门传送到具有相同字母的另一个单元格内，这次传送不计入移动次数。每种字母对应的传送门只能使用一次。

问到达右下角所需的最少移动次数，若无法到达，则返回-1。

如果不考虑传送门的影响，本题就是很常规的bfs，直接从左上角开始执行bfs就行了。

对于传送门单元格，如果需要使用某种传送门的话，就应该在首次遇到这种传送门的时候就使用，因为使用传送门可以到达的单元格是相同的，而首次到达这种传送门所需的时间显然小于等于第k次到达这种传送门所需的时间。换言之，只需在常规的bfs中稍作修改，当遇到某个传送门单元格时，直接将可达的所有单元格也加入到bfs的队列中就行了，而这些单元格被加入队列中之后，因为去重的作用，也不需要担心再次走到具有相同传送门的单元格而影响到时间复杂度。

另外需要特别注意类似样例一中出生点就是传送门的情况，这种情况下应该使用所有传送门可达的点来初始化bfs的队列，而不是只有(0, 0)。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, matrix):
        """
        :type matrix: List[str]
        :rtype: int
        """
        
        m = len(matrix)
        n = len(matrix[0])

        transport = {}
        for i in range(m):
            for j in range(n):
                if 'A' <= matrix[i][j] <= 'Z':
                    if matrix[i][j] not in transport:
                        transport[matrix[i][j]] = []
                    transport[matrix[i][j]].append((i, j))
    
        q = deque()
        dis = [[-1] * n for _ in range(m)]
        if 'A' <= matrix[0][0] <= 'Z':
            for x, y in transport[matrix[0][0]]:
                q.append((x, y))
                dis[x][y] = 0
        else:
            q.append((0, 0))
            dis[0][0] = 0
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while q:
            nowx, nowy = q.popleft()
            for d in range(4):
                x = nowx + dx[d]
                y = nowy + dy[d]
                if 0 <= x < m and 0 <= y < n and matrix[x][y] != '#' and dis[x][y] == -1:
                    if 'A' <= matrix[x][y] <= 'Z':
                        for tx, ty in transport[matrix[x][y]]:
                            q.append((tx, ty))
                            dis[tx][ty] = dis[nowx][nowy] + 1
                    else:
                        q.append((x, y))
                        dis[x][y] = dis[nowx][nowy] + 1
        
        return dis[-1][-1]
```
