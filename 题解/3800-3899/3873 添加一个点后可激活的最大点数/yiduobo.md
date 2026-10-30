---
title: "3873. 添加一个点后可激活的最大点数"
aliases: ["yiduobo的每日leetcode 3873.添加一个点后可激活的最大点数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/graph", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019123083873629982"
zhihu_id: "2019123083873629982"
zhihu_title: "yiduobo的每日leetcode 3873.添加一个点后可激活的最大点数"
question_id: "3873"
question: "添加一个点后可激活的最大点数"
problem_url: "https://leetcode.cn/problems/maximum-points-activated-with-one-addition/"
difficulty: "Hard"
created: "2026-03-22T19:06:01+08:00"
updated: "2026-03-22T19:06:02+08:00"
upvotes: 1
comments: 0
---

# 3873. 添加一个点后可激活的最大点数

> **[yiduobo的每日leetcode 3873.添加一个点后可激活的最大点数](https://zhuanlan.zhihu.com/p/2019123083873629982) · 知乎 · 2026-03-22 · 赞同 1**
> 力扣：[3873. 添加一个点后可激活的最大点数](https://leetcode.cn/problems/maximum-points-activated-with-one-addition/) · Hard · 灵茶山艾府：[中介并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3873.添加一个点后可激活的最大点数

<https://leetcode.cn/problems/maximum-points-activated-with-one-addition/>

题目给出一个二维整数数组points，其中points\[index\] \= \[x\[index\], y\[index\]\]，表示第index个点的坐标。points中的所有坐标互不相同。

若一个点被激活，那么所有与该点具有相同x坐标或者y坐标的点也会被激活。激活会一直持续，直到没有额外的点可以被激活位置。

现在可以额外添加一个不在points中的整数点(x, y)，从这个点开始激活。

问可以被激活的最大点数，包括这个新添加的点。

如果将points中的点视为图中的点，若两个points的x或者y相同，那么就在图中连上一条边。基于题目描述中激活的规则，同一个连通分量中的点要么不被激活，要么都被激活。为了使得激活的点数最多，只需选择点数最多的两个连通分量，新增一个点将这两个连通分量连接起来就行了，答案就是这两个连通分量的大小加上1。

为了得到具体的连通分量以及对应的大小，在这里可以采用哈希表配合并查集进行处理。具体来说，使用两个哈希表xs和ys，其中xs[x]表示第一个具有x坐标的点的编号，ys[y]则表示第一个具有y坐标的点的编号。

接下来，对于当前遍历到的第index个点(x, y)，若x首次出现，那么就将xs[x]置为index，否则将xs[x]与index通过并查集合并到一起。同样的，若y首次出现，那么就将ys[y]置为index，否则将ys[y]与index通过并查集合并到一起。

在合并过程中，可以额外使用一个数组size记录当前连通分量的大小。

全部处理完成后，遍历所有连通分量，取出其中最大和次大的size，二者之和再加上1即为最终答案。需要注意仅有一个连通分量的情况，此时的答案应该是最大的size加上1。

最后附上python代码：

```python
class Solution(object):
    def maxActivated(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """
        
        n = len(points)
        fa = [index for index in range(n)]
        size = [1] * n
        parts = {}
        xs = {}
        ys = {}

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for index, (x, y) in enumerate(points):
            if x not in xs:
                xs[x] = index
            else:
                fa_s = find(fa, xs[x])
                fa[index] = fa_s
                size[fa_s] += size[index]
            
            if y not in ys:
                ys[y] = index
            else:
                fa_s = find(fa, ys[y])
                fa_index = find(fa, index)
                if fa_s != fa_index:
                    fa[fa_index] = fa_s
                    size[fa_s] += size[fa_index]

        first, second = 0, 0
        for index in range(n):
            if find(fa, index) != index:
                continue
            if size[index] > first:
                first, second = size[index], first
            elif size[index] > second:
                second = size[index]

        return first + second + 1
```
