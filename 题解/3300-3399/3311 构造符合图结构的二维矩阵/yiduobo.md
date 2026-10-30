---
title: "3311. 构造符合图结构的二维矩阵"
aliases: ["yiduobo的每日leetcode 3311.构造符合图结构的二维矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "题单/贪心算法", "题单/贪心算法/五-思维题", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1490523325"
zhihu_id: "1490523325"
zhihu_title: "yiduobo的每日leetcode 3311.构造符合图结构的二维矩阵"
question_id: "3311"
question: "构造符合图结构的二维矩阵"
problem_url: "https://leetcode.cn/problems/construct-2d-grid-matching-graph-layout/"
difficulty: "Hard"
rating: 2664
created: "2024-10-17T02:17:25+08:00"
updated: "2024-10-17T02:17:25+08:00"
upvotes: 1
comments: 0
---

# 3311. 构造符合图结构的二维矩阵

> **[yiduobo的每日leetcode 3311.构造符合图结构的二维矩阵](https://zhuanlan.zhihu.com/p/1490523325) · 知乎 · 2024-10-17 · 赞同 1**
> 力扣：[3311. 构造符合图结构的二维矩阵](https://leetcode.cn/problems/construct-2d-grid-matching-graph-layout/) · Hard · 灵茶山艾府：[拼图：分类讨论/不分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3311.构造符合图结构的二维矩阵

[. - 力扣（LeetCode）](https://leetcode.cn/problems/construct-2d-grid-matching-graph-layout/description/)

题目给出一个二维整数数组edges，表示一张有n个节点的无向图，其中edges\[i\] \= \[u\[i\], v\[i\]\]，表示在节点u\[i\]到v\[i\]之间有一条边。

现在要求构造一个二维矩阵，包含图中的0到n - 1这n个节点，同时矩阵中所有在水平或者竖直方向上相邻的单元格对应的节点需要在图中有边相连。如果有多种答案，返回任意一个即可。

题目的数据规模比较大，必须使用O(n)或者O(nlogn)的算法，不妨从矩阵上各个位置的差异出发进行分析。

对于一个矩阵而言，其四个角上的单元格只与两个单元格相邻，在四条边上且不在四个角上的单元格，则与三个单元格相邻，其他所有单元格均与四个单元格相邻。换言之，这些单元格对应的节点的度数分别为2、3、4。需要特别注意的是，题目并没有保证矩阵的行数和列数存在下限，因此在这里还需要先考虑特殊情况。由于题目只需给出一种可行的构造，那么在这里先认为在特殊情况下矩阵的行数小于等于列数，这样就只需要基于行数进行讨论：

1、如果矩阵只有一行：

这种情况下，矩阵只有两个角，角上的节点的度数为1，而其他所有节点度数均为2

2、如果矩阵只有两行：

这种情况下，矩阵的四个角上节点的度数为2，其他不处于角上的节点度数则均为3

3、如果矩阵行数大于等于3：

这种情况下如最开始讨论的，矩阵的四个角上节点的度数为2，处于边上但不处于角上的节点度数为3，其他节点度数为4

可以发现，在这里就可以通过节点度数中的最大值和最小值来判断是否属于特殊情况。具体来说：

1、若图中节点的度数最小值为1，说明属于情况1：

对于这种情况，只需先找出任意一个度为1的节点，填充在矩阵的最左侧，接下来从这个节点开始，将其在图中相邻且没有被用过的节点填充在当前节点右侧，不断重复此过程直到填充全部n个节点为止。

2、若途中节点度数的最大值为3，说明属于情况2：

对于这种情况，可以先找到任意一个度为2的节点，填充在矩阵的左上角。接下来对于与这个节点相邻的两个节点，将其中度为2的节点填充在矩阵的左下角，将另一个节点填充在其右侧。需要注意这里可能出现2 \* 2矩阵的情况，因此另一个节点的度可以是2也可以是3，但是不影响最终的填充方法。

到目前为止，就填充了上面这一行的前两个节点以及下面这一行的最左侧节点，接下来从第二列，也就是下标为1的这一列开始向右进行遍历。

对于当前列，不妨设上方行被填充的节点为x，那么在这里就可以枚举x在图中相邻的节点y：

2-1）若y已经被填充在x的左侧，则直接跳过

2-2）若y恰好也是下面这一行左侧这一列已填充节点的相邻节点，那么就将y填充在当前列的下面这一行

2-3）若以上两种情况都不满足，则将其填充在x的右侧

这样一来，就相当于每一轮都填充了当前列下面行的节点，以及下一列上面行的节点。

重复填充到最后一列，此时还剩下矩阵右下角这个位置没有填充，此时只需枚举右上角节点在途中的相邻节点，将没有被用过的那一个填充在矩阵右下角即可。

3、若不满足以上两种情况，说明属于情况3，也就是最常规的情况：

首先依然是找出任意一个度为2的节点，填充在矩阵的左上角。接下来从这个节点开始向右遍历，每次将与当前节点相邻，且没有被使用过，同时度不为4的节点填充在当前节点的右侧，直到填充了另一个度为2的节点为止。这样一来，就完成了第一行的填充。

接下来可以先通过第一行的列数以及n来计算出需要填充的总行数m，然后开始进行第二行到第m行的填充。

首先依然是考虑最左侧节点如何填充。对于第二行的第一个节点，其必须是第一行第一个节点的邻居，且这个节点没有被填充在第一行的第二个节点上；对于第三行以及之后的第一个节点，其必须是上一行第一个节点的邻居，且这个节点既没有被填充在上上行的第一个节点，也没有被填充在上一行的第二个节点。

按照这个原则，遍历上一行的第一个节点在图中的相邻节点，找出唯一一个没有被用过的节点填充在当前行的最左侧。接下来对于当前行的其他节点，则可以从第一个节点开始向右进行遍历，对于当前列需要填充的节点，其必须是其左侧节点在图中的相邻节点，同时也必须是其上方节点在图中的相邻节点，那么在这里就可以遍历其左侧节点在图中的所有邻居y，若y既是其上方节点在图中的邻居，同时y也没有被填充在左上方的位置，那么就可以将y填充在当前列。

按照上面的方法逐行完成填充即可。

最后附上python代码：

```python
class Solution(object):
    def constructGridLayout(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """

        g = [set() for _ in range(n)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        degree = [len(g[x]) for x in range(n)]
        res = []

        if min(degree) == 1:
            for x in range(n):
                if degree[x] == 1:
                    break

            res.append([x])
            while len(res[-1]) < n:
                for y in g[res[-1][-1]]:
                    if len(res[-1]) == 1 or y != res[-1][-2]:
                        res[-1].append(y)
                        break
        
        elif max(degree) <= 3:
            res.append([])
            res.append([])

            for x in range(n):
                if degree[x] == 2:
                    break
            res[0].append(x)
            for y in g[x]:
                if degree[y] == 2 and len(res[1]) < len(res[0]):
                    res[1].append(y)
                else:
                    res[0].append(y)

            for col in range(1, n // 2 - 1):
                for y in g[res[0][col]]:
                    if y == res[0][col - 1]:
                        continue
                    if y in g[res[1][col - 1]]:
                        res[1].append(y)
                    else:
                        res[0].append(y)
            
            for y in g[res[0][-1]]:
                if degree[y] == 2 and y != res[0][-2]:
                    res[1].append(y)
                    break

        else:
            res.append([])
            for x in range(n):
                if degree[x] == 2:
                    break
            
            res[0].append(x)
            while len(res[0]) == 1 or degree[res[0][-1]] != 2:
                for y in g[res[0][-1]]:
                    if degree[y] != 4 and (len(res[0]) == 1 or res[0][-2] != y):
                        res[0].append(y)
                        break
            
            m = n // len(res[0])
            for row in range(1, m):
                res.append([])
                for y in g[res[row - 1][0]]:
                    if y != res[row - 1][1] and (row == 1 or y != res[row - 2][0]):
                        res[row].append(y)
                        break
                
                for col in range(1, len(res[0])):
                    for y in g[res[row][col - 1]]:
                        if y != res[row - 1][col - 1] and y in g[res[row - 1][col]]:
                            res[row].append(y)
                            break

        return res
```
