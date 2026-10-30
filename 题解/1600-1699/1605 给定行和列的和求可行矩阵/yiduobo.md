---
title: "1605. 给定行和列的和求可行矩阵"
aliases: ["yiduobo的每日leetcode 1605.给定行和列的和求可行矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dong-hua", "leetcode/gou-zao", "题单/贪心算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/433688910"
zhihu_id: "433688910"
zhihu_title: "yiduobo的每日leetcode 1605.给定行和列的和求可行矩阵"
question_id: "1605"
question: "给定行和列的和求可行矩阵"
problem_url: "https://leetcode.cn/problems/find-valid-matrix-given-row-and-column-sums/"
difficulty: "Medium"
rating: 1868
created: "2021-11-16T00:02:22+08:00"
updated: "2021-11-16T00:02:22+08:00"
upvotes: 1
comments: 0
---

# 1605. 给定行和列的和求可行矩阵

> **[yiduobo的每日leetcode 1605.给定行和列的和求可行矩阵](https://zhuanlan.zhihu.com/p/433688910) · 知乎 · 2021-11-16 · 赞同 1**
> 力扣：[1605. 给定行和列的和求可行矩阵](https://leetcode.cn/problems/find-valid-matrix-given-row-and-column-sums/) · Medium · 灵茶山艾府：[没有思路？一个动画秒懂！附优化写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1605.给定行和列的和求可行矩阵

[力扣](https://leetcode-cn.com/problems/find-valid-matrix-given-row-and-column-sums/)

对于一个m行n列的矩阵，题目就是要通过m + n个方程来确定m \* n个未知数的值。

我在这里采取的是逐行逐列填充的做法。具体来说就是遍历每一行，并使用一个变量pos记录当前填充的列是哪一列，对于当前遍历到的行index而言：

1、若当前的colSum[pos] \< rowSum[index]，那么就将pos这一列的值全部分配给index这一行，也就是说设置res[index][pos]为colSum[pos]。

此时pos这一列已经满足了条件，需要继续考虑下一列，因此需要将pos加上1。

index这一行剩下需要填充的值由rowSum[index]变成了rowSum[index] - colSum[pos]，但尚未满足条件，因此需要重复此过程直到colSum[pos] >\= rowSum[index]为止。

2、若当前的colSum[pos] >\= rowSum[index]，那么此时只需要从pos这一列中分配rowSum[index]给index这一行，也就是说设置res[index][pos]为rowSum[index]。

此时pos这一列剩下需要填充的值由colSum[pos]变成了colSum[pos] - rowSum[index]，但尚未满足条件，因此不需要移动pos。

index这一行则因为满足了条件，因此可以继续考虑下一行了。

最后附上python代码：

```python
class Solution(object):
    def restoreMatrix(self, rowSum, colSum):
        """
        :type rowSum: List[int]
        :type colSum: List[int]
        :rtype: List[List[int]]
        """

        m = len(rowSum)
        n = len(colSum)
        res = [[0] * n for _ in range(m)]
        
        pos = 0
        for index in range(m):
            while colSum[pos] < rowSum[index]:
                res[index][pos] = colSum[pos]
                rowSum[index] -= colSum[pos]
                pos += 1
            
            res[index][pos] = rowSum[index]
            colSum[pos] -= rowSum[index]
        
        return res
```
