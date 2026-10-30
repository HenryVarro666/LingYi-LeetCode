---
title: "797. 所有可能的路径"
aliases: ["yiduobo的每日leetcode 797.所有可能的路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342396465"
zhihu_id: "342396465"
zhihu_title: "yiduobo的每日leetcode 797.所有可能的路径"
question_id: "797"
question: "所有可能的路径"
problem_url: "https://leetcode.cn/problems/all-paths-from-source-to-target/"
created: "2021-01-06T21:01:49+08:00"
updated: "2021-01-06T21:01:49+08:00"
upvotes: 0
comments: 0
---

# 797. 所有可能的路径

> **[yiduobo的每日leetcode 797.所有可能的路径](https://zhuanlan.zhihu.com/p/342396465) · 知乎 · 2021-01-06 · 赞同 0**
> 力扣：[797. 所有可能的路径](https://leetcode.cn/problems/all-paths-from-source-to-target/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

797.所有可能的路径

[力扣](https://leetcode-cn.com/problems/all-paths-from-source-to-target/)

题目要求给出所有从0到n-1的合法路径，由于这里的n非常小，因此直接dfs也是可行的。我在这里采用的是动态规划的做法，令f[x]表示节点x到n - 1的所有路径，那么我们就是要求f[0]。对于这里的求解顺序，由于给出的图是有向无环图，那么可以先执行一次拓扑排序，确定各个顶点的序，然后根据这个序反向来做动态规划。

拓扑排序的流程是统计各个点的入度，初始先将入度为0的节点加入到队列中。接下来开始执行bfs，对于当前处理的节点，遍历以该节点为起点的所有边，将边终点的节点入度减一。若某个节点的入度减到0，那么将该节点加入到队列中。

例如样例2中：

1、各个节点的入度分别为0、1、1、3、3，因此队列初始化为[0]。

2、开始执行bfs，当前处理到节点0，将节点1、3、4的入度减一，此时的入度分别为0、0、1、2、2，发现节点1的入度被减到了0，因此将1加入到队列中。此时的队列为[0, 1]。

3、接下来处理节点1，将节点2、3、4的入度减一，此时的入度分别为0、0、0、1、1，发现节点2的入度被减到了0，因此将2加入到队列中。此时的队列为[0, 1, 2]。

4、接下来处理节点2，将节点3的入度减一，此时的入度分别为0、0、0、0、1，发现节点3的入度被减到了0，因此将3加入到队列中。此时的队列为[0, 1, 2, 3]。

5、接下来处理节点3，将节点4的入度减一，此时的入度分别为0、0、0、0、0，发现节点4的入度被减到了0，因此将4加入到队列中。此时的队列为[0, 1, 2, 3, 4]。由于节点4已经加入到队列中，那么拓扑排序就可以提前终止了，因此其他未加入队列的节点必然不会出现在0到4的路径上。

此时得到的拓扑排序队列为[0, 1, 2, 3, 4]，那么我们就反过来从右向左开始进行动态规划。初始化f[n - 1]为[n -1]，然后从下一个数开始向前遍历。对于当前处理的节点now，遍历所有以now为起点的的边，设边上的终点为next，那么就可以将以next为起点的所有到n - 1的路径加入到f[now]当中，即

f\[now\].extend(\[\[now\] + path for path in f\[next\]\])

完成动态规划后，最终f[0]就是答案。

最后附上python代码：

```python
class Solution(object):
    def allPathsSourceTarget(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: List[List[int]]
        """

        n = len(graph)
        ind = [0] * n
        g = {}
        for index, next_list in enumerate(graph):
            g[index] = set()
            for next in next_list:
                ind[next] += 1
                g[index].add(next)
        
        if ind[n - 1] == 0:
            return []

        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)

        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
                    if next == n - 1:
                        break
            if ind[n - 1] == 0:
                break

        if ind[n - 1] != 0:
            return []

        f = [[] for _ in range(n)]
        f[n - 1].append([n - 1])
        for index in range(len(q) - 2, -1, -1):
            now = q[index]
            for next in g[now]:
                if ind[next] == 0:
                    f[now].extend([[now] + path for path in f[next]])
                    
        return f[0]
```
