---
title: "LCP 31. 变换的迷宫"
aliases: ["yiduobo的每日leetcode LCP31.变换的迷宫"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/dfs", "题单/网格图", "题单/网格图/五-综合应用"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574135811"
zhihu_id: "574135811"
zhihu_title: "yiduobo的每日leetcode LCP31.变换的迷宫"
question_id: "LCP 31"
question: "变换的迷宫"
problem_url: "https://leetcode.cn/problems/Db3wC1/"
difficulty: "Hard"
created: "2022-10-16T18:29:48+08:00"
updated: "2022-10-16T18:29:48+08:00"
upvotes: 0
comments: 0
---

# LCP 31. 变换的迷宫

> **[yiduobo的每日leetcode LCP31.变换的迷宫](https://zhuanlan.zhihu.com/p/574135811) · 知乎 · 2022-10-16 · 赞同 0**
> 力扣：[LCP 31. 变换的迷宫](https://leetcode.cn/problems/Db3wC1/) · Hard · 灵茶山艾府：[DFS 48ms](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP31.变换的迷宫

[力扣](https://leetcode.cn/problems/Db3wC1/)

加料版的走迷宫问题，常规做法就是把这些加的料都用状态表示出来，然后看情况选择bfs或者记忆化搜索。

对于本题，最直观的想法就是f[t][x][y][state]表示是否可能在时刻t，处于位置(x, y)，且身上魔法卷轴的使用情况为state。状态表示的前三项是没有什么操作空间的，但是对于魔法卷轴这一项，本题的永久卷轴会永久改变地图，一旦使用之后将会影响后续的状态表示，所以需要想办法将这个地图的改变也表示出来。

直接暴力加上两维，变成f[t][x][y][state][cx][cy]表示是否可能在时刻t，处于位置(x, y)，且身上魔法卷轴的使用情况为state，地图上的(cx, cy)被永久修改。这种状态表示可以顺利执行后续的bfs或者记忆化搜索，但是本身的状态空间太大了，必须想办法优化。

问题主要出在永久卷轴这里，那么不妨思考一下永久卷轴使用之后对于后续操作的意思。实际上，永久卷轴使用之后，提供的作用就是之后还是可能走回到(cx, cy)上。注意到本题并没有什么收集道具的需求，那么一旦在某一时刻走回到(cx, cy)，这个过程中的行动完全可以用一直待在(cx, cy)这个位置上挂机来代替。换言之，使用永久卷轴相当于提供了一种待在(cx, cy)一直挂机的选项，这样一来就没有必要在状态中储存(cx, cy)了，而是在使用永久卷轴的这一回合处理掉后续一直待在(cx, cy)挂机的情况。

那么这里就可以简单使用一个两位的二进制，分别表示临时卷轴和永久卷轴是否使用过。

为了方便处理挂机的情况，在这里就应该使用记忆化搜索。

从f[0][0][0][0]开始进行记忆化搜索，对于当前的f[nowt][nowx][nowy][nows]而言：

1、若(nowx, nowy)是地图的右下角，那么说明走到了目的地，直接返回true

2、否则若nowt \= t，那么说明时间到了但依然没有走到目的地，直接返回false

3、否则开始尝试行动。分别尝试往上、下、左、右以及原地挂机这5个选项。对于下一轮的目的地(x, y)：

3-1）若maze[nowt + 1][x][y]不是陷阱，那么可以直接走过去。于是可以递归求解f[nowt + 1][x][y][nows]，若为true，那么返回true

3-2）否则maze[nowt + 1][x][y]是陷阱，需要选择使用卷轴。

若当前没有使用过临时卷轴，那么就可以尝试使用临时卷轴。此时的nexts \= nows + 1，然后递归求解f[nowt + 1][x][y][nexts]，若为true，那么返回true

若当前没有使用过永久卷轴，那么就可以尝试使用永久卷轴。此时的nexts \= nows + 2，另外还需要从nowt + 1到t - 1枚举所有的挂机时间nextt，然后递归求解f[nextt][x][y][nexts]，若为true，那么返回true

如果尝试完所有的走法都没有true，那么就返回false

记忆化搜索完成后，f[0][0][0][0]就是最终的答案。

最后附上python代码：

```python
class Solution(object):
    def escapeMaze(self, maze):
        """
        :type maze: List[List[str]]
        :rtype: bool
        """

        t = len(maze)
        m = len(maze[0])
        n = len(maze[0][0])
        
        f = [[[[None] * 4 for k in range(n)] for j in range(m)] for i in range(t)]

        dx = [1, 0, -1, 0, 0]
        dy = [0, 1, 0, -1, 0]

        def dfs(nowt, nowx, nowy, nows, f):
            if f[nowt][nowx][nowy][nows] is None:
                if nowx == m - 1 and nowy == n - 1:
                    return True

                f[nowt][nowx][nowy][nows] = False

                if nowt == t - 1:
                    return False
                
                
                for index in range(5):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        if maze[nowt + 1][x][y] == '.':
                            if dfs(nowt + 1, x, y, nows, f):
                                return True
                        else:
                            if nows == 0 or nows == 2:
                                if dfs(nowt + 1, x, y, nows + 1, f):
                                    return True
                
                            if nows < 2:
                                for nextt in range(nowt + 1, t):
                                    if dfs(nextt, x, y, nows + 2, f):
                                        return True
            
            return False
        
        

        return dfs(0, 0, 0, 0, f)
```
