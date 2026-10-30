---
title: "2699. 修改图中的边权"
aliases: ["yiduobo的每日leetcode 2699.修改图中的边权"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650508160"
zhihu_id: "650508160"
zhihu_title: "yiduobo的每日leetcode 2699.修改图中的边权"
question_id: "2699"
question: "修改图中的边权"
problem_url: "https://leetcode.cn/problems/modify-graph-edge-weights/"
difficulty: "Hard"
rating: 2874
created: "2023-08-17T00:38:35+08:00"
updated: "2023-08-17T00:38:35+08:00"
upvotes: 0
comments: 0
---

# 2699. 修改图中的边权

> **[yiduobo的每日leetcode 2699.修改图中的边权](https://zhuanlan.zhihu.com/p/650508160) · 知乎 · 2023-08-17 · 赞同 0**
> 力扣：[2699. 修改图中的边权](https://leetcode.cn/problems/modify-graph-edge-weights/) · Hard · 灵茶山艾府：[详细分析两次 Dijkstra（稠密图下是线性做法）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2699.修改图中的边权

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/modify-graph-edge-weights/)

题目保证了给出的图是连通图，且权重为-1的边的修改上限2 \* 10^9远超target的上限10^7，因此在这里无需考虑可修改的边权重不够大凑不够target的情况，那么在这里就只有两种可能导致无解：

1、即使将所有-1边的权重都变为1，从source到destination的最短路长度依然大于target。

2、即使不适用任何权重为-1的边，从source到destination依然存在一条长度小于target的最短路。

对于第一种情况，将所有-1的边权重设置为1，然后执行一次dijkstra算法就可以判断了。对于第二种情况相同，直接放弃所有权重为-1的边，执行一次dijkstra算法就可以判断了。

排除了上面的特殊情况，接下来考虑如何处理有解的情况。

一个最直观的想法是对于上面情况1中计算出的最短路d，现在有d \< target，那么对于缺少的target - d这个部分，需要找出位于source到destination最短路径上的某条原始权重为-1的边进行加权，使得这条路径的权重之和等于target。

但是这样做会出现一个问题，就是原来图中从source到destination的次短路、第三短路等路径的长度可能都小于target，那么在修改最短路中的某条边之后，原来的某条路径变成了新的最短路，而这条路径的长度可能依然小于target。

换言之，在这里不能随便找一条边就进行加权，必须在加权后计算其对到其他点的最短路的影响，然后动态地对其他的边进行加权，因此在这里需要再执行一次dijkstra算法，在计算过程中执行加权这一操作。

不妨考虑加权的目标边(x, y)，其加权的时机应该选在计算出source到x的最短路之后，因为这里的加权操作会让x到y的距离更大，这也就意味着对其加权不会影响到之前计算出的最短路。对于这条边，其如果不存在与某条source到destination的路径上，那么对这条边随意加权并不会影响最终结果，反之如果其位于某条从source到destination的路径上，那么这条路径就可以拆解为

source -> x -> y -> destination

其中，source到x的部分就是当前计算出的source到x的最短路，这是一个固定值。x到y的距离是我们计划调整的部分，而最后y到destination的最短路则可以认为是在没有对任何边的权重进行调整时，从destination出发到达y的最短路径的长度，这个值可以在计算特殊情况1时的那次dijkstra中，通过从destination出发计算得到。

这样一来，x到y的边的新权重就应该是target - dis[x] - pre_dis[y]，其中dis[x]表示本轮dijkstra算法计算的在边权调整后从source到x的最短路长度，而pre_dis[y]则表示在边权还未调整之前，从destination出发到y的最短路长度，也就等价于从y出发到destination的最短路径长度。

最后这一次dijkstra算法执行完成后，新的边权即为最终答案。

另外可以发现，如果按照最后这种做法，那么特殊情况2中的，从source到destination存在一条不包含权重为-1的边，同时长度小于target的最短路这种情况，就不会受到任何加权操作的影响，也就是说最后这次dijkstra算法计算出的从source到destination的最短路依然是小于target的，那么在这里就没有为了第二种特殊情况额外执行一次dijkstra算法了。

到了这里，就得到了最终确定的算法：

1、首先将所有权重为-1的边都是为权重为1的边，从destination开始执行dijkstra算法，得到从destination出发到其他各个节点的最短距离pre_dis。由于是无向图，因此pre_dis也可以认为是在这种情况下，从各个节点出发到达destination的最短距离。若此时到的source的最短路径长度大于target，那么说明无解，直接返回空数组。

2、接下来从source开始再次执行dijkstra算法，执行过程中对权重为-1的边进行加权。对于边(x, y)的具体加权值为target - dis[x] - pre_dis[y]，也就是target减去本轮dijkstra到达x的最短路长度，再减去上一轮从y出发到destination的最短路长度。

3、执行完成后，若第二轮的dis[destination]依然小于target，说明原始图中存在一条不包含权重为-1且路径长度小于target的路径，此时直接返回空数组，否则将修改后的边权数组返回即可。

最后附上python代码：

```python
class Solution(object):
    def modifiedGraphEdges(self, n, edges, source, destination, target):
        """
        :type n: int
        :type edges: List[List[int]]
        :type source: int
        :type destination: int
        :type target: int
        :rtype: List[List[int]]
        """

        global g
        g = [[None] * n for _ in range(n)]
        for x, y, v in edges:
            g[x][y] = g[y][x] = v

        def dijkstra(start):
            dis = [None] * n
            dis[start] = 0
            vis = [False] * n
            global g

            for _ in range(n):
                mi = None
                for i in range(n):
                    if dis[i] is not None and not vis[i] and (mi is None or dis[mi] > dis[i]):
                        mi = i
                
                if mi is None:
                    break
                
                vis[mi] = True

                for i in range(n):
                    if g[mi][i] is not None:
                        d = abs(g[mi][i])
                        if start == source and g[mi][i] == -1:
                            if dis[mi] + pre_dis[i] + 1 < target:
                                g[mi][i] = g[i][mi] = target - dis[mi] - pre_dis[i]
                            else:
                                g[mi][i] = g[i][mi] = 1

                            d = g[mi][i]

                        if dis[i] is None or dis[i] > dis[mi] + d:
                            dis[i] = dis[mi] + d
            
            return dis
        

        pre_dis = dijkstra(destination)
        if pre_dis[source] > target:
            return []

        dis = dijkstra(source)
        if dis[destination] < target:
            return []
        
        res = []
        for x, y, v in edges:
            if v == -1:
                res.append([x, y, g[x][y]])
            else:
                res.append([x, y, v])

        return res
```
