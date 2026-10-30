---
title: "1245. 树的直径"
aliases: ["yiduobo的每日leetcode 1245.树的直径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614636675"
zhihu_id: "614636675"
zhihu_title: "yiduobo的每日leetcode 1245.树的直径"
question_id: "1245"
question: "树的直径"
problem_url: "https://leetcode.cn/problems/tree-diameter/"
created: "2023-03-16T23:43:30+08:00"
updated: "2023-03-16T23:43:30+08:00"
upvotes: 0
comments: 0
---

# 1245. 树的直径

> **[yiduobo的每日leetcode 1245.树的直径](https://zhuanlan.zhihu.com/p/614636675) · 知乎 · 2023-03-16 · 赞同 0**
> 力扣：[1245. 树的直径](https://leetcode.cn/problems/tree-diameter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1245.树的直径

[力扣](https://leetcode.cn/problems/tree-diameter/)

关于树的直径，最经典的做法就是两次bfs，即从树中任意节点开始bfs走到距离最远的节点，然后从这个最远的节点再进行一次bfs走到最远的节点，这两个节点的距离就是树的直径了。

最后附上python代码：

```python
class Solution(object):
    def treeDiameter(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            g[x].add(y)

            if y not in g:
                g[y] = set()
            g[y].add(x)
        
        q = [0]
        vis = set([0])
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    if next not in vis:
                        q.append(next)
                        vis.add(next)
            
            head, tail = tail, len(q)
        
        now = q[-1]
        q = [now]
        res = 0
        vis = set([now])
        head, tail = 0, 1
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    if next not in vis:
                        q.append(next)
                        vis.add(next)
            
            head, tail = tail, len(q)
        
        return res - 1
```
