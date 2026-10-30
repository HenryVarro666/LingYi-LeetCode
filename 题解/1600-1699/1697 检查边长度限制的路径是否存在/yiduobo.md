---
title: "1697. 检查边长度限制的路径是否存在"
aliases: ["yiduobo的每日leetcode 1697.检查边长度限制的路径是否存在"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/447844384"
zhihu_id: "447844384"
zhihu_title: "yiduobo的每日leetcode 1697.检查边长度限制的路径是否存在"
question_id: "1697"
question: "检查边长度限制的路径是否存在"
problem_url: "https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths/"
created: "2021-12-20T23:51:02+08:00"
updated: "2021-12-20T23:51:02+08:00"
upvotes: 0
comments: 0
---

# 1697. 检查边长度限制的路径是否存在

> **[yiduobo的每日leetcode 1697.检查边长度限制的路径是否存在](https://zhuanlan.zhihu.com/p/447844384) · 知乎 · 2021-12-20 · 赞同 0**
> 力扣：[1697. 检查边长度限制的路径是否存在](https://leetcode.cn/problems/checking-existence-of-edge-length-limited-paths/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1697.检查边长度限制的路径是否存在

[力扣](https://leetcode-cn.com/problems/checking-existence-of-edge-length-limited-paths/)

对于给出的每个询问，如果每次都按照询问中的limit选出长度小于limit的边，然后建图后bfs的话时间复杂度高达O((n + m)q)，肯定是不行的。

一个自然的想法是如果询问中的limit是按照大小顺序从小到大排列好的话，那么后一次询问就可以在前一次询问已经建好的图的基础上添加部分边然后求解，这样一来可以大大缩减时间复杂度。

这种做法一般叫做离线算法，与之对应的是在线算法。二者的区别是在线算法在每个询问到达时会立即进行计算并得出答案，而离线算法则是一开始收集好所有的询问，然后将这些询问通过某种方式重新排列后依次求解。换言之，在能使用离线算法的情况下，离线算法一定不会比在线算法慢，因为离线算法的下限就是按照询问给出的顺序原封不动地求解。

回到题目。在这里如果按照询问的limit从小到大进行排序的话，那么相对应的也需要预先将所有的边按照从小到大的顺序进行排序。然后对于当前询问index，将长度在limit[index - 1]到limit[index] - 1之间的所有边加入到图中，并更新节点之间的连通性。在更新连通性这一块，采用并查集是比较合适的做法。

本题虽然是一道hard的题目，但是使用离线算法来求解的话并不复杂。在多数可以运用离线算法的问题上，通常也要将题目中的各种序利用起来，借助序带来的单调性来优化最终的算法。

最后附上python代码：

```python
class Solution(object):
    def distanceLimitedPathsExist(self, n, edgeList, queries):
        """
        :type n: int
        :type edgeList: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        sorted_edge = sorted(edgeList, key=lambda d:d[2])
        m = len(sorted_edge)
        pos = 0
        f = range(n)

        q = len(queries)
        for index in range(q):
            queries[index].append(index)
        res = [False] * q
        
        for x, y, l, q_ind in sorted(queries, key=lambda d:d[2]):
            while pos < m and sorted_edge[pos][2] < l:
                fa_p = self.find(sorted_edge[pos][0], f)
                fa_q = self.find(sorted_edge[pos][1], f)
                if fa_p != fa_q:
                    if fa_p < fa_q:
                        f[fa_p] = fa_q
                    else:
                        f[fa_q] = fa_p

                pos += 1
            
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            res[q_ind] = fa_x == fa_y
        
        return res
    
    def find(self, x, f):
        if f[x] != x:
            f[x] = self.find(f[x], f)
        
        return f[x]
```
