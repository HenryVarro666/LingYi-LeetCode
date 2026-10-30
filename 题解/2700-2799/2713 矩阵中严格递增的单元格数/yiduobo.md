---
title: "2713. 矩阵中严格递增的单元格数"
aliases: ["yiduobo的每日leetcode 2713.矩阵中严格递增的单元格数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/ordered-set", "leetcode/sorting", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651483885"
zhihu_id: "651483885"
zhihu_title: "yiduobo的每日leetcode 2713.矩阵中严格递增的单元格数"
question_id: "2713"
question: "矩阵中严格递增的单元格数"
problem_url: "https://leetcode.cn/problems/maximum-strictly-increasing-cells-in-a-matrix/"
difficulty: "Hard"
rating: 2387
created: "2023-08-22T03:17:17+08:00"
updated: "2023-08-22T03:17:17+08:00"
upvotes: 0
comments: 0
---

# 2713. 矩阵中严格递增的单元格数

> **[yiduobo的每日leetcode 2713.矩阵中严格递增的单元格数](https://zhuanlan.zhihu.com/p/651483885) · 知乎 · 2023-08-22 · 赞同 0**
> 力扣：[2713. 矩阵中严格递增的单元格数](https://leetcode.cn/problems/maximum-strictly-increasing-cells-in-a-matrix/) · Hard · 灵茶山艾府：[动态规划+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2713.矩阵中严格递增的单元格数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-strictly-increasing-cells-in-a-matrix/)

朴素的动态规划是很容易想到的，可以仿照登山问题给出状态表示：f[i][j]表示从单元格(i, j)出发可以访问的最大单元格数量，那么对于f[i][j]，初始情况下就有f[i][j] \= 1，接下来需要枚举第i行以及第j列的所有单元格，对于其中满足mat[i][y] > mat[i][j]的单元格(i, y)或者满足mat[x][j] > mat[i][j]的单元格(x, j)，就有

f[i][j] \= max(f[i][j], f[i][y] + 1)

f[i][j] \= max(f[i][j], f[x][j] + 1)

计算完成后，f中的最大值即为最终答案。

这是一个O((mn)^2)的算法，在题目给出的数据规模下是不可行的，必须进行优化。状态表示的这两维是不太好动的，因此只能从转移方程入手。

可以发现，f[i][j]的更新实际上取决于其所在行和列中满足条件的f的最大值，而这个条件就是其对应的单元格的值要大于(i, j)的值。那么一个自然的想法就是将所有单元格从大到小进行排序，然后逐个计算其对应的f值，此时计算f[i][j]时，所有已经计算好f值的单元格的数值必然都大于(i, j)的值，因此在这里就只需取第i行以及第j列中所有已经计算出的f值的最大值来更新f[i][j]就行了。为了高效取到这个最大值，则可以使用两个哈希表row和col分别记录每一行和每一列中，当前已经计算好的f值的最大值，那么对于f[i][j]，就可以使用row[i]和col[j]中的较大值来进行更新，然后再反过来利用f[i][j]更新row[i]和col[j]。

到了这里，整个算法的时间复杂度就降到了O(mn)，是一个可行的算法了。

另外需要特别注意的是，对于值相同的单元格，需要在一个批次内分别计算，然后再使用计算的f值更新row和col，否则会出现某个位置的f值是通过其同行或同列的同值单元格更新过来的，与题目要求的严格递增不符。

最后附上python代码：

```python
class Solution(object):
    def maxIncreasingCells(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])

        row = [0] * m
        col = [0] * n

        num_list = []
        for i in range(m):
            for j in range(n):
                num_list.append([-mat[i][j], i, j])
        
        num_list.sort()
        left = 0
        res = 0
        while left < len(num_list):
            right = left + 1
            while right < len(num_list) and num_list[left][0] == num_list[right][0]:
                right += 1

            step = []
            for v, x, y in num_list[left: right]:
                step.append(max(row[x], col[y]) + 1)
                res = max(res, step[-1])
            
            for index in range(len(step)):
                v, x, y = num_list[left + index]
                row[x] = max(row[x], step[index])
                col[y] = max(col[y], step[index])
            
            left = right
        
        return res
```
