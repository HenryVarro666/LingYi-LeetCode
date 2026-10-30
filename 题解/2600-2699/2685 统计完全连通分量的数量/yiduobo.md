---
title: "2685. 统计完全连通分量的数量"
aliases: ["yiduobo的每日leetcode 2685.统计完全连通分量的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650007665"
zhihu_id: "650007665"
zhihu_title: "yiduobo的每日leetcode 2685.统计完全连通分量的数量"
question_id: "2685"
question: "统计完全连通分量的数量"
problem_url: "https://leetcode.cn/problems/count-the-number-of-complete-components/"
difficulty: "Medium"
rating: 1769
created: "2023-08-14T20:49:56+08:00"
updated: "2023-08-14T20:49:56+08:00"
upvotes: 0
comments: 0
---

# 2685. 统计完全连通分量的数量

> **[yiduobo的每日leetcode 2685.统计完全连通分量的数量](https://zhuanlan.zhihu.com/p/650007665) · 知乎 · 2023-08-14 · 赞同 0**
> 力扣：[2685. 统计完全连通分量的数量](https://leetcode.cn/problems/count-the-number-of-complete-components/) · Medium · 灵茶山艾府：[DFS 求每个连通块的点数和边数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2685.统计完全连通分量的数量

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-the-number-of-complete-components/description/)

首先进行一趟bfs，找出图中所有的连通分量。接下来对于单个连通分量，遍历其中的所有节点，通过当前连通分量的大小以及该节点的度，就能判断这个节点是否与连通分量中的其他点都相连。若连通分量中的所有节点都与连通分量中的其他节点相连，那么这就是一个完全连通分量。

最后附上python代码：

```python
class Solution(object):
    def countCompleteComponents(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        res = 0
        vis = set()
        for index in range(n):
            if index not in vis:
                q = [index]
                vis.add(index)
                head, tail = 0, 1
                while head < tail:
                    now = q[head]
                    head += 1
                    for nxt in g[now]:
                        if nxt not in vis:
                            vis.add(nxt)
                            q.append(nxt)
                            tail += 1

                flag = True
                for x in q:
                    if len(g[x]) != len(q) - 1:
                        flag = False
                        break
                
                if flag:
                    res += 1
        
        return res
```
