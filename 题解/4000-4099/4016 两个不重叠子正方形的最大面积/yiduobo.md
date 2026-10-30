---
title: "4016. 两个不重叠子正方形的最大面积"
aliases: ["yiduobo的每日leetcode 4016.两个不重叠子正方形的最大面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/单调栈", "题单/动态规划/七-其他线性-DP", "题单/单调栈/二-矩形"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2070649488138670280"
zhihu_id: "2070649488138670280"
zhihu_title: "yiduobo的每日leetcode 4016.两个不重叠子正方形的最大面积"
question_id: "4016"
question: "两个不重叠子正方形的最大面积"
problem_url: "https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/"
difficulty: "Medium"
rating: 1959
created: "2026-08-11T23:30:37+08:00"
updated: "2026-08-11T23:30:40+08:00"
upvotes: 2
comments: 0
---

# 4016. 两个不重叠子正方形的最大面积

> **[yiduobo的每日leetcode 4016.两个不重叠子正方形的最大面积](https://zhuanlan.zhihu.com/p/2070649488138670280) · 知乎 · 2026-08-11 · 赞同 2**
> 力扣：[4016. 两个不重叠子正方形的最大面积](https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/) · Medium · 灵茶山艾府：[前后缀分解，转化成 221 题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4016.两个不重叠子正方形的最大面积

<https://leetcode.cn/problems/maximum-area-of-two-non-overlapping-square-submatrices/description/>

题目给出一个大小为m \* n的二维整数矩阵mat，其中的元素值可能是0或者1。

现在要求从中找出两个大小为k \* k的正方形子矩阵，这两个子矩阵不能重叠，同时其中所有的单元格都为1。

问可能得到的最大的k对应的正方形面积是多少。若找不出合法的正方形，则返回0。

首先可以明确的是，若存在边长为k的正方形子矩阵对，那么至少在水平或者竖直方向上存在一条分割线，使得这两个正方形子矩阵分别处于这条分割线的两侧。当然，也可以水平和竖直方向都存在分割线。

若竖直方向上存在一条分割线，也就是这两个正方形呈现左右关系，那么最左侧以及最右侧的，边长为k的全1正方形必然也处于这条分割线的两侧，也就是说这两个正方形也是合法的边长为k的正方形子矩阵对。

同理，若存在水平方向上的分割线，那么最上方以及最下方的边长为k的全1正方形必然也是合法的正方形对。

基于这一点，就可以记录每种不同边长的，最上、最下、最左、最右的全1正方形的右下角下标，接下来从大到小遍历可行的边长，若当前边长对应的最上和最下的正方形在水平方向上不重叠，或者最左和最优的正方形在竖直方向上不重叠，只要满足其一，当前遍历到边长的平方即为最终答案。

到了这里，问题就转化成了如何找出每种边长对应的最靠边的正方形下标。需要注意的是，若(x, y)是边长为k的全1正方形的右下角的坐标，那么其也必然是边长为1到边长为k - 1的全1正方形的右下角坐标，因此在这里只需要计算以(x, y)为右下角的最大的全1正方形的边长f[x][y]，然后使用(x, y)更新边长为f[x][y]的最靠边的正方形下标。接下来在倒序遍历时，对于当前遍历到的边长k，先使用边长k + 1对应的最靠边的下标更新k对应的最靠边的下标，然后计算答案就行了。

最后对于f[x][y]的计算则是经典问题，若mat[x][y]为0，那么f[x][y]就为0，否则f[x][y]就是min(f[x - 1][y], f[x][y - 1], f[x - 1][y - 1]) + 1。

最后附上python代码：

```python
class Solution(object):
    def maxArea(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """
        
        m = len(mat)
        n = len(mat[0])

        ma = min(m, n)
        g = [[None] * 4 for _ in range(ma + 1)]

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    if i == 0 or j == 0:
                        f[i][j] = 1
                    else:
                        f[i][j] = min(f[i - 1][j - 1], f[i][j - 1], f[i - 1][j]) + 1

                    v = f[i][j]
                    top, bottom, left, right = g[v]
                    if top is None or top > i:
                        top = i
                    if bottom is None or bottom < i:
                        bottom = i
                    if left is None or left > j:
                        left = j
                    if right is None or right < j:
                        right = j
                    g[v] = [top, bottom, left, right]
    
        top, bottom, left, right = None, None, None, None
        for v in range(ma, 0, -1):
            if g[v][0] is None:
                continue
            if top is None or top > g[v][0]:
                top = g[v][0]
            if bottom is None or bottom < g[v][1]:
                bottom = g[v][1]
            if left is None or left > g[v][2]:
                left = g[v][2]
            if right is None or right < g[v][3]:
                right = g[v][3]
            
            if top + v <= bottom or left + v <= right:
                return v * v
        
        return 0
```
