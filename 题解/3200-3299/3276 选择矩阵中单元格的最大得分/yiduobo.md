---
title: "3276. 选择矩阵中单元格的最大得分"
aliases: ["yiduobo的每日leetcode 3276.选择矩阵中单元格的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/graph", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794214537"
zhihu_id: "794214537"
zhihu_title: "yiduobo的每日leetcode 3276.选择矩阵中单元格的最大得分"
question_id: "3276"
question: "选择矩阵中单元格的最大得分"
problem_url: "https://leetcode.cn/problems/select-cells-in-grid-with-maximum-score/"
difficulty: "Hard"
rating: 2403
created: "2024-10-03T02:14:33+08:00"
updated: "2024-10-03T02:14:33+08:00"
upvotes: 1
comments: 0
---

# 3276. 选择矩阵中单元格的最大得分

> **[yiduobo的每日leetcode 3276.选择矩阵中单元格的最大得分](https://zhuanlan.zhihu.com/p/794214537) · 知乎 · 2024-10-03 · 赞同 1**
> 力扣：[3276. 选择矩阵中单元格的最大得分](https://leetcode.cn/problems/select-cells-in-grid-with-maximum-score/) · Hard · 灵茶山艾府：[枚举值域，状压行号，附费用流做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3276.选择矩阵中单元格的最大得分

[. - 力扣（LeetCode）](https://leetcode.cn/problems/select-cells-in-grid-with-maximum-score/description/)

题目给出一个二维矩阵grid，要求从中选出一个或多个单元格，要求每行只能选择一个单元格，且单元格内的数字不能相同。问如何选择可以使得选择的单元格元素之和最大。

题目中矩阵的行和列都不超过10，而单元格中的元素大小不超过100。

题目中这个10基本上就是用dfs或者状态压缩动态规划了，而本题看上去是按某个顺序都选，而不是选或者不选，这也就意味着不加任何优化的dfs是O(n!)的，所以这里优先考虑后者。

当然，直接套用状态压缩动态规划也不是那么方便，因为本题的限制条件并不是不能同列，而是数值不能相同，而数值的规模到了100，不能保留在压缩过的状态中。

一种可行的转化方法是将数值视为列号重新构造矩阵，例如样例中的矩阵就可以修改成

| 1 | 2 | 3 | 0 |
| --- | --- | --- | --- |
| 0 | 2 | 3 | 4 |
| 1 | 0 | 0 | 0 |

题目就变成了对于上面修改过的矩阵，从中选择若干单元格，这些单元格的行和列都互不相同，问选择的单元格之和最大为多少，其中行数不超过10，列数不超过100。

到了这里，就可以通过f[j][state]表示前j列中选择若干单元格，这些单元格占据了state表示的行时的最大单元格之和，那么对于f[j][state]，可以不选任意单元格，就是f[j][state] \= f[j - 1][state]，也可以选择当前列中值不为0，且所在行被state所包含的单元格，若这个单元格处于第i行，那么就是f[j][state] \= f[j - 1][state ^ (1 \<\< i)] + j。

除此之外，在这里使用网络流是更好的做法。

在这里需要先明确一点，应该选择尽量多的单元格，即可以使用最大流相关的算法来解决这个问题。理由是本题中单元格的值为正数，那么对于某一行，如果按照当前最优的选择无法从这一行中选出任意单元格，就说明这一行中所有单元格的值都在其他行被选择过了。对于这种情况，如果有可能通过变更其他行选择的单元格的值，使得这一行也有单元格可以被选择的话，即“有可能选择更多的单元格”，那么就应该进行变更，因为此时在变更前选择的单元格对应的值将在这一行被选择，也就相当于在之前的基础上多出了变更后的单元格的值，一定是更优的，也就是说最优的选择方案一定是尽量选择了尽量多的单元格。

有了这个前提，就可以使用费用流来求解了。

具体建图方法为：

1、将grid中的每一行都抽象成一个点，其中第i行编号为i

2、设置源点s的编号为总行数m

3、将1到矩阵中的最大值ma都抽象成一个点，其中大小为j的数值编号为m + j

4、设置汇点t的编号为m + ma + 1

5、从s向每一行对应的点发射一条容量为1，费用为0的边，容量1表示每一行最多选择一个数，费用0是因为具体选数时才会产生费用

6、若第i行中存在数字j，那么就从i向m + j发射一条容量为1，费用为ma - j的边，表示可以在i这一行可以选择j这个数，而选择的费用则为ma - j，同时建立反向边，方向边容量为0，费用取反

7、从1到ma都向j发射一条容量为1，费用为0的边，表示每个数值只能选择一次

建图完成后，执行最小费用最大流算法，最终答案就是流量乘以ma再减去最小费用。

费用流的具体实现这里就不展开了，因为我没有自信可以在这里把原理讲得特别清楚，有兴趣的同学可以查一查相关的资料。

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

        ma = 0
        for i in range(m):
            for j in range(n):
                ma = max(ma, grid[i][j])
        
        s = m
        t = m + ma + 1

        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]
        
        for i in range(m):
            c[s][i] = 1
        
        for j in range(m + 1, m + ma + 1):
            c[j][t] = 1
        
        for i in range(m):
            for j in range(n):
                c[i][m + grid[i][j]] = 1
                cost[i][m + grid[i][j]] = ma - grid[i][j]
                cost[m + grid[i][j]][i] = grid[i][j] - ma

        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                nxt = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + cost[now][index]):
                        dis[index] = dis[now] + cost[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        nxt = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(nxt)
                now = nxt

            res += ma - dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]
```
