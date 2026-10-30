---
title: "2617. 网格图中最少访问的格子数"
aliases: ["yiduobo的每日leetcode 2617.网格图中最少访问的格子数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/monotonic-stack", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/网格图", "题单/动态规划", "题单/常用数据结构/五-堆-优先队列", "题单/网格图/五-综合应用", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646174860"
zhihu_id: "646174860"
zhihu_title: "yiduobo的每日leetcode 2617.网格图中最少访问的格子数"
question_id: "2617"
question: "网格图中最少访问的格子数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-visited-cells-in-a-grid/"
difficulty: "Hard"
rating: 2582
created: "2023-07-27T02:53:35+08:00"
updated: "2023-07-27T02:53:35+08:00"
upvotes: 0
comments: 0
---

# 2617. 网格图中最少访问的格子数

> **[yiduobo的每日leetcode 2617.网格图中最少访问的格子数](https://zhuanlan.zhihu.com/p/646174860) · 知乎 · 2023-07-27 · 赞同 0**
> 力扣：[2617. 网格图中最少访问的格子数](https://leetcode.cn/problems/minimum-number-of-visited-cells-in-a-grid/) · Hard · 灵茶山艾府：[两种方法：单调栈优化 DP / 贪心+最小堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2617.网格图中最少访问的格子数

[力扣](https://leetcode.cn/problems/minimum-number-of-visited-cells-in-a-grid/)

由于本题中的移动只能向右或者向下，那么就可以采用经典的f[i][j]表示走到位置(i, j)所需的最少步数的动态规划算法进行处理。

对于f[i][j]，其可能从同一行的左侧或者同一列的上方走过来，在这里以左侧举例。

因此需要从0到j - 1枚举上一步的列k，若位置(i, k)之前可以到达，且k + grid[i][k] >\= j，那么就说明可以从(i, k)走到(i, j)这个位置，于是就有f[i][j] \= min(f[i][k] + 1)，其中f[i][k]合法且k + grid[i][k] >\= j。可以发现，这是一个最小值的问题，因此可以对每一行都使用一个堆来维护当前这一行所有已经到达过的位置的最少到达步数。

另一方面，若(i, k)由于步长的限制无法到达(i, j)，那么自然也不可能到达(i, j + 1)以及更右侧的位置，也就是说对于位置(i, j + 1)而言，其上一步的候选位置就可以在(i, j)上一步的候选位置的基础上，排除掉无法到达(i, j + 1)的一些位置，因为从这些位置出发也不可能到达(i, j + 1)以及更右侧的位置，因此没必要再将这些位置留在堆中。另外，若grid[i][j]大于0，那么说明可以从(i, j)出发到达(i, j + 1)以及后续的部分位置，因此在计算完f[i][j]后还需要将(i, j)这个位置也加入到堆中。

根据上面的结论，堆中就应该储存部分位置对应的二元组(step, max_bound)，分别表示到达这个位置所需的步数以及从这个位置出发可以到达的最右侧位置。接下来对于f[i][j]，若堆顶元素的max_bound小于j，那么就将其弹出，重复此过程直到堆为空或者堆顶元素对应的max_bound大于等于j。

若此时的堆不为空，那么在水平方向上来看，从堆顶所在的位置走到(i, j)是最优的选择，于是更新f[i][j] \= min(f[i][j], step + 1)，若此时的grid[i][j]大于0，那么还需要将(f[i][j], j + grid[i][j])也加入到堆中。

反之若堆为空，说明(i, j)左侧没有任何位置可以到达j，此时直接跳过就行了。

对于从上方走过来的情况，也可以使用类似的方法，对每一列使用一个堆储存当前列可达位置的所需步数以及从这个位置出发可以到达的最下方位置，然后使用类似的更新方法计算从上方到达(i, j)的最小代价即可。

最后附上python代码：

```python
class Solution(object):
    def minimumVisitedCells(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        h_heap = [[] for _ in range(m)]
        v_heap = [[] for _ in range(n)]
        f = [[-1] * n for _ in range(m)]
        f[0][0] = 1

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    heapq.heappush(h_heap[0], [1, grid[0][0]])
                    heapq.heappush(v_heap[0], [1, grid[0][0]])
                else:
                    while h_heap[i] and h_heap[i][0][1] < j:
                        heapq.heappop(h_heap[i])
                    
                    if h_heap[i]:
                        f[i][j] = h_heap[i][0][0] + 1
                    
                    while v_heap[j] and v_heap[j][0][1] < i:
                        heapq.heappop(v_heap[j])
                    
                    if v_heap[j]:
                        if f[i][j] == -1 or f[i][j] > v_heap[j][0][0] + 1:
                            f[i][j] = v_heap[j][0][0] + 1
                    
                    if f[i][j] != -1 and grid[i][j] > 0:
                        heapq.heappush(h_heap[i], [f[i][j], j + grid[i][j]])
                        heapq.heappush(v_heap[j], [f[i][j], i + grid[i][j]])

        return f[-1][-1]
```
