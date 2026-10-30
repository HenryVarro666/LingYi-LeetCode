---
title: "3608. 包含k个连通分量需要的最小时间"
aliases: ["yiduobo的每日leetcode 3608.包含k个连通分量需要的最小时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/union-find", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942681960557287307"
zhihu_id: "1942681960557287307"
zhihu_title: "yiduobo的每日leetcode 3608.包含k个连通分量需要的最小时间"
question_id: "3608"
question: "包含 K 个连通分量需要的最小时间"
problem_url: "https://leetcode.cn/problems/minimum-time-for-k-connected-components/"
difficulty: "Medium"
rating: 1893
created: "2025-08-23T20:33:52+08:00"
updated: "2025-08-23T20:33:52+08:00"
upvotes: 0
comments: 0
---

# 3608. 包含k个连通分量需要的最小时间

> **[yiduobo的每日leetcode 3608.包含k个连通分量需要的最小时间](https://zhuanlan.zhihu.com/p/1942681960557287307) · 知乎 · 2025-08-23 · 赞同 0**
> 力扣：[3608. 包含 K 个连通分量需要的最小时间](https://leetcode.cn/problems/minimum-time-for-k-connected-components/) · Medium · 灵茶山艾府：[并查集，从大到小合并（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3608.包含k个连通分量需要的最小时间

[3608. 包含 K 个连通分量需要的最小时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-for-k-connected-components/description/)

题目给出一个整数n，表示一个包含n个节点的无向图，节点从0到n - 1编号。这张图由一个二维数组edges表示，其中edges\[index\] \= \[u\[index\], v\[index\], time\[index\]\]表示一条连接节点u\[index\]和节点v\[index\]的无向边，这条边将在time\[index\]被移除。

另外给出一个整数k。在一开始，图可能是连通的，也可能是非联通的，现在要求找出一个最小的时间t，使得在移除所有time \<\= t的边之后，图中包含至少k个连通分量。

一般来说，拆分连通分量是比较麻烦的，所以对于这类问题，如果可以离线处理，那么就可以离线倒推。假设一开始所有节点都是孤立的，然后将原始图中边删除的顺序反过来，逐条将边加入到图中，在这个过程中利用并查集维护连通性。

对于本题，则可以先将所有边按照time从到大小进行排序，接下来一趟遍历，将这些边逐条加入图中，直到图中的连通块小于k个为止，此时这条边对应的时间戳即为最终答案。若所有边加入进去之后连通块的数量依然大于等于k，或者一开始就没有边，那么答案就为0。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, n, edges, k):
        """
        :type n: int
        :type edges: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        if not edges:
            return 0

        edges.sort(key=lambda d:d[2], reverse=True)
        fa = [x for x in range(n)]
        parts = n

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for x, y, t in edges:
            fa_x = find(fa, x)
            fa_y = find(fa, y)
            if fa_x != fa_y:
                parts -= 1
                if parts < k:
                    return t
                fa[fa_x] = fa_y
        
        return 0
```
