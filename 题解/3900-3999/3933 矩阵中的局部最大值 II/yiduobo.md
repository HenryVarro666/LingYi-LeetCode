---
title: "3933. 矩阵中的局部最大值II"
aliases: ["yiduobo的每日leetcode 3933.矩阵中的局部最大值II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/segment-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042063587271783079"
zhihu_id: "2042063587271783079"
zhihu_title: "yiduobo的每日leetcode 3933.矩阵中的局部最大值II"
question_id: "3933"
question: "矩阵中的局部最大值 II"
problem_url: "https://leetcode.cn/problems/largest-local-values-in-a-matrix-ii/"
difficulty: "Medium"
created: "2026-05-26T21:43:08+08:00"
updated: "2026-05-26T21:43:11+08:00"
upvotes: 1
comments: 0
---

# 3933. 矩阵中的局部最大值II

> **[yiduobo的每日leetcode 3933.矩阵中的局部最大值II](https://zhuanlan.zhihu.com/p/2042063587271783079) · 知乎 · 2026-05-26 · 赞同 1**
> 力扣：[3933. 矩阵中的局部最大值 II](https://leetcode.cn/problems/largest-local-values-in-a-matrix-ii/) · Medium · 灵茶山艾府：[两种方法：二维 ST 表 / 线段树套 ST 表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3933.矩阵中的局部最大值II

<https://leetcode.cn/problems/largest-local-values-in-a-matrix-ii/>

题目给出一个n \* m的整数矩阵matrix，其中所有的元素均为非负整数。n、m以及matrix中元素的大小都不超过200。

对于matrix中的非零的单元格(row, col)，令x \= matrix[row][col]，接下来对于在(row, col)的x行和x列范围内，所有行距离和列距离不同时等于x的单元格，若这些单元格中不存在值大于x的单元格，那么就称matrix[row][col]是一个局部最大值。

要求计算matrix中局部最大值的数量。

一个直观的思路是直接枚举每个单元格，然后按照题目的描述检测子矩阵内的最大值是否大于当前元素。基于本题的数据规模考虑，计算子矩阵内的最大值不能使用O(nm)的暴力算法，在这里可以使用二维st表来计算，时间复杂度为O(nmlog(nm))。

我在这里使用的是另一种计算方法。

首先，对于矩阵中的所有元素，其能否成为局部最大值，只取决于那些大于该元素的其他元素是否出现在以matrix[row][col]为中心的子矩阵中。那么在这里就可以先将矩阵中所有元素按照数值大小收集起来，然后按从大到小的顺序分批处理。

对于当前批次，枚举其中的所有元素。对于当前元素，需要检测之前批次中的元素是否出现在以当前元素为中心的子矩阵中。对于这个问题，可以使用二维树状数组求解。

具体来说，对于matrix[row][col]，需要计算以(row - x, col - x)为左下角，(row + x, col + x)为右上角的子矩阵中之前批次的元素数量，这个子矩阵则可以拆分为4个前缀矩阵来进行计算，而对于前缀矩阵，就可以使用二维树状数组来进行高效计算了。

得到子矩阵中之前批次的元素数量后，还需要排除掉刚好落在子矩阵四个角落上的元素数量，在这里可以通过集合记录之前处理过哪些位置上的元素来辅助计算。

接下来，若最终得到的之前批次处理过的元素数量为0，说明子矩阵范围内不存在更大的元素，当前的matrix[row][col]是一个局部最大值，此时需要更新答案。反之，则说明其不是，此时无事发生。

当前批次全部计算完成后，使用当前批次的所有位置更新二维树状数组，然后继续下一批次的计算。

最后附上python代码：

```python
class Solution(object):
    def countLocalMaximums(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """
        
        pos = {}

        m = len(matrix)
        n = len(matrix[0])

        for i in range(m):
            for j in range(n):
                if matrix[i][j] > 0:
                    if matrix[i][j] not in pos:
                        pos[matrix[i][j]] = []
                    pos[matrix[i][j]].append((i, j))
        
        f = [[0] * (n + 1) for _ in range(m + 1)]
        res = 0
        filled = set()

        def add(x, y):
            tmp = y
            while x <= m:
                y = tmp
                while y <= n:
                    f[x][y] += 1
                    y += y & -y
                x += x & -x
        
        def get(x, y):
            tmp = y
            s = 0
            while x > 0:
                y = tmp
                while y > 0:
                    s += f[x][y]
                    y -= y & -y
                x -= x & -x
            return s

        for v in sorted(pos.keys(), reverse=True):
            for x, y in pos[v]:
                x1 = max(x - v, 0)
                y1 = max(y - v, 0)
                x2 = min(x + v, m - 1)
                y2 = min(y + v, n - 1)

                s = get(x2 + 1, y2 + 1) - get(x2 + 1, y1) - get(x1, y2 + 1) + get(x1, y1)
                if x1 == x - v and y1 == y - v and (x1, y1) in filled:
                    s -= 1
                if x1 == x - v and y2 == y + v and (x1, y2) in filled:
                    s -= 1
                if x2 == x + v and y1 == y - v and (x2, y1) in filled:
                    s -= 1
                if x2 == x + v and y2 == y + v and (x2, y2) in filled:
                    s -= 1
                
                if s == 0:
                    res += 1
            
            for x, y in pos[v]:
                add(x + 1, y + 1)
                filled.add((x, y))
        
        return res
```
