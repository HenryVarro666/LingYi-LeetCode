---
title: "3225. 网格图操作后的最大分数"
aliases: ["yiduobo的每日leetcode 3225.网格图操作后的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719841508"
zhihu_id: "719841508"
zhihu_title: "yiduobo的每日leetcode 3225.网格图操作后的最大分数"
question_id: "3225"
question: "网格图操作后的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-from-grid-operations/"
difficulty: "Hard"
rating: 3028
created: "2024-09-13T02:43:01+08:00"
updated: "2024-09-13T02:43:01+08:00"
upvotes: 3
comments: 0
---

# 3225. 网格图操作后的最大分数

> **[yiduobo的每日leetcode 3225.网格图操作后的最大分数](https://zhuanlan.zhihu.com/p/719841508) · 知乎 · 2024-09-13 · 赞同 3**
> 力扣：[3225. 网格图操作后的最大分数](https://leetcode.cn/problems/maximum-score-from-grid-operations/) · Hard · 灵茶山艾府：[【图解】DP 及其优化：从 n^4 到 n^3 到 n^2（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3225.网格图操作后的最大分数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-score-from-grid-operations/)

题目给出一个n \* n的二维矩阵grid，一开始grid中的每个格子都为白色，且每个格子都有一个非负的分数。

对于grid中的每一列j，都可以选择一个位置(i, j)，将(i, j)以及j这一列中位于(i, j)上方的所有格子染成黑色，当然也可以不进行选择，那么j这一列则继续保持白色。

完成染色后，若某个格子(i, j)为白色，且其同一行左右两个相邻格子中至少有一个黑色格子，那么就将grid[i][j]累加到最终得分中。

问如何染色才能使得最终得分最大。

---

常规的动态规划是比较容易想到的：令f[i][j][k]表示前i列，最后这一列染黑了j个格子，左侧相邻的列染黑了k个格子时可以得到的最大得分。那么对于f[i][j][k]：

1、首先考虑边界情况：

当只有一列时所有的f值必然都为0。

当只有两列时，需要对比当前j和k的大小。若j较大，那么第0列的k + 1到j这些格子可以得分，反之则是第1列的j + 1到k这些格子可以得分。

注意到题目中得分的格子必然都是某一列中的连续格子，是一个区间和问题，那么可以对每一列都计算前缀和，这样一来就可以在O(1)的时间内计算出对应的区间和了。

为了方便描述，在这里令s[i][j]表示grid[i][0] + grid[i][1] + ... + grid[i][j]，那么对于只有两列的情况，当j较大时，f[i][j][k] \= s[0][j] - s[0][k]，反之若k较大，那么f[i][j][k] \= s[1][k] - s[1][j]。

2、接下来对于i >\= 2的一般情况：

对于这种情况，最直观的思路自然是枚举当前列往左两列染黑的格子数量t，然后根据j、k、t的大小关系以及f[i - 1][k][t]来更新f[i][j][k]，具体来说：

2-1）当k \<\= j时:

这种情况下新的得分只会出现在i - 1这一列，而根据j、k、t的大小关系，部分格子的得分可能已经在f[i - 1][k][t]中计算过了，因此有需要再进行细分：

2-1-1）当t \<\= k \<\= j时：

| t | k | j |
| --- | --- | --- |
| X | X | X |
|  | X | X |
|  | 得分 | X |
|  | 得分 | X |

此时得分不会受到t的影响，因此最终得分为f[i - 1][k][t] + s[i - 1][j] - s[i - 1][k]

2-1-2）当k \< t \<\= j时：

| t | k | j |
| --- | --- | --- |
| X | X | X |
| X | 上轮得分 | X |
|  | 得分 | X |
|  | 得分 | X |

此时grid[i - 1][k + 1]到grid[i - 1][t]的得分已经被计算过了，因此最终得分为f[i - 1][k][t] + s[i - 1][j] - s[i - 1][t]

2-1-3）当k \<\= j \< t时：

| t | k | j |
| --- | --- | --- |
| X | X | X |
| X | 上轮得分 | X |
| X | 上轮得分 |  |
| X | 上轮得分 |  |

此时没有新的得分产生，最终得分为f[i - 1][k][t]

2-2）当k > j时：

| t | k | j |
| --- | --- | --- |
|  | X | X |
|  | X | X |
|  | X | 得分 |
|  | X | 得分 |

这种情况下新的得分只会出现在i这一列，此时无论t如何取值，产生得分的区域都是grid[i][j + 1]到grid[i][k]，因此最终得分为f[i - 1][k][t] + s[i][k] - s[i][j]

到了这里，就得到了一种时间复杂度为O(n^4)的算法，其中状态表示为O(n^3)，转移时需要枚举t，所以总的时间复杂度为O(n^4)。

本题中的n最大取值为100，因此上面的算法还需要进行优化。

---

观察上面几种情况的转移方程，可以发现对于

1、t \<\= k \<\= j：

f[i][j][k] \= max(f[i][j][k], f[i - 1][k][t] + s[i - 1][j] - s[i - 1][k])

2、k \<\= j \< t：

f[i][j][k] \= max(f[i][j][k], f[i - 1][k][t])

3、k > j：

f[i][j][k] \= max(f[i][j][k], f[i - 1][k][t] + s[i][k] - s[i][j])

这三种情况而言，后面要么没有s的部分，要么s的部分与t完全无关。换言之，对于这三种情况，并不需要枚举所有的t，只需要想办法高效地找出最大的f[i - 1][k][t]就行了。

需要特别注意的是，前两种情况分别限定了t \<\= k以及k \< t，因此在这里需要使用两个数组best1[i][j]以及best2[i][j]来分别表示f[i][j][0]到f[i][j][k]之间的最大值，以及f[i][j][k + 1]到f[i][j][n - 1]之间的最大值，即best1[i][j]和best2[i][j]分别表示了限定k \<\= j时最优的f[i][j][k]以及限定了j \< k时最优的f[i][j][k]。

在i这一维上往前移动一步，对应的就是best1[i - 1][k]表示限定了t \<\= k时最优的f[i - 1][k][t]，best2[i - 1][k]表示限定了k \< t时最优的f[i - 1][k][t]。这样一来，上面三种情况的转移方程就可以写成：

1、t \<\= k \<\= j：

f[i][j][k] \= max(f[i][j][k], best1[i - 1][k] + s[i - 1][j] - s[i - 1][k])

2、k \<\= j \< t：

f[i][j][k] \= max(f[i][j][k], best2[i - 1][k])

3、k > j：

f[i][j][k] \= max(f[i][j][k]，max(best1[i - 1][k], best2[i - 1][k]) + s[i][k] - s[i][j])

对于上面三种情况，在计算f[i][j][k]后，根据j和k的大小关系再回过头去更新best[i][j]即可。

到了这里，还剩下k \< t \<\= j这种情况需要考虑。

---

可以发现，当中间这一列染色的块最少时，其染成的黑色无法给第i列或者第i - 2列带来任何的收益。另一方面，由于题目保证了grid的分数非负，因此对于这种情况，中间这一列就应该保持全白才能尽量多得分。

换言之，对于k \< t \<\= j以及k \<\= j \< t，都只需要考虑k \= 0的情况，这样一来，就可以照常暴力枚举t，根据j和t的大小直接计算对应的f[i][j][k]了。

需要注意，计算完成后还是要使用f[i][j][k]来更新best1[j]。

---

综合上面几种情况，就有：

1、当k \= 0时：

直接暴力枚举t。当j >\= t时，有f[i][j][k] \= max(f[i][j][k], f[i - 1][k][t] + s[i - 1][j] - s[i - 1][t])，反之就有f[i][j][k] \= max(f[i][j][k], f[i - 1][k][t])

2、当k > 0且k \<\= j时：

此时默认k >\= t，因为k \< t的情况对应的f[i][j][k]必然比f[i][j][0]要差，无需计算。因此在这里就有f[i][j][k] \= max(f[i][j][k], best1[i - 1][k] + s[i - 1][j] - s[i - 1][k])

3、当k > j时：

有f[i][j][k] \= max(f[i][j][k], max(best1[i - 1][k], best2[i - 1][k]) + s[i][k] - s[i][j])

这样一来，对于k \= 0情况，转移的复杂度为O(n)，而对于k > 0的情况，转移的复杂度为O(1)，整体的时间复杂度就优化到了O(n^3)。另外注意到f和best的每一轮只与上一轮有关，因此可以使用滚动数组优化掉i这一维来优化空间。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid)

        if n < 2:
            return 0
        
        s = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s[i][j + 1] = s[i][j] + grid[j][i]

        best_f1 = [0] * (n + 1)
        best_f2 = [0] * (n + 1)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for j in range(n + 1):
            for k in range(n + 1):
                if j >= k:
                    f[j][k] = s[0][j] - s[0][k]
                    best_f1[j] = max(best_f1[j], f[j][k])
                else:
                    f[j][k] = s[1][k] - s[1][j]
                    best_f2[j] = max(best_f2[j], f[j][k])

        for i in range(2, n):
            g = f[:]
            f = [[0] * (n + 1) for _ in range(n + 1)]

            best_g1 = best_f1[:]
            best_g2 = best_f2[:]
            best_f1 = [0] * (n + 1)
            best_f2 = [0] * (n + 1)

            for j in range(n + 1):
                for k in range(n + 1):
                    if k == 0:
                        for t in range(n + 1):
                            if j >= t:
                                f[j][k] = max(f[j][k], g[k][t] + s[i - 1][j] - s[i - 1][t])
                            else:
                                f[j][k] = max(f[j][k], g[k][t])

                        best_f1[j] = max(best_f1[j], f[j][k])
                    
                    elif j >= k:
                        f[j][k] = max(f[j][k], best_g1[k] + s[i - 1][j] - s[i - 1][k])
                        best_f1[j] = max(best_f1[j], f[j][k])
                    
                    else:
                        f[j][k] = max(f[j][k], max(best_g1[k], best_g2[k]) + s[i][k] - s[i][j])
                        best_f2[j] = max(best_f2[j], f[j][k])

        return max(max(best_f1), max(best_f2))
```
