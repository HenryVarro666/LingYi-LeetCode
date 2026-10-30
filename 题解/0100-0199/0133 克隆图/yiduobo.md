---
title: "133. 克隆图"
aliases: ["yiduobo的每日leetcode 133.克隆图"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141469770"
zhihu_id: "141469770"
zhihu_title: "yiduobo的每日leetcode 133.克隆图"
question_id: "133"
question: "克隆图"
problem_url: "https://leetcode.cn/problems/clone-graph/"
created: "2020-05-16T22:43:23+08:00"
updated: "2020-05-16T22:43:23+08:00"
upvotes: 0
comments: 0
---

# 133. 克隆图

> **[yiduobo的每日leetcode 133.克隆图](https://zhuanlan.zhihu.com/p/141469770) · 知乎 · 2020-05-16 · 赞同 0**
> 力扣：[133. 克隆图](https://leetcode.cn/problems/clone-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

133.克隆图<https://leetcode-cn.com/problems/clone-graph/>

搞了半天才弄清楚题目的意思，简单来说就是需要构造出一张新图，结构需要跟原图一模一样。

注意到题目保证了每个节点的值跟索引相同，因此可以通过节点的值作为key，使用dict来储存新图中的节点。

于是可以从原图给的node开始进行bfs。不妨设当前bfs的节点为now，那么枚举原图中now的neighbor：

首先，若neighbor.val没有在dict中，说明未遍历到neighbor，新图中还没有neighbor对应的节点，于是可以将neighbor加入bfs的队列中，同时构造新图中对应的节点，并在dict中以neighbor.val为key储存新图中的节点。

接下来，将新图中neighbor对应的节点加入到新图中now对应节点的邻居列表中，具体来说就是：

dict[now.val]表示now在新图中对应的节点

dict[now.val].neighbor就是邻居列表

dict[neighbor.val]则是neighbor在新图中对应的节点

于是就有dict[now.val].neighbor.append(dict[neighbor.val])

bfs完成后返回node在新图中的对应节点dict[node.val]即可。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val = 0, neighbors = []):
        self.val = val
        self.neighbors = neighbors
"""

class Solution(object):
    def cloneGraph(self, node):
        """
        :type node: Node
        :rtype: Node
        """

        if not node:
            return node

        g = {}
        g[node.val] = Node(node.val, [])
        q = [node]
        l = 0
        r = 1
        while l < r:
            now = q[l]
            l += 1
            for neighbor in now.neighbors:
                if neighbor.val not in g:
                    g[neighbor.val] = Node(neighbor.val, [])
                    q.append(neighbor)
                    r += 1
                g[now.val].neighbors.append(g[neighbor.val])

        return g[node.val]
```
