---
title: "3197. 包含所有1的最小矩形面积II"
aliases: ["yiduobo的每日leetcode 3197.包含所有1的最小矩形面积II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/bao-li", "题单/常用数据结构", "题单/动态规划", "题单/贪心算法", "题单/常用数据结构/编程能力强化训练", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707113687"
zhihu_id: "707113687"
zhihu_title: "yiduobo的每日leetcode 3197.包含所有1的最小矩形面积II"
question_id: "3197"
question: "包含所有 1 的最小矩形面积 II"
problem_url: "https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-ii/"
difficulty: "Hard"
rating: 2541
created: "2024-07-05T00:30:39+08:00"
updated: "2024-07-05T00:30:39+08:00"
upvotes: 1
comments: 0
---

# 3197. 包含所有1的最小矩形面积II

> **[yiduobo的每日leetcode 3197.包含所有1的最小矩形面积II](https://zhuanlan.zhihu.com/p/707113687) · 知乎 · 2024-07-05 · 赞同 1**
> 力扣：[3197. 包含所有 1 的最小矩形面积 II](https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-ii/) · Hard · 灵茶山艾府：[两种方法：O((mn)^2) 暴力 / O(mn) 动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3197.包含所有1的最小矩形面积II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-ii/description/)

题目给出一个二维的二进制数组grid，要求使用三个不重叠、面积大于零、且边在水平和竖直方向上的矩形来覆盖住grid中所有的1，要求这三个矩形的面积之和最小，问这个最小面积是多少。

本题是之前3195题的加强版，要求使用三个矩形进行覆盖。

[yiduobo：yiduobo的每日leetcode 3195.包含所有1的最小矩形面积I](https://zhuanlan.zhihu.com/p/706907219)

由于3个矩形互不重叠，那么就可以将grid划分成三个部分，然后让每个矩形负责其中一个部分。对于覆盖单个部分中所有1的最小矩形这个问题，就是3195题了，可以直接套用3195题的处理方法。

接下来是考虑如何划分。划分成三个部分可以认为是先在水平或者竖直方向上进行以此划分，然后对于划分出来的两个部分，再选取其中一个进行水平或者竖直方向上的划分。

注意到全水平和全竖直的划分各有一种情况重复，因此最终只有以下六种划分方法：

```python
|---------------|  |---------------|  |---------------|  |-----------------|  |-----------------|  |-----------------|
|       1       |  |       1       |  |       |       |  |     |     |     |  |     |           |  |           |     |
|---------------|  |---------------|  |   1   |   2   |  |     |     |     |  |     |     2     |  |     1     |     |
|       2       |  |       |       |  |       |       |  |  1  |  2  |  3  |  |  1  |-----------|  |-----------|  3  |
|---------------|  |   2   |   3   |  |---------------|  |     |     |     |  |     |           |  |           |     |
|       3       |  |       |       |  |       3       |  |     |     |     |  |     |     3     |  |     2     |     |
|---------------|  |---------------|  |---------------|  |-----------------|  |-----------------|  |-----------------|
```

划分完成后，使用3195题中的处理方法计算覆盖每个块中所有1的最小矩形面积，累加后更新最终答案即可。

划分的时间复杂度是平方级的，计算单个块中的最小矩形面积也是平方级的，对于本题完全够用了。

最后附上python代码：

```python
class Solution(object):
    def minimumSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        def minArea(x1, y1, x2, y2):
            top, bottom = x2, x1
            left, right = y2, y1
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    if grid[i][j] == 1:
                        top = min(top, i)
                        bottom = max(bottom, i)
                        left = min(left, j)
                        right = max(right, j)

            return max(1, (bottom - top + 1) * (right - left + 1))
        

        m = len(grid)
        n = len(grid[0])
        res = m * n

        for i in range(m - 1):
            for i2 in range(i + 1, m - 1):
                res = min(res, minArea(0, 0, i, n - 1) + minArea(i + 1, 0, i2, n - 1) + minArea(i2 + 1, 0, m - 1, n - 1))

            for j in range(n - 1):
                res = min(res, minArea(0, 0, i, n - 1) + minArea(i + 1, 0, m - 1, j) + minArea(i + 1, j + 1, m - 1, n - 1))
                res = min(res, minArea(i + 1, 0, m - 1, n - 1) + minArea(0, 0, i, j) + minArea(0, j + 1, i, n - 1))
        
        
        for j in range(n - 1):
            for j2 in range(j + 1, n - 1):
                res = min(res, minArea(0, 0, m - 1, j) + minArea(0, j + 1, m - 1, j2) + minArea(0, j2 + 1, m - 1, n - 1))
            
            for i in range(m - 1):
                res = min(res, minArea(0, 0, m - 1, j) + minArea(0, j + 1, i, n - 1) + minArea(i + 1, j + 1, m - 1, n - 1))
                res = min(res, minArea(0, j + 1, m - 1, n - 1) + minArea(0, 0, i, j) + minArea(i + 1, 0, m - 1, j))
        
        return res
```
