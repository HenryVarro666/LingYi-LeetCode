---
title: "934. 最短的桥"
aliases: ["yiduobo的每日leetcode 934.最短的桥"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357642595"
zhihu_id: "357642595"
zhihu_title: "yiduobo的每日leetcode 934.最短的桥"
question_id: "934"
question: "最短的桥"
problem_url: "https://leetcode.cn/problems/shortest-bridge/"
created: "2021-03-16T22:49:42+08:00"
updated: "2021-03-16T22:49:42+08:00"
upvotes: 3
comments: 3
---

# 934. 最短的桥

> **[yiduobo的每日leetcode 934.最短的桥](https://zhuanlan.zhihu.com/p/357642595) · 知乎 · 2021-03-16 · 赞同 3**
> 力扣：[934. 最短的桥](https://leetcode.cn/problems/shortest-bridge/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

934.最短的桥

[力扣](https://leetcode-cn.com/problems/shortest-bridge/)

由于题目中只有两块陆地，那么我们可以先随便从A中找一个1，然后从这个1开始进行bfs，将这个1以及与之连通的所有1都覆盖成2，那么现在A中就有一片连续的1和一片连续的2了。

之前bfs使用的队列q中恰好就储存了所有值为2的点，那么从这些点开始继续进行bfs，每一轮都往外扩展一步，那么当某一次扩展到值为1的节点时，当前轮次就是答案。

最后附上python代码：

```python
class Solution(object):
    def shortestBridge(self, A):
        """
        :type A: List[List[int]]
        :rtype: int
        """

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        n = len(A)
        q = []
        for i in range(n):
            for j in range(n):
                if A[i][j] == 1:
                    q.append([i, j])
                    A[i][j] = 2
                    break
            if len(q) > 0:
                break

        l = 0
        r = 1
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < n and y >= 0 and y < n and A[x][y] == 1:
                    A[x][y] = 2
                    q.append([x, y])
                    r += 1

        l = 0
        r = len(q)
        step = 0
        while l < r:
            step += 1
            for nowx, nowy in q[l : r]:
                for index in range(4):
                    x = nowx + dx[index]
                    y = nowy + dy[index]
                    if x >= 0 and x < n and y >= 0 and y < n:
                        if A[x][y] == 0:
                            A[x][y] = 2
                            q.append([x, y])
                        elif A[x][y] == 1:
                            return step - 1
            
            l, r = r, len(q)
```
