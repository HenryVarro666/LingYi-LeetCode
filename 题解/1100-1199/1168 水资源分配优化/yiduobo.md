---
title: "1168. 水资源分配优化"
aliases: ["yiduobo的每日leetcode 1168.水资源分配优化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611598276"
zhihu_id: "611598276"
zhihu_title: "yiduobo的每日leetcode 1168.水资源分配优化"
question_id: "1168"
question: "水资源分配优化"
problem_url: "https://leetcode.cn/problems/optimize-water-distribution-in-a-village/"
created: "2023-03-06T04:37:49+08:00"
updated: "2023-03-06T04:37:49+08:00"
upvotes: 0
comments: 0
---

# 1168. 水资源分配优化

> **[yiduobo的每日leetcode 1168.水资源分配优化](https://zhuanlan.zhihu.com/p/611598276) · 知乎 · 2023-03-06 · 赞同 0**
> 力扣：[1168. 水资源分配优化](https://leetcode.cn/problems/optimize-water-distribution-in-a-village/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1168.水资源分配优化

[力扣](https://leetcode.cn/problems/optimize-water-distribution-in-a-village/)

题目给出一些节点和边，要求构造出一棵或多棵树，使得这些生成树中边的权重之和再加上各自生成树中最小的节点值最小。

如果最终只有一棵生成树，这就是经典的最小生成树问题，那么不妨考虑在什么情况下会得到多棵树。对于两棵树t1和t2，若连结二者的最小代价v既大于t1中最小的节点，同时又大于t2中最小的节点，那么就没有理由将两棵树连结起来了。另一方面，从边的大小这个角度出发的最小生成树的算法是kruskal，因此在这里就可以在kruskal算法上进行一些修改来处理本题。

具体来说，初始化答案为所有节点值之和，表示在一开始每棵树都是独立的。接下来将边从小到大进行排序然后一趟遍历，对于当前遍历到的边(x, y, c)，除了检测边连结的两个节点x和y是否属于不同的连通块之外，还需要检测这两个节点当前所属连通块中节点值的最小值是否有大于等于c的。若都满足，那么就将这两个连通块合并，同时将这条边的权重累加到答案中并将这两个连通块中最小值较大的一方从答案中移除。

最后附上python代码：

```python
class Solution(object):
    def minCostToSupplyWater(self, n, wells, pipes):
        """
        :type n: int
        :type wells: List[int]
        :type pipes: List[List[int]]
        :rtype: int
        """

        fa = range(n)
        res = sum(wells)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y, c in sorted(pipes, key=lambda d:d[2]):
            x -= 1
            y -= 1

            fa_x = find(x)
            fa_y = find(y)

            if fa_x != fa_y and (wells[fa_x] >= c or wells[fa_y] >= c):
                res += c
                if wells[fa_x] < wells[fa_y]:
                    fa[fa_y] = fa_x
                    res -= wells[fa_y]
                else:
                    fa[fa_x] = fa_y
                    res -= wells[fa_x]

        return res
```
