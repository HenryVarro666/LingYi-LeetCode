---
title: "749. 隔离病毒"
aliases: ["yiduobo的每日leetcode 749.隔离病毒"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337967848"
zhihu_id: "337967848"
zhihu_title: "yiduobo的每日leetcode 749.隔离病毒"
question_id: "749"
question: "隔离病毒"
problem_url: "https://leetcode.cn/problems/contain-virus/"
created: "2020-12-18T20:43:58+08:00"
updated: "2020-12-18T20:43:58+08:00"
upvotes: 0
comments: 0
---

# 749. 隔离病毒

> **[yiduobo的每日leetcode 749.隔离病毒](https://zhuanlan.zhihu.com/p/337967848) · 知乎 · 2020-12-18 · 赞同 0**
> 力扣：[749. 隔离病毒](https://leetcode.cn/problems/contain-virus/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

749.隔离病毒

[力扣](https://leetcode-cn.com/problems/contain-virus/)

算法思路不难，但是比较麻烦的题目。

对于每一轮：

1、先执行一趟bfs，找出所有的病毒块以及其之后将感染的区域，并将其保存起来。

2、接下来根据接下来被感染区域的面积选择对应的病毒块，遍历病毒块中的每一个位置，往四个方向进行扩展，若扩展的位置没有在该方向上没有墙，且未被感染，那么就在该位置对应方向上筑墙。

3、最后，将其他接下来将被感染的区域置为1，表示被感染。

对于墙，每个位置最多有4个方向，那么可以使用4位的二进制来表示当前方向上是否有墙。

另外需要注意的是，被墙隔开的病毒要算作两块病毒。

算法上没有什么好说的，看代码和注释会清晰一点。最后附上python代码：

```python
class Solution(object):
    def containVirus(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        walls = [[0] * n for _ in range(m)]
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        rnd = 0
        used = [[0] * n for _ in range(m)]

        while True:
            virius = []
            target = []
            prepare_wall = []
            
            max_target = 0
            max_target_pos = None
            rnd += 1

            for i in range(m):
                for j in range(n):
                    #used[i][j]不等于rnd表示在第rnd轮(i,j)这个位置还未被访问过
                    if used[i][j] != rnd and grid[i][j] == 1:
                        virius.append([])
                        target.append(set())
                        prepare_wall.append([])
                        used[i][j] = rnd
                        q = [[i, j]]
                        l = 0
                        r = 1
                        while l < r:
                            nowx, nowy = q[l]
                            l += 1
                            virius[-1].append([nowx, nowy])
                            for index in range(4):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                #walls[x][y]表示位置(x,y)的筑墙情况。
                                if x >= 0 and x < m and y >= 0 and y < n and (walls[x][y] & (1 << index)) == 0:
                                    #若(x,y)未被感染，则将其加入接下来被感染的target中，同时将如果需要筑的墙加入prepare_wall中
                                    if grid[x][y] == 0:
                                        target[-1].add((x, y))
                                        prepare_wall[-1].append([x, y, 1 << index])
                                    #否则若(x,y)已被感染，且在这一轮没有被访问过，那么将其加入bfs队列中
                                    else:
                                        if used[x][y] != rnd:
                                            q.append([x, y])
                                            r += 1
                                            used[x][y] = rnd

                        #max_target_pos表示这一轮target中面积最大的下标
                        if max_target < len(target[-1]):
                            max_target = len(target[-1])
                            max_target_pos = len(target) - 1
            
            if max_target == 0:
                return res

            #筑墙并累加至答案
            for nowx, nowy, direct in prepare_wall[max_target_pos]:
                walls[nowx][nowy] |= direct
            res += len(prepare_wall[max_target_pos])

            #感染
            for index in range(len(target)):
                if index != max_target_pos:
                    for (nowx, nowy) in target[index]:
                        grid[nowx][nowy] = 1
```
