---
title: "1210. 穿过迷宫的最少移动次数"
aliases: ["yiduobo的每日leetcode 1210.穿过迷宫的最少移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/网格图", "题单/网格图/二-网格图-BFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382319774"
zhihu_id: "382319774"
zhihu_title: "yiduobo的每日leetcode 1210.穿过迷宫的最少移动次数"
question_id: "1210"
question: "穿过迷宫的最少移动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-reach-target-with-rotations/"
difficulty: "Hard"
rating: 2022
created: "2021-06-20T13:12:58+08:00"
updated: "2021-06-20T13:12:58+08:00"
upvotes: 0
comments: 0
---

# 1210. 穿过迷宫的最少移动次数

> **[yiduobo的每日leetcode 1210.穿过迷宫的最少移动次数](https://zhuanlan.zhihu.com/p/382319774) · 知乎 · 2021-06-20 · 赞同 0**
> 力扣：[1210. 穿过迷宫的最少移动次数](https://leetcode.cn/problems/minimum-moves-to-reach-target-with-rotations/) · Hard · 灵茶山艾府：[还在 if-else？一个循环处理六种移动！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1210.穿过迷宫的最少移动次数

[力扣](https://leetcode-cn.com/problems/minimum-moves-to-reach-target-with-rotations/)

依然是使用bfs来解决，在这里蛇的状态可以是水平也可以说是竖直，那么我们需要使用三元组(x, y, h_flag)来表示蛇当前的状态，表示蛇的头在(x, y)，而h_flag为真时蛇是水平状态，而h_flag为假时蛇是竖直状态，那么对于当前状态(x, y, h_flag)：

1、当蛇是水平状态时，也就是h_flag为真时：

可以向右前进一步，向下移动一步，或者调转方向，三种情况分别对应

1-1）向右前进，那么此时蛇头的位置会从(x, y)变成(x, y + 1)，但方向h_flag不变

1-2）向下移动，那么此时蛇头的位置会从(x, y)变成(x + 1, y)，但方向h_flag不变

1-3）调转方向，那么此时蛇头的位置会从(x, y)变成(x + 1, y - 1)，同时方向发生了变化，于是此时的方向应该变为not h_flag

2、当蛇是竖直状态时：

可以向下前进一步，向右移动一步，或者调转方向，三种情况分别对应

2-1）向下前进，那么此时蛇头的位置会从(x, y)变成(x + 1, y)，但方向h_flag不变

2-2）向右移动，那么此时蛇头的位置会从(x, y)变成(x, y + 1)，当方向h_flag不变

2-3）调转方向，那么此时蛇头的位置会从(x, y)变成(x - 1, y + 1)，同时方向发生了变化，于是此时的方向应该变为not h_flag

有了蛇头每一轮的变化情况，接下来就只需要按照普通bfs的流程执行即可。需要注意的是bfs时需要对水平和竖直的情况分别进行去重。

最后附上python代码：

```python
class Solution(object):
    def minimumMoves(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid)
        used_v = [[False] * n for _ in range(n)]
        used_h = [[False] * n for _ in range(n)]
        used_h[0][1] = True
        q = [[0, 1, 1]]
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for nowx, nowy, h_flag in q[l : r]:
                l += 1
                if h_flag:
                    if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and not used_h[nowx][nowy + 1]:
                        q.append([nowx, nowy + 1, h_flag])
                        used_h[nowx][nowy + 1] = True
                    if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and grid[nowx + 1][nowy - 1] == 0:
                        if not used_h[nowx + 1][nowy]:
                            q.append([nowx + 1, nowy, h_flag])
                            used_h[nowx + 1][nowy] = True
                        if not used_v[nowx + 1][nowy - 1]:
                            q.append([nowx + 1, nowy - 1, 1 - h_flag])
                            used_v[nowx + 1][nowy - 1] = True
                    if used_h[n - 1][n - 1]:
                        return step
                else:
                    if nowx + 1 < n and grid[nowx + 1][nowy] == 0 and not used_v[nowx + 1][nowy]:
                        q.append([nowx + 1, nowy, h_flag])
                        used_v[nowx + 1][nowy] = True
                    if nowy + 1 < n and grid[nowx][nowy + 1] == 0 and grid[nowx - 1][nowy + 1] == 0:
                        if not used_v[nowx][nowy + 1]:
                            q.append([nowx, nowy + 1, h_flag])
                            used_v[nowx][nowy + 1] = True
                        if not used_h[nowx - 1][nowy + 1]:
                            q.append([nowx - 1, nowy + 1, 1 - h_flag])
                            used_h[nowx - 1][nowy + 1] = True
            
            l, r = r, len(q)
        
        return -1
```
