---
title: "3593. 使叶子路径成本相等的最小增量"
aliases: ["yiduobo的每日leetcode 3593.使叶子路径成本相等的最小增量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940202545659225637"
zhihu_id: "1940202545659225637"
zhihu_title: "yiduobo的每日leetcode 3593.使叶子路径成本相等的最小增量"
question_id: "3593"
question: "使叶子路径成本相等的最小增量"
problem_url: "https://leetcode.cn/problems/minimum-increments-to-equalize-leaf-paths/"
difficulty: "Medium"
rating: 1959
created: "2025-08-17T00:18:37+08:00"
updated: "2025-08-17T00:18:37+08:00"
upvotes: 1
comments: 0
---

# 3593. 使叶子路径成本相等的最小增量

> **[yiduobo的每日leetcode 3593.使叶子路径成本相等的最小增量](https://zhuanlan.zhihu.com/p/1940202545659225637) · 知乎 · 2025-08-17 · 赞同 1**
> 力扣：[3593. 使叶子路径成本相等的最小增量](https://leetcode.cn/problems/minimum-increments-to-equalize-leaf-paths/) · Medium · 灵茶山艾府：[统计最大路径和的出现次数，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3593.使叶子路径成本相等的最小增量

[3593. 使叶子路径成本相等的最小增量 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-increments-to-equalize-leaf-paths/)

题目给出一个整数n，以及一颗无向树，树中包含n个节点，编号为0到n - 1，其中0号节点为根节点。树中每个节点index都有一个成本cost[index]，表示经过该节点的成本，定义路径得分为树中某条路径上所有节点的成本之和。现在要求为树中部分节点增加成本，使得所有从根节点到叶子节点的路径得分相等。

从题目给出的样例3可以发现，对于一颗子树，如果从子树根节点到其中所有叶子节点的路径得分都相同，那么接下来就可以直接修改根节点，而不需要修改单个叶子节点。更进一步的，这种情况下就可以视为将这些叶子折叠进了这个根节点。

基于这个结论，就可以从根节点向下一趟dfs，对于当前遍历到的节点now，先遍历其所有孩子节点nxt，递归求解将以nxt为根节点的子树中所有叶子节点折叠到nxt时，nxt的路径得分v。对于所有的v，找出其中的最大值ma以及ma出现的次数cnt。接下来，需要将所有小于ma的值修改成ma，修改的次数为孩子节点的总数减去cnt，将其累加到答案中。到了这一步，就形成了样例3中节点1这种形态，此时可以将以now为根节点的子树中的叶子节点都折叠到now了，而now的路径得分就应该是ma + cost[now]，返回这个值供上层节点使用即可。

最后附上python代码：

```python
class Solution(object):
    def minIncrease(self, n, edges, cost):
        """
        :type n: int
        :type edges: List[List[int]]
        :type cost: List[int]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        global res
        res = 0

        def dfs(now, fa):
            ma = 0
            cnt = 0
            tot = 0
            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                v = dfs(nxt, now)
                tot += 1

                if v > ma:
                    ma = v
                    cnt = 0
                if v == ma:
                    cnt += 1
            
            global res
            res += tot - cnt
            return ma + cost[now]
        
        dfs(0, -1)
        return res
```
