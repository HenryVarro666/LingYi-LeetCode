---
title: "803. 打砖块"
aliases: ["yiduobo的每日leetcode 803.打砖块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342955042"
zhihu_id: "342955042"
zhihu_title: "yiduobo的每日leetcode 803.打砖块"
question_id: "803"
question: "打砖块"
problem_url: "https://leetcode.cn/problems/bricks-falling-when-hit/"
created: "2021-01-09T00:19:24+08:00"
updated: "2021-01-09T00:19:24+08:00"
upvotes: 0
comments: 0
---

# 803. 打砖块

> **[yiduobo的每日leetcode 803.打砖块](https://zhuanlan.zhihu.com/p/342955042) · 知乎 · 2021-01-09 · 赞同 0**
> 力扣：[803. 打砖块](https://leetcode.cn/problems/bricks-falling-when-hit/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

803.打砖块

[力扣](https://leetcode-cn.com/problems/bricks-falling-when-hit/)

很有意思的题目。如果将矩阵中的每个格子看做图中的一个点，那么可以假设存在一个额外节点，其中矩阵中第0行的所有点与额外节点相连。现在问按顺序删去图中的某些点是否能将图划分为多个部分，若可以那么划分出去的节点个数为多少。

在无向图中，这类将图划分为多个部分的点被称作关节点，一般可以利用tarjan算法一遍dfs求解出来。但是需要注意的是，这里的图是动态变化的，在这一轮删去某个点之后，可能会导致图中某个点变为关节点，因此使用tarjan算法是行不通的。

另一个自然的想法就是对于图中的任意点，想办法求解出该点是依靠哪个或者哪些相邻的点才能与额外节点连接上的。不过这个做法有个问题就是预处理的顺序不太好确定，即对于A和B两点，可能存在A依赖B，B依赖A，A和B可以互相依赖这几种情况，那么应该先处理哪个节点就不太好确定了。

既然靠删节点的做法行不通，那么就索性将hits中的节点先全部删了，然后逆序遍历hits逐个再加回来。若当前新加的节点将若干篇不与额外节点相连的部分重新连接到额外节点上，那么说明正向操作时删去该节点将使得这几个部分脱落，那么这几个部分的节点个数就是这次删除掉落的砖块数量。对于连接成片这个操作，很自然就想到了使用并查集来做，于是现在就有了一种做法：

1、首先将grid中所有出现在hits中的格子对应的值减去1

2、接下来遍历grid的第0行，若当前位置值等于1，那么将其加入到bfs队列中。接下来开始执行bfs，将相邻节点加入到队列中。执行完bfs之后，队列中的所有点就是最终状态下依然与额外节点相邻的点，我们将其染色为0。

3、接下来从第1行开始遍历grid，若当前位置等于1，且未被染色，那么就将从该位置开始向相邻位置进行bfs。执行完bfs之后就得了一个新的不与额外节点相邻的片区。将其从1开始进行染色，同时记录下当前颜色对应的片区一共有多少个节点。

4、现在我们有了最终状态下的若干个片区以及其对应的节点数量，接下来开始逆序遍历hits。对于hits当前的位置(x, y)，若其对应的grid[x][y]不等于0，说明该位置之前并没有砖块，因此将0加入到答案中，然后继续遍历hits。若grid[x][y]等于0，则说明这是一个被移除的砖块，那么就考察其连接着哪些片区。

对于连接的这些片区，则有几种情况：

4-1）未连接任何片区，(x, y)是新出现的孤立节点：

此时说明(x, y)在更早之前的某次操作已经被移除了，因此将0加入到答案中，同时将(x, y)看做新的片区并染为新的颜色，记录其节点数为1。

4-2）连接的片区中没有颜色为0的片区：

此时说明(x, y)分割了几个片区，但这些片区早先已经被移除了，因此将0加入到答案中，同时将(x, y)以及这些片区的颜色都染成最小的颜色，将最小颜色对应的节点数目更新为当前被分割片区的节点数目之和加一，这里的加一代表的(x, y)。

4-3）连接的片区中有颜色为0的片区：

此时说明移除(x, y)之后，其连接的颜色不为0的片区都将掉落，因此统计这些片区的节点数目之和并加入到答案中，同时将(x, y)以及这些片区的颜色染成0。

这里需要注意的是，当x \= 0时，说明直接就与额外节点相邻了，因此此时可以认为连接上了颜色为0的片区。而这里判断颜色和染色的操作则交个并查集来处理。

最后附上python代码：

```python
class Solution(object):
    def hitBricks(self, grid, hits):
        """
        :type grid: List[List[int]]
        :type hits: List[List[int]]
        :rtype: List[int]
        """

        
        m = len(grid)
        n = len(grid[0])
        color = [[None] * n for _ in range(m)]

        for x, y in hits:
            grid[x][y] -= 1

        now = 0
        q = []
        cnt = []
        for j in range(n):
            if grid[0][j] == 1:
                color[0][j] = now
                q.append([0, j])
        self.bfs(q, m, n, grid, color, now, cnt)
        now += 1

        for i in range(1, m):
            for j in range(n):
                if grid[i][j] == 1 and color[i][j] is None:
                    color[i][j] = now
                    q = [[i, j]]
                    self.bfs(q, m, n, grid, color, now, cnt)
                    now += 1
        
        fa = [x for x in range(now)]
        res = []
        hits.reverse()
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        for nowx, nowy in hits:
            if grid[nowx][nowy] == 0:
                drop = set()
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                        drop.add(color[x][y])

                

                grid[nowx][nowy] = 1
                tmp = 0
                if nowx == 0:
                    min_fa = 0
                else:
                    min_fa = now
                drop_fa_set = set()
                for drop_color in drop:
                    drop_fa = self.find(drop_color, fa)
                    min_fa = min(min_fa, drop_fa)
                    if drop_fa != 0 and drop_fa not in drop_fa_set:
                        tmp += cnt[drop_fa]
                        drop_fa_set.add(drop_fa)
                
                if min_fa == 0:
                    res.append(tmp)
                    color[nowx][nowy] =0
                else:
                    res.append(0)
                    color[nowx][nowy] = min_fa
                    if min_fa == now:
                        fa.append(min_fa)
                        cnt.append(tmp + 1)
                        now += 1
                    else:
                        cnt[min_fa] = tmp + 1

                for drop_fa in drop_fa_set:
                    fa[drop_fa] = min_fa
                
            else:
                res.append(0)

        res.reverse()
        return res

    def find(self, drop_color, fa):
        if fa[drop_color] != drop_color:
            tmp = self.find(fa[drop_color], fa)
            fa[drop_color] = tmp

        return fa[drop_color]

    def bfs(self, q, m, n, grid, color, now, cnt):
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        l = 0
        r = len(q)
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x < m and y >=0 and y < n and grid[x][y] == 1 and color[x][y] is None:
                    color[x][y] = now
                    q.append([x, y])
                    r += 1
        
        cnt.append(len(q))
```
