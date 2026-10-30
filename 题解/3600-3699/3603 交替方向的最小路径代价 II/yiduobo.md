---
title: "3603. 交替方向的最小路径代价II"
aliases: ["yiduobo的每日leetcode 3603.交替方向的最小路径代价II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1941642812916466742"
zhihu_id: "1941642812916466742"
zhihu_title: "yiduobo的每日leetcode 3603.交替方向的最小路径代价II"
question_id: "3603"
question: "交替方向的最小路径代价 II"
problem_url: "https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-ii/"
difficulty: "Medium"
rating: 1639
created: "2025-08-20T23:36:40+08:00"
updated: "2025-08-20T23:36:40+08:00"
upvotes: 2
comments: 0
---

# 3603. 交替方向的最小路径代价II

> **[yiduobo的每日leetcode 3603.交替方向的最小路径代价II](https://zhuanlan.zhihu.com/p/1941642812916466742) · 知乎 · 2025-08-20 · 赞同 2**
> 力扣：[3603. 交替方向的最小路径代价 II](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-ii/) · Medium · 灵茶山艾府：[网格图 DP：记忆化搜索 / 递推 / 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3603.交替方向的最小路径代价II

[3603. 交替方向的最小路径代价 II - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-path-with-alternating-directions-ii/description/)

题目给出两个整数m和n，分别表示网格的行数和列数。进入单元格(i, j)的成本定义为(i + 1) \* (j + 1)。另外给出一个二维数组waitCost，其中waitCost[i][j]表示在(i, j)等待的成本。

路径始终从第1步进入单元格(0, 0)并支付入场花费开始。在奇数秒，必须向右或者向下移动到相邻的单元格，并支付其进入成本；在偶数秒，则需要原地等待1秒，并支付等待的费用waitCost[i][j]。

问到达(m - 1, n - 1)所需的最小成本。

可以发现，除了第一秒进入(0, 0)，并走到(0, 1)或者(1, 0)外，其他所有奇数秒的行动之前，必然存在一个偶数秒的等待。如果令f[i][j]表示走到(i, j)所需的最小代价，那么对于除了(0, 0)，(0, 1)，(1, 0)之外的(i, j)，就有f[i][j] \= min(f[i - 1][j] + waitCost[i - 1][j], f[i][j - 1] + waitCost[i][j - 1]) + (i + 1) \* (j + 1)，也就是走到上一个单元格所需的代价，加上在上一个单元格等待的代价。

基于这一点，只需从左上角到右下角进行逐个单元格遍历，计算对应的f值即可。需要注意特别处理(0, 0), (0, 1)，(1, 0)这三个单元格的f值，另外对于第0行以及第0列的单元格，只有唯一的上一个单元格，也需要特殊处理。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, m, n, waitCost):
        """
        :type m: int
        :type n: int
        :type waitCost: List[List[int]]
        :rtype: int
        """
        
        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j] = 1
                elif i == 0:
                    if j == 1:
                        f[i][j] = 3
                    else:
                        f[i][j] = f[i][j - 1] + waitCost[i][j - 1] + (i + 1) * (j + 1)
                elif j == 0:
                    if i == 1:
                        f[i][j] = 3
                    else:
                        f[i][j] = f[i - 1][j] + waitCost[i - 1][j] + (i + 1) * (j + 1)
                else:
                    f[i][j] = min(f[i][j - 1] + waitCost[i][j - 1], f[i - 1][j] + waitCost[i - 1][j]) + (i + 1) * (j + 1)
        
        return f[-1][-1]
```
