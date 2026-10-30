---
title: "3148. 矩阵中的最大得分"
aliases: ["yiduobo的每日leetcode 3148.矩阵中的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/贪心算法", "题单/常用数据结构/一-前缀和", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703624458"
zhihu_id: "703624458"
zhihu_title: "yiduobo的每日leetcode 3148.矩阵中的最大得分"
question_id: "3148"
question: "矩阵中的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-difference-score-in-a-grid/"
difficulty: "Medium"
rating: 1820
created: "2024-06-16T01:39:22+08:00"
updated: "2024-06-16T01:39:37+08:00"
upvotes: 1
comments: 0
---

# 3148. 矩阵中的最大得分

> **[yiduobo的每日leetcode 3148.矩阵中的最大得分](https://zhuanlan.zhihu.com/p/703624458) · 知乎 · 2024-06-16 · 赞同 1**
> 力扣：[3148. 矩阵中的最大得分](https://leetcode.cn/problems/maximum-difference-score-in-a-grid/) · Medium · 灵茶山艾府：[脑筋急转弯+二维前缀最小值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3148.矩阵中的最大得分

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-difference-score-in-a-grid/description/)

题目给出一个正整数组成的二维矩阵grid，可以从矩阵中任意位置移动到其正右侧或者其正下方的另一个单元格。从值为c1的单元格移动到值为c2的单元格的得分为c2 - c1。现在可以从矩阵中任意位置开始，但是至少需要移动一步，问移动路径的最大得分是多少。

不妨设移动路径上一共有m个单元格，其值分别为c[1]、c[2]、...、c[m]，那么最终的总得分就是

(c[2] - c[1]) + (c[3] - c[2]) + ... + (c[m] - c[m - 1])

可以发现，除了c[1]和c[m]外，其他所有元素都将被消去，那么问题实际上就变成了从矩阵中某个单元格出发，走到其右下方的另一个单元格，要求终点的值减去起点的值最大。

于是在这里可以枚举终点单元格(i, j)，问题就变成了找出以(0, 0)为左上角，(i, j)为右下角的矩阵中，除(i, j)自身之外其他单元格的最小值，那么从这个最小的单元格出发就是(i, j)对应的最优起点。而对于左上角矩阵中最小值这个问题，则可以通过动态规划求解。令f[i][j]以(0, 0)为左上角，(i, j)为右下角的矩阵中的最小值，那么对于f[i][j]：

1、当i \= 0且j \= 0时：

矩阵中仅有grid[0][0]这一个元素，因此f[i][j] \= grid[i][j]。

另外在这种情况下，不存在以(i, j)为终点的合法路径。

2、当i \= 0且j > 0时：

此时f[i][j]对应的矩阵可以认为是f[i][j - 1]对应的矩阵，再加上grid[i][j]这个元素组成，因此就有f[i][j] \= min(f[i][j - 1], grid[i][j])。

这种情况下，(i, j)对应最优起点将出现在f[i][j - 1]对应的矩阵中，此时应该用grid[i][j] - f[i][j - 1]来更新答案。

3、当i > 0且j \= 0时：

此时与情况2对称，有f[i][j] \= min(f[i - 1][j], grid[i][j])，同时用grid[i][j] - f[i - 1][j]来更新答案。

4、当i > 0且j > 0时：

此时f[i][j]对应的矩阵可以认为是f[i][j - 1]对应的矩阵，叠加上f[i - 1][j]对应的矩阵，再加上grid[i][j]这个元素组成。虽然f[i - 1][j - 1]对应的矩阵会被考虑两次，但是这里f计算的是最小值，重复计算不影响最终结果。因此就有f[i][j] \= min(f[i][j - 1], f[i - 1][j], grid[i][j])。

这种情况下，(i, j)对应的最优起点要么出现在f[i][j - 1]对应的矩阵中，要么出现在f[i - 1][j]对应的矩阵中，此时应该用grid[i][j] - min(f[i][j - 1], f[i - 1][j])来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        res = -100000
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = grid[i][j]
                    else:
                        res = max(res, grid[i][j] - f[i][j - 1])
                        f[i][j] = min(f[i][j - 1], grid[i][j])
                elif j == 0:
                    res = max(res, grid[i][j] - f[i - 1][j])
                    f[i][j] = min(f[i - 1][j], grid[i][j])
                else:
                    res = max(res, grid[i][j] - min(f[i - 1][j], f[i][j - 1]))
                    f[i][j] = min(f[i - 1][j], f[i][j - 1], grid[i][j])

        return res
```
