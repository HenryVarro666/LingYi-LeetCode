---
title: "3128. 直角三角形"
aliases: ["yiduobo的每日leetcode 3128.直角三角形"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "leetcode/enumeration", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/零-常用枚举技巧", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702084872"
zhihu_id: "702084872"
zhihu_title: "yiduobo的每日leetcode 3128.直角三角形"
question_id: "3128"
question: "直角三角形"
problem_url: "https://leetcode.cn/problems/right-triangles/"
difficulty: "Medium"
rating: 1541
created: "2024-06-06T23:38:30+08:00"
updated: "2024-06-06T23:38:30+08:00"
upvotes: 0
comments: 0
---

# 3128. 直角三角形

> **[yiduobo的每日leetcode 3128.直角三角形](https://zhuanlan.zhihu.com/p/702084872) · 知乎 · 2024-06-06 · 赞同 0**
> 力扣：[3128. 直角三角形](https://leetcode.cn/problems/right-triangles/) · Medium · 灵茶山艾府：[枚举中间+乘法原理（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3128.直角三角形

[. - 力扣（LeetCode）](https://leetcode.cn/problems/right-triangles/description/)

题目给出一个01矩阵，要求计算其中直角三角形数量。直角三角形指的是矩阵中的3个1，其中某个1和另一个1在同一行，和另一个1在同一列，不要求相邻。

根据题目中直角三角形的定义，可以尝试枚举所有直角位置的1，对于位于(i, j)的1，若i这一行存在x个1，j这一列存在y个1，那么从i这一行中另外x - 1个1中任选一个，从j这一列中另外y - 1个1中任选一个，就能构成一个直角三角形，因此以(i, j)为直角位置的1能构成的直角三角形一共有(x - 1) \* (y - 1)个。

根据上面的结论，就可以先遍历整个矩阵，计算每一行和每一列上1的数量，记录在两个数组row和col中。接下来再次遍历整个矩阵，若当前遍历的grid[i][j]为1，那么就将(row[i] - 1) \* (col[j] - 1)累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def numberOfRightTriangles(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        row = [0] * m
        col = [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    row[i] += 1
                    col[j] += 1

        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    res += (row[i] - 1) * (col[j] - 1)
        
        return res
```
