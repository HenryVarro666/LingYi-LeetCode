---
title: "3067. 在带权树网络中统计可连接服务器对数目"
aliases: ["yiduobo的每日leetcode 3067.在带权树网络中统计可连接服务器对数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/math", "leetcode/combinatorics", "leetcode/enumeration", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/常用数据结构/零-常用枚举技巧", "题单/链表-二叉树与回溯/三-一般树", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697081154"
zhihu_id: "697081154"
zhihu_title: "yiduobo的每日leetcode 3067.在带权树网络中统计可连接服务器对数目"
question_id: "3067"
question: "在带权树网络中统计可连接服务器对数目"
problem_url: "https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/"
difficulty: "Medium"
rating: 1909
created: "2024-05-11T00:46:23+08:00"
updated: "2024-05-11T00:46:23+08:00"
upvotes: 1
comments: 0
---

# 3067. 在带权树网络中统计可连接服务器对数目

> **[yiduobo的每日leetcode 3067.在带权树网络中统计可连接服务器对数目](https://zhuanlan.zhihu.com/p/697081154) · 知乎 · 2024-05-11 · 赞同 1**
> 力扣：[3067. 在带权树网络中统计可连接服务器对数目](https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/) · Medium · 灵茶山艾府：[枚举根 DFS + 乘法原理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3067.在带权树网络中统计可连接服务器对数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/description/)

题目的数据规模不大，完全可以逐个枚举中间节点c，然后计算对应的count[c]是多少。

对于当前的中间节点c，由于题目要求c到b的路径与c到a的路径不重叠，那么就意味着如果将c视为树的根节点，那么a和b就必须处在不同的子树中。理由是如果二者处于除了c以为的同一子树中，那么从该子树的根节点出发到节点c的这些路径将会出现重复，与题目要求不符。

有了这个结论，就可以先通过dfs计算c的每个孩子为根节点的子树中，与c的距离为signalSpeed的倍数的节点总数，然后利用乘法原理计算不同子树中符合条件的点对的数量。

具体实现上，先逐个枚举中间节点c，对于枚举到的c，使用一个变量tot记录已遍历的子树中与c距离为signalSpeed的倍数的节点数量。

接下来枚举c的所有子节点，从当前子节点开始向下进行dfs，计算子树中与c距离为signalSpeed的倍数的节点数量，记为cnt。为了避免重复计算，此时应该计算cnt与tot形成的点对数量，即将cnt \* tot累加到count[c]中，然后再将cnt累加到tot中并继续考虑下一个子节点即可。

最后附上python代码：

```python
class Solution(object):
    def countPairsOfConnectableServers(self, edges, signalSpeed):
        """
        :type edges: List[List[int]]
        :type signalSpeed: int
        :rtype: List[int]
        """

        g = {}
        for x, y, w in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = w
        

        def dfs(now, fa, dis):
            cnt = 0
            if dis % signalSpeed == 0:
                cnt += 1
            for child in g[now]:
                if child != fa:
                    cnt += dfs(child, now, dis + g[now][child])
            
            return cnt

        n = len(edges) + 1
        res = [0] * n
        for root in range(n):
            tot = 0
            for child in g[root]:
                cnt = dfs(child, root, g[root][child])
                res[root] += tot * cnt
                tot += cnt
        
        return res
```
