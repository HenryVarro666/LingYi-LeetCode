---
title: "675. 为高尔夫比赛砍树"
aliases: ["yiduobo的每日leetcode 675.为高尔夫比赛砍树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/298443161"
zhihu_id: "298443161"
zhihu_title: "yiduobo的每日leetcode 675.为高尔夫比赛砍树"
question_id: "675"
question: "为高尔夫比赛砍树"
problem_url: "https://leetcode.cn/problems/cut-off-trees-for-golf-event/"
created: "2020-11-17T22:27:32+08:00"
updated: "2020-11-17T22:27:32+08:00"
upvotes: 0
comments: 0
---

# 675. 为高尔夫比赛砍树

> **[yiduobo的每日leetcode 675.为高尔夫比赛砍树](https://zhuanlan.zhihu.com/p/298443161) · 知乎 · 2020-11-17 · 赞同 0**
> 力扣：[675. 为高尔夫比赛砍树](https://leetcode.cn/problems/cut-off-trees-for-golf-event/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

675.为高尔夫比赛砍树

[力扣](https://leetcode-cn.com/problems/cut-off-trees-for-golf-event/)

直接按题目要求，按树的高度排序，每一轮做一次bfs是比较直观的做法。这里的图是二分图，每次bfs路径上的点到其他点的最短路径长度也可以记录下来，但是始终还是没有想出如何利用上面的这两个性质来做优化。

最后实现的是最普通的多轮bfs的做法，附上python代码，其中q是bfs使用的队列，used则表示这个点在当前这一轮bfs中是否被使用过：

```python
class Solution(object):
    def cutOffTree(self, forest):
        """
        :type forest: List[List[int]]
        :rtype: int
        """

        m = len(forest)
        n = len(forest[0])

        pos_list = []
        for i in range(m):
            for j in range(n):
                if forest[i][j] > 1:
                    pos_list.append([i, j, forest[i][j]])
        
        start_x, start_y = 0, 0
        used = [[0] * n for _ in range(m)]
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = 0
        for rnd, [next_x, next_y, height] in enumerate(sorted(pos_list, key=lambda d:d[2])):
            q = [[start_x, start_y]]
            used[start_x][start_y] = rnd + 1
            l = 0
            r = 1
            step = 0
            while l < r:
                step += 1
                for index in range(l, r):
                    nowx, nowy = q[index]
                    for direct in range(4):
                        x = nowx + dx[direct]
                        y = nowy + dy[direct]
                        if x >= 0 and x < m and y >= 0 and y < n and forest[x][y] > 0 and used[x][y] < rnd + 1:
                            used[x][y] = rnd + 1
                            if x == next_x and y == next_y:
                                res += step
                                break
                            q.append([x, y])

                    if used[next_x][next_y] == rnd + 1:
                        break

                if used[next_x][next_y] == rnd + 1:
                    break

                l, r = r, len(q)
            
            if used[next_x][next_y] != rnd + 1:
                return -1

            start_x, start_y = next_x, next_y

        return res
```
