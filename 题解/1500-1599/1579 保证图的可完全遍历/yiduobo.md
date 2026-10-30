---
title: "1579. 保证图的可完全遍历"
aliases: ["yiduobo的每日leetcode 1579.保证图的可完全遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/430274869"
zhihu_id: "430274869"
zhihu_title: "yiduobo的每日leetcode 1579.保证图的可完全遍历"
question_id: "1579"
question: "保证图的可完全遍历"
problem_url: "https://leetcode.cn/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/"
created: "2021-11-06T21:02:46+08:00"
updated: "2021-11-06T21:02:46+08:00"
upvotes: 0
comments: 0
---

# 1579. 保证图的可完全遍历

> **[yiduobo的每日leetcode 1579.保证图的可完全遍历](https://zhuanlan.zhihu.com/p/430274869) · 知乎 · 2021-11-06 · 赞同 0**
> 力扣：[1579. 保证图的可完全遍历](https://leetcode.cn/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1579.保证图的可完全遍历

[力扣](https://leetcode-cn.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/)

如果单独考虑alice或者bob，为了让n个节点连通，同时使用的边数最少，那么显然应该构造出一棵生成树，即使用n - 1条边来连通n个节点。

对于二者的生成树而言，为了使得最终答案中的边数最少，那么自然是希望这两棵生成树中的公共边越多越好，于是一个自然的想法是先尽可能使用绿色边来连通各个节点。

当然，这些绿色边也可能形成冗余，一个可行的做法是先找出图中的桥，然后对于连通分量中的边选择去除掉部分。另一个思路是反过来思考，先假设图中没有边，然后利用并查集来将边加入到图中，这个方法相比起来实现会简单得多。

使用并查集找出所有可用的绿色边之后，再分别在这个基础上加入红色边和蓝色边，使得各个节点连通起来。当然，无论最终如何连接，答案中的两棵树中的边数必然都是n - 1条，因此这一步只需要检测绿边图在加入红边或者蓝边之后的连通性即可。

这一步可是使用并查集检测，也可以检测删去的冗余边的数目。不妨设使用的绿色边为k条，那么最终使用的红色边或者蓝色边数量必然是n - 1 - k条。若最终使用的红色边或者蓝色边数量不等于n - 1 - k，那么说明图中必然有些点无法连通，此时返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def maxNumEdgesToRemove(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        alice_edge = []
        bob_edge = []
        f = range(n)

        res = 0
        used_common = 0
        for t, x, y in edges:
            x -= 1
            y -= 1
            if t == 1:
                alice_edge.append([x, y])
            elif t == 2:
                bob_edge.append([x, y])
            else:
                fa_x = self.find(x, f)
                fa_y = self.find(y, f)
                if fa_x == fa_y:
                    res += 1
                else:
                    used_common += 1
                    if fa_x < fa_y:
                        f[fa_y] = fa_x
                    else:
                        f[fa_x] = fa_y

        g = f[:]

        alice_del = 0
        for x, y in alice_edge:
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            if fa_x == fa_y:
                alice_del += 1
            elif fa_x < fa_y:
                f[fa_y] = fa_x
            else:
                f[fa_x] = fa_y
        
        if alice_del != len(alice_edge) - (n - 1 - used_common):
            return -1
        
        bob_del = 0
        for x, y in bob_edge:
            fa_x = self.find(x, g)
            fa_y = self.find(y, g)
            if fa_x == fa_y:
                bob_del += 1
            elif fa_x < fa_y:
                g[fa_y] = fa_x
            else:
                g[fa_x] = fa_y
        
        if bob_del != len(bob_edge) - (n - 1 - used_common):
            return -1
        
        return res + alice_del + bob_del

    def find(self, now, fa):
        if fa[now] != now:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
```
