---
title: "1632. 矩阵转换后的秩"
aliases: ["yiduobo的每日leetcode 1632.矩阵转换后的秩"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438278670"
zhihu_id: "438278670"
zhihu_title: "yiduobo的每日leetcode 1632.矩阵转换后的秩"
question_id: "1632"
question: "矩阵转换后的秩"
problem_url: "https://leetcode.cn/problems/rank-transform-of-a-matrix/"
created: "2021-11-27T00:23:11+08:00"
updated: "2021-11-27T00:23:36+08:00"
upvotes: 0
comments: 0
---

# 1632. 矩阵转换后的秩

> **[yiduobo的每日leetcode 1632.矩阵转换后的秩](https://zhuanlan.zhihu.com/p/438278670) · 知乎 · 2021-11-27 · 赞同 0**
> 力扣：[1632. 矩阵转换后的秩](https://leetcode.cn/problems/rank-transform-of-a-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1632.矩阵转换后的秩

[力扣](https://leetcode-cn.com/problems/rank-transform-of-a-matrix/)

首先，如果完全抛开等于的情况，那么对于矩阵中任意位置上的数x而言，都必须先计算出其所在行和列上所有小于x的位置的秩，然后取其中的最大值加一即为x所在位置的秩。

当然，这里对于x而言只需要关心比x稍微小一点的数所在位置的秩，不妨设x在其所在行是第k_row小的，在其所在的列时第k_column小的，那么对于x而言，只需要关心其所在行第k_row - 1小的数所在位置的秩，以及其所在列第k_column - 1小的数坐在位置的秩，然后取二者中较大的那一个加一即为x所在位置的秩。也就是说，如果在大小相邻的位置之间连上一条有向边的话，问题就转化成了拓扑排序的问题。这里点的规模为m \* n，而如果仅考虑稍微小一点的数的话，每个点只会有两个前驱节点，因此边的规模也是m \* n级别的。

当然，上面是完全不考虑相等的情况时的做法，而一旦出现相等的数，情况就复杂很多了。由于题目要求同行同列中相等数的秩必须一样，那么对于一个x而言，除了考虑其自身之外，还需要考虑其同行同列其他x。这样一来，某个x的前驱节点就必须想所有的x发出一条有向边，那么此时边的规模就很大了，肯定是不行的。一个自然的想法就是将所有行列相连的x缩成一个节点，在这里可以使用bfs或者并查集来做。我在这里采用的是并查集，相对直观一点。

缩完点之后，由于每个x最多只会有两个原生的前驱节点，那么这个缩完后的点的前驱节点数目最多只有x的数目乘以2，因此最终边的规模依然是m \* n级别的，此时再执行拓扑排序就没有问题了。

根据上面的结论就能整理出一种做法：

1、首先将矩阵中的数按行和列分别收集起来，并进行排序

2、枚举每一行，对同一行中值相等的点利用并查集进行合并

3、枚举每一列，对同一列中值相等的点利用并查集进行合并

4、枚举每一行，对同一行大小顺序相邻的两个节点x和y，设x \< y，那么就将x在并查集中的父亲fa_x发射一条边只想到y在并查集中的父亲fa_y，并将fa_y的入度加上1

5、枚举每一列，对同一列大小顺序相邻的两个节点x和y，设x \< y，那么同样是将x在并查集中的父亲fa_x发射一条边只想到y在并查集中的父亲fa_y，并将fa_y的入度加上1

6、至此建图完毕，接下来执行拓扑排序。枚举矩阵中的所有位置，将入度为0，且在并查集中的父亲就是其本身的所有节点加入到队列中，然后开始执行拓扑排序，记录下遍历到每个节点的轮次

7、最后枚举矩阵中的所有点，当前点在并查集中的父亲的拓扑序就是当前位置的秩

由于矩阵是二维的，那么为了方便起见，可以将矩阵中的点按从上到下从左到右的顺序进行编号，即第i行第j列这个位置的编号为i \* n + j，然后使用这个编号来进行并查集以及拓扑排序相关的操作。

最后附上python代码，其中一共有6处二重循环，分别对应了上面操作中除拓扑排序外的其他6步：

```python
class Solution(object):
    def matrixRankTransform(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(matrix)
        n = len(matrix[0])
        fa = range(m * n)
        size = [1] * (m * n)
        row = [[] for _ in range(m)]
        column = [[] for _ in range(n)]
        for i in range(m):
            for j in range(n):
                row[i].append((matrix[i][j], i * n + j))
                column[j].append((matrix[i][j], i * n + j))
        
        for i in range(m):
            row[i].sort()
            for j in range(1, n):
                if row[i][j][0] == row[i][j - 1][0]:
                    fa_l = self.find(row[i][j - 1][1], fa)
                    fa_r = self.find(row[i][j][1], fa)
                    if fa_l != fa_r:
                        if size[fa_l] < size[fa_r]:
                            fa[fa_l] = fa_r
                            size[fa_r] += size[fa_l]
                        else:
                            fa[fa_r] = fa_l
                            size[fa_l] += size[fa_r]
        
        for j in range(n):
            column[j].sort()
            for i in range(1, m):
                if column[j][i][0] == column[j][i - 1][0]:
                    fa_l = self.find(column[j][i - 1][1], fa)
                    fa_r = self.find(column[j][i][1], fa)
                    if fa_l != fa_r:
                        if size[fa_l] < size[fa_r]:
                            fa[fa_l] = fa_r
                            size[fa_r] += size[fa_l]
                        else:
                            fa[fa_r] = fa_l
                            size[fa_l] += size[fa_r]
        
        ind = [0] * (m * n)
        next = [set() for _ in range(m * n)]

        for i in range(m):
            for j in range(1, n):
                if row[i][j][0] > row[i][j - 1][0]:
                    fa_l = self.find(row[i][j - 1][1], fa)
                    fa_r = self.find(row[i][j][1], fa)
                    if fa_r not in next[fa_l]:
                        next[fa_l].add(fa_r)
                        ind[fa_r] += 1
        
        for j in range(n):
            for i in range(1, m):
                if column[j][i][0] > column[j][i - 1][0]:
                    fa_l = self.find(column[j][i - 1][1], fa)
                    fa_r = self.find(column[j][i][1], fa)
                    if fa_r not in next[fa_l]:
                        next[fa_l].add(fa_r)
                        ind[fa_r] += 1
    
        q = []
        l = r = 0
        for num in range(m * n):
            if self.find(num, fa) == num and ind[num] == 0:
                q.append(num)
                r += 1
        
        step = 0
        order = [None] * (m * n)
        while l < r:
            new_r = r
            step += 1
            for num in q[l : r]:
                order[num] = step
                for next_num in next[num]:
                    ind[next_num] -= 1
                    if ind[next_num] == 0:
                        q.append(next_num)
                        new_r += 1

            l, r = r, new_r
        
        res = [[None] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = order[self.find(i * n + j, fa)]
        
        return res

    def find(self, now, fa):
        if now != fa[now]:
            fa[now] = self.find(fa[now], fa)
        return fa[now]
```
