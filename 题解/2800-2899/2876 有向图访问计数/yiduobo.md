---
title: "2876. 有向图访问计数"
aliases: ["yiduobo的每日leetcode 2876.有向图访问计数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662762734"
zhihu_id: "662762734"
zhihu_title: "yiduobo的每日leetcode 2876.有向图访问计数"
question_id: "2876"
question: "有向图访问计数"
problem_url: "https://leetcode.cn/problems/count-visited-nodes-in-a-directed-graph/"
difficulty: "Hard"
rating: 2210
created: "2023-10-23T01:10:53+08:00"
updated: "2023-10-23T01:10:53+08:00"
upvotes: 0
comments: 0
---

# 2876. 有向图访问计数

> **[yiduobo的每日leetcode 2876.有向图访问计数](https://zhuanlan.zhihu.com/p/662762734) · 知乎 · 2023-10-23 · 赞同 0**
> 力扣：[2876. 有向图访问计数](https://leetcode.cn/problems/count-visited-nodes-in-a-directed-graph/) · Hard · 灵茶山艾府：[【模板】内向基环树，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2876.有向图访问计数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-visited-nodes-in-a-directed-graph/)

本题与之前的2836题类似，也是给出一张图，图中每个节点只会向外发出一条边，因此最终形成的必然是若干个环，然后从环上的节点向外延伸出树形结构。

[yiduobo：yiduobo的每日leetcode 2836.在传球游戏中最大化函数值](https://zhuanlan.zhihu.com/p/659573926)

本题的做法也可以参考之前这题，先通过遍历将环和树的形态构造出来，然后对于环上的节点，其对应的答案就是环上的长度，而对于树上的节点，其对应的答案则是其走到环上所需的步数再加上环的长度，于是只需从每个环上的每个节点开始，在其对应的树中向下做bfs，计算树中每个节点到当前节点的路径长度，从而得到每个节点对应的答案。

最后附上python代码：

```python
class Solution(object):
    def countVisitedNodes(self, edges):
        """
        :type edges: List[int]
        :rtype: List[int]
        """

        g = {}
        circle_list = []
        n = len(edges)
        vis = set()
        q = []
        
        for i in range(n):
            if i not in vis:
                q.append(i)
                vis.add(i)
                while edges[q[-1]] not in vis:
                    q.append(edges[q[-1]])
                    vis.add(q[-1])
                
                x = edges[q[-1]]
                if x not in g:
                    circle_list.append([])
                    while q[-1] != x:
                        g[q[-1]] = set()
                        circle_list[-1].append(q.pop())
                    
                    circle_list[-1].append(x)
                    g[x] = set()

                while q:
                    g[x].add(q[-1])
                    x = q.pop()
                    g[x] = set()
        
        res = [0] * n
        for circle in circle_list:
            for x in circle:
                q = [x]
                res[x] = len(circle)
                head, tail = 0, 1
                while head < tail:
                    now = q[head]
                    head += 1
                    for nxt in g[now]:
                        res[nxt] = res[now] + 1
                        q.append(nxt)
                        tail += 1
        
        return res
```
