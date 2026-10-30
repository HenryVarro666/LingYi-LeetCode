---
title: "2846. 边权重均等查询"
aliases: ["yiduobo的每日leetcode 2846.边权重均等查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/十一-根号算法", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660196203"
zhihu_id: "660196203"
zhihu_title: "yiduobo的每日leetcode 2846.边权重均等查询"
question_id: "2846"
question: "边权重均等查询"
problem_url: "https://leetcode.cn/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/"
difficulty: "Hard"
rating: 2508
created: "2023-10-09T03:19:03+08:00"
updated: "2023-10-09T03:19:03+08:00"
upvotes: 1
comments: 0
---

# 2846. 边权重均等查询

> **[yiduobo的每日leetcode 2846.边权重均等查询](https://zhuanlan.zhihu.com/p/660196203) · 知乎 · 2023-10-09 · 赞同 1**
> 力扣：[2846. 边权重均等查询](https://leetcode.cn/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/) · Hard · 灵茶山艾府：[LCA 模板（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2846.边权重均等查询

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/description/)

对于题目中的一组询问(x, y)，实际上就是要找出x和y的lca，然后统计x到lca以及lca到y的路径上出现次数最多的边权，最后使用路径长度减去这个最多的出现次数即为这组查询的答案。

可以发现，其中涉及到了两个部分，第一个为树中两点的最近公共祖先，在这里最适合的做法是tarjan算法的离线求解，不过我在这里偷懒，直接照抄了之前2277题里使用欧拉序和线段树求解lca的做法，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 2277.树中最接近路径的节点](https://zhuanlan.zhihu.com/p/629018444)

除此之外，还需要高效求解x-lca-y这条路径的长度以及路径上每条边出现的次数。路径长度比较好求解，x的深度减去lca的深度就是x到lca的路径长度，同样的，y的深度减去lca的深度就是y到lca的路径长度，二者相加就是这条路径的长度。

受到计算路径长度方法的启发，注意到本题中边权的取值范围只有26种，那么就可以对每个节点使用一个哈希表记录根节点到当前节点路径中每种边权出现的次数，那么x到lca以及y到lca路径上每种边权出现的次数就可以通过x、y以及lca对应的哈希表中边权出现的次数加减得到，其中出现次数最多的即为所求。另外，对于cnt的求解则可以在求解欧拉序的dfs过程中顺带完成。

最后附上python代码：

```python
class Solution(object):
    def minOperationsQueries(self, n, edges, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        g = {}
        for x, y, v in edges:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[y][x] = v
        
        global pos
        pos = -1

        f = [None] * 65536
        depth = [None] * n
        first = [None] * n
        cnt = [{} for _ in range(n)]

        def add(node, left, right, pos, now):
            if left == right:
                f[node] = now
                return
            
            if f[node] is None or depth[f[node]] > depth[now]:
                f[node] = now

            mid = (left + right) >> 1
            if pos <= mid:
                add(node + node + 1, left, mid, pos, now)
            else:
                add(node + node + 2, mid + 1, right, pos, now)

        def dfs(now, fa):
            global pos
            pos += 1

            if depth[now] is None:
                if fa is None:
                    depth[now] = 0
                else:
                    depth[now] = depth[fa] + 1
                
                first[now] = pos
            
            add(0, 0, 32767, pos, now)

            for next in g.get(now, {}):
                if next != fa:
                    cnt[next] = cnt[now].copy()
                    cnt[next][g[now][next]] = cnt[next].get(g[now][next], 0) + 1
                    dfs(next, now)
                    pos += 1
                    add(0, 0, 32767, pos, now)

        def get(node, left, right, start, end):
            if left == start and right == end:
                return f[node]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(node + node + 1, left, mid, start, end)
            elif start > mid:
                return get(node + node + 2, mid + 1, right, start, end)
            else:
                left_res = get(node + node + 1, left, mid, start, mid)
                right_res = get(node + node + 2, mid + 1, right, mid + 1, end)
                if depth[left_res] < depth[right_res]:
                    return left_res
                else:
                    return right_res

        def get_lca(x, y):
            start = first[x]
            end = first[y]
            if start > end:
                start, end = end, start
            
            return get(0, 0, 32767, start, end)

        dfs(0, None)
        res = []
        for x, y in queries:
            if x == y:
                res.append(0)
                continue

            lca = get_lca(x, y)
            path_cnt = {}
            for v in cnt[x]:
                path_cnt[v] = cnt[x][v]
            for v in cnt[y]:
                path_cnt[v] = path_cnt.get(v, 0) + cnt[y][v]
            for v in cnt[lca]:
                path_cnt[v] -= cnt[lca][v] * 2
            res.append(depth[x] + depth[y] - depth[lca] * 2 - max(path_cnt.values()))
        
        return res
```
