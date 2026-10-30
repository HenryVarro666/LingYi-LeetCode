---
title: "3607. 电网维护"
aliases: ["yiduobo的每日leetcode 3607.电网维护"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/专题-离线算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942374002132756273"
zhihu_id: "1942374002132756273"
zhihu_title: "yiduobo的每日leetcode 3607.电网维护"
question_id: "3607"
question: "电网维护"
problem_url: "https://leetcode.cn/problems/power-grid-maintenance/"
difficulty: "Medium"
rating: 1700
created: "2025-08-23T00:03:09+08:00"
updated: "2025-08-23T00:03:09+08:00"
upvotes: 0
comments: 0
---

# 3607. 电网维护

> **[yiduobo的每日leetcode 3607.电网维护](https://zhuanlan.zhihu.com/p/1942374002132756273) · 知乎 · 2025-08-23 · 赞同 0**
> 力扣：[3607. 电网维护](https://leetcode.cn/problems/power-grid-maintenance/) · Medium · 灵茶山艾府：[两种方法：懒删除堆 / 倒序处理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3607.电网维护

[3607. 电网维护 - 力扣（LeetCode）](https://leetcode.cn/problems/power-grid-maintenance/description/)

题目给出一个整数c，表示有c个电站，每个电站有一个唯一标识符id，从1到c编号。

这些电站通过n条双向电缆相互连接，表示为一个二维数组connections，其中每个元素connections\[index\] \= \[u\[index\], v\[index\]\]，表示电站u\[index\]与v\[index\]之间的连接。直接或间接连接的电站组成了一个电网。

在一开始，所有电站都是在线状态。

另外给出一个二维数组queries，其中每个查询属于一下两种类型之一：

[1, x]，表示对电站x进行维护检查。如果x在线，那么就返回x，反之则需要返回其所在电网中编号最小的在线电站的id。若这个电网中没有在线的电站，则返回-1。

[2, x]，表示将电站x变为离线。电站的离线不影响电网的结构。

要求返回所有[1, x]的查询结果。

题目实际上给出了一张无向图，而一个电网就是无向图中的一个连通分量，那么在这里可以先对图中的边进行一趟遍历，利用并查集获取每个电网的具体信息。接下来，注意到每次查询中可能需要知道电网中id最小的在线电站编号，那么在这里就可以对于每个电网，都使用一个堆来维护该电网中所有在线的电站，另外还需要一个数组记录每个电站当前是否在线。

接下来对于每次[1, x]查询，若x在线，则直接将x加入到答案数组中，否则先通过并查集定位到x所在的电网，接下来通过其对应的堆来获取电网中最小的在线电站id即可。

需要注意的是，在这里如果使用懒删除的做法来维护这些堆，那么在计算电网中最小在线电站时需要先不断将不在线的堆顶电站从堆中删去，直到堆为空或者堆顶电站在线为止。

最后附上python代码：

```python
class Solution(object):
    def processQueries(self, c, connections, queries):
        """
        :type c: int
        :type connections: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        fa = [x for x in range(c + 1)]
        network = {}

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y in connections:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                fa[fa_x] = fa_y

        for x in range(1, c + 1):
            fa_x = find(fa, x)
            if fa_x not in network:
                network[fa_x] = []
            network[fa_x].append(x)
        
        for fa_x in network:
            heapq.heapify(network[fa_x])
        
        res = []
        online = [True] * (c + 1)
        for q in queries:
            if q[0] == 1:
                if online[q[1]]:
                    res.append(q[1])
                else:
                    fa_q = find(fa, q[1])
                    while network[fa_q] and not online[network[fa_q][0]]:
                        heapq.heappop(network[fa_q])
                    
                    if network[fa_q]:
                        res.append(network[fa_q][0])
                    else:
                        res.append(-1)
            
            else:
                online[q[1]] = False
        
        return res
```
