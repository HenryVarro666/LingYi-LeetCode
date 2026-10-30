---
title: "3249. 统计好节点的数目"
aliases: ["yiduobo的每日leetcode 3249.统计好节点的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721494671"
zhihu_id: "721494671"
zhihu_title: "yiduobo的每日leetcode 3249.统计好节点的数目"
question_id: "3249"
question: "统计好节点的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-good-nodes/"
difficulty: "Medium"
rating: 1566
created: "2024-09-23T00:41:05+08:00"
updated: "2024-09-23T00:41:05+08:00"
upvotes: 1
comments: 0
---

# 3249. 统计好节点的数目

> **[yiduobo的每日leetcode 3249.统计好节点的数目](https://zhuanlan.zhihu.com/p/721494671) · 知乎 · 2024-09-23 · 赞同 1**
> 力扣：[3249. 统计好节点的数目](https://leetcode.cn/problems/count-the-number-of-good-nodes/) · Medium · 灵茶山艾府：[DFS 计算子树大小，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3249.统计好结点的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-good-nodes/description/)

题目给出一颗具有n个节点的树，其中节点的编号为0到n - 1，树的根节点为0号节点。接下来对于树中的某个节点，若以该节点的所有子节点为根的子树中的节点数量都一样，那么该节点就是一个好节点。问树中一共有多少个好节点。

从根节点向下递归求解，对于当前求解的节点now，先递归求解其所有的孩子节点是否为好节点，在这个过程可以同步计算以每个孩子节点为根节点的子树中有多少个节点。接下来通过以每个孩子节点为根节点的子树中的节点数目是否相同来确定now是否为好节点，同时将这些节点数目累加起来，再加1后即为以now为根节点的子树中节点的数目，返回给上一层节点使用即可。

最后附上python代码：

```python
class Solution(object):
    def countGoodNodes(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        global res
        res = 0

        def dfs(now, fa):
            target = None
            same = True
            tot = 0

            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                cnt = dfs(nxt, now)
                if target is None:
                    target = cnt
                elif target != cnt:
                    same = False
                tot += cnt
            
            if same:
                global res
                res += 1
            
            return tot + 1
        
        dfs(0, -1)
        return res
```
