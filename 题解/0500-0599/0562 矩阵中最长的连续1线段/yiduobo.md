---
title: "562. 矩阵中最长的连续1线段"
aliases: ["yiduobo的每日leetcode 562.矩阵中最长的连续1线段"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601310928"
zhihu_id: "601310928"
zhihu_title: "yiduobo的每日leetcode 562.矩阵中最长的连续1线段"
question_id: "562"
question: "矩阵中最长的连续1线段"
problem_url: "https://leetcode.cn/problems/longest-line-of-consecutive-one-in-matrix/"
created: "2023-01-28T02:03:14+08:00"
updated: "2023-01-28T02:03:14+08:00"
upvotes: 1
comments: 0
---

# 562. 矩阵中最长的连续1线段

> **[yiduobo的每日leetcode 562.矩阵中最长的连续1线段](https://zhuanlan.zhihu.com/p/601310928) · 知乎 · 2023-01-28 · 赞同 1**
> 力扣：[562. 矩阵中最长的连续1线段](https://leetcode.cn/problems/longest-line-of-consecutive-one-in-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

562.矩阵中最长的连续1线段

[力扣](https://leetcode.cn/problems/longest-line-of-consecutive-one-in-matrix/)

经典的动态规划问题。令row[i][j]、col[i][j]、left[i][j]、right[i][j]分别表示以单元格(i, j)为终点的水平方向、竖直方向、左对角线方向、右对角线方向上的连续1的数目，那么对于这四个值，若当前的mat[i][j] \= 0，这四个值都都为0，否则：

当j \= 0时，row[i][j] \= 1，否则row[i][j] \= row[i][j -1] + 1

当i \= 0时，row[i][j] \= 1，否则col[i][j] \= col[i - 1][j] + 1

当i \= 0或j \= n - 1时，left[i][j] \= 0，否则left[i][j] \= left[i - 1][j + 1] + 1

当i \= 0或j \= 0时，right[i][j] \= 0，否则right[i][j] \= right[i - 1][j - 1] + 1

计算完成后，取四个数组中的最大值作为答案即可。

另外，在这里可以发现四个数组的更新都可以通过滚动来省去一维。

除此之外，还存在时间复杂度为O(1)的做法。如果在指定方向上枚举，则完全不需要数组，只需要使用遍历迭代就行了。

以row[i][j]为例，在这里可以只一个变量now而不是数组。每次都按先行后列的方式枚举，在枚举到新的一行时将now清零，接下来对于mat[i][j]，若mat[i][j]为1，则将now加上1，否则将now清零。

对于col，则是先列后行的枚举。两条对角线则略有不同，因为对角线的数目都是m + n - 1，其中m和n分别为mat的高和宽。对于左对角线上的点，其横纵坐标之和相等，且分别从0开始延续到m + n - 1，而对于右对角线上的点，其横纵坐标之差相等，且分别从-(n - 1)开始延续要m - 1。

最后附上python代码：

```python
class Solution(object):
    def longestLine(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])

        now = 0
        res = 0
        for i in range(m):
            now = 0
            for j in range(n):
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for j in range(n):
            now = 0
            for i in range(m):
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for s in range(m + n - 1):
            now = 0
            for i in range(max(0, s - n + 1), min(m - 1, s) + 1):
                j = s - i
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0
        
        for s in range(-(n - 1), m):
            now = 0
            for i in range(max(s, 0), min(m - 1, s + n - 1) + 1): 
                j = i - s
                if mat[i][j] == 1:
                    now += 1
                    res = max(res, now)
                else:
                    now = 0

        return res
```
