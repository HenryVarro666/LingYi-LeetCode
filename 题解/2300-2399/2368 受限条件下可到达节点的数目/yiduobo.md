---
title: "2368. 受限条件下可到达节点的数目"
aliases: ["yiduobo的每日leetcode 2368.受限条件下可到达节点的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/array", "leetcode/hash-table", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563198488"
zhihu_id: "563198488"
zhihu_title: "yiduobo的每日leetcode 2368.受限条件下可到达节点的数目"
question_id: "2368"
question: "受限条件下可到达节点的数目"
problem_url: "https://leetcode.cn/problems/reachable-nodes-with-restrictions/"
difficulty: "Medium"
rating: 1477
created: "2022-09-10T16:44:46+08:00"
updated: "2022-09-10T16:44:46+08:00"
upvotes: 0
comments: 0
---

# 2368. 受限条件下可到达节点的数目

> **[yiduobo的每日leetcode 2368.受限条件下可到达节点的数目](https://zhuanlan.zhihu.com/p/563198488) · 知乎 · 2022-09-10 · 赞同 0**
> 力扣：[2368. 受限条件下可到达节点的数目](https://leetcode.cn/problems/reachable-nodes-with-restrictions/) · Medium · 灵茶山艾府：[树上 DFS（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2368.受限条件下可到达节点的数目

[力扣](https://leetcode.cn/problems/reachable-nodes-with-restrictions/)

直接从0号节点开始进行bfs，在过程中既不要访问受限节点，也不要将其加入到bfs队列中。bfs完成后，队列的长度就是可到节点的数目。

最后附上python代码：

```python
class Solution(object):
    def reachableNodes(self, n, edges, restricted):
        """
        :type n: int
        :type edges: List[List[int]]
        :type restricted: List[int]
        :rtype: int
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            
            g[x].add(y)
            g[y].add(x)
        
        q = [0]
        l = 0
        r = 1
        used = set(restricted)
        used.add(0)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in used:
                    used.add(next)
                    q.append(next)
                    r += 1
        
        return len(q)
```
