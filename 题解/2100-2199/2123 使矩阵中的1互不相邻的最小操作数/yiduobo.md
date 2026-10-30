---
title: "2123. 使矩阵中的1互不相邻的最小操作数"
aliases: ["yiduobo的每日leetcode 2123.使矩阵中的1互不相邻的最小操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626355710"
zhihu_id: "626355710"
zhihu_title: "yiduobo的每日leetcode 2123.使矩阵中的1互不相邻的最小操作数"
question_id: "2123"
question: "使矩阵中的1互不相邻的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-remove-adjacent-ones-in-matrix/"
created: "2023-05-02T23:24:21+08:00"
updated: "2023-05-02T23:24:21+08:00"
upvotes: 0
comments: 0
---

# 2123. 使矩阵中的1互不相邻的最小操作数

> **[yiduobo的每日leetcode 2123.使矩阵中的1互不相邻的最小操作数](https://zhuanlan.zhihu.com/p/626355710) · 知乎 · 2023-05-02 · 赞同 0**
> 力扣：[2123. 使矩阵中的1互不相邻的最小操作数](https://leetcode.cn/problems/minimum-operations-to-remove-adjacent-ones-in-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2123.是矩阵中的1互不相邻的最小操作数

[力扣](https://leetcode.cn/problems/minimum-operations-to-remove-adjacent-ones-in-matrix/)

经典的二分图匹配问题，可以按照一下的思路逐步转化。

首先，题目需要处理的是相邻的1构成的点对。现在的问题就是要求从中选出最少的点，使得每个点对中至少有一段处理选出的点集当中。

另一方面，对于棋盘类问题上相邻点对的问题，一种常见的处理方法是将其转化为二分图来进行处理。简单描述来说，对于棋盘位于(i, j)位置的位置，可以根据i + j的奇偶性将这些位置分为左右两侧，可以发现若两个位置相邻，那么这两个位置对应的点必然分处图的两侧。

接下来，对于每一组相邻的1，可以在二分图中新增一条边，那么问题就转化成了在二分图中选择一些点，要求这些点能覆盖住图中所有的边。这是经典的二分图最小点覆盖集问题，等价于求解二分图的最大匹配。具体的证明可以参考konig定理，这里就不展开了。

到了这里，只需要跑一遍匈牙利算法，找出最大匹配就行了。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        linked = {}
        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if (i + j) % 2 == 0 and grid[i][j] == 1:
                    left = i * n + j
                    if left not in linked:
                        linked[left] = []

                    if i > 0 and grid[i - 1][j] == 1:
                        linked[left].append(left - n)
                    if i < m - 1 and grid[i + 1][j] == 1:
                        linked[left].append(left + n)
                    if j > 0 and grid[i][j - 1] == 1:
                        linked[left].append(left - 1)
                    if j < n - 1 and grid[i][j + 1] == 1:
                        linked[left].append(left + 1)

        p = {}
        def match(left):
            for right in linked[left]:
                if right not in vis:
                    vis.add(right)
                    if right not in p or match(p[right]):
                        p[right] = left
                        return True
            return False

        res = 0
        for left in linked:
            vis = set()
            if match(left):
                res += 1
        
        return res
```
