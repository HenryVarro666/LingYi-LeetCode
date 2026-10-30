---
title: "2359. 找到离给定两个节点最近的节点"
aliases: ["yiduobo的每日leetcode 2359.找到离给定两个节点最近的节点"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/enumeration", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/562369611"
zhihu_id: "562369611"
zhihu_title: "yiduobo的每日leetcode 2359.找到离给定两个节点最近的节点"
question_id: "2359"
question: "找到离给定两个节点最近的节点"
problem_url: "https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/"
difficulty: "Medium"
rating: 1715
created: "2022-09-08T01:27:22+08:00"
updated: "2022-09-08T01:27:22+08:00"
upvotes: 0
comments: 0
---

# 2359. 找到离给定两个节点最近的节点

> **[yiduobo的每日leetcode 2359.找到离给定两个节点最近的节点](https://zhuanlan.zhihu.com/p/562369611) · 知乎 · 2022-09-08 · 赞同 0**
> 力扣：[2359. 找到离给定两个节点最近的节点](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/) · Medium · 灵茶山艾府：[两种方法：最短路 / 我吹过你吹过的晚风（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2359.找到离给定两个节点最近的节点

[力扣](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/)

由于每个节点只有一条出边，那么可以先从node1出发一直往下走，直到无法继续往下走，或者走回原来走到过的节点为止。由于每个节点最多只会访问一次，因此这里的时间复杂度为O(n)。

同样地，接下来清除掉访问记录，然后从node2出发一直往下走，直到无法继续往下走或者走回原来走到过的节点为止。

对于上面两次行走，可以使用两个哈希表dis1和dis2分别记录从node1和node2出发走到某个节点需要的步数，接下来遍历dis1中的所有节点node，若node在dis2中也出现了，也就意味着从node1和node2出发都可以到达node，而距离的较大值就是dis1[node]和dis2[node]中的较大值。使用这个值与当前的最小值进行比较并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def closestMeetingNode(self, edges, node1, node2):
        """
        :type edges: List[int]
        :type node1: int
        :type node2: int
        :rtype: int
        """

        dis1 = {node1: 0}
        used = set([-1, node1])
        now = node1
        step = 0
        while edges[now] not in used:
            now = edges[now]
            step += 1
            dis1[now] = step
            used.add(now)
        
        dis2 = {node2: 0}
        used = set([-1, node2])
        now = node2
        step = 0
        while edges[now] not in used:
            now = edges[now]
            step += 1
            dis2[now] = step
            used.add(now)
        
        res = -1
        min_dis = None
        for node in dis1:
            if node in dis2:
                d = max(dis1[node], dis2[node])
                if min_dis is None or min_dis > d:
                    min_dis = d
                    res = node
        
        return res
```
