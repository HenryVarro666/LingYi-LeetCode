---
title: "3212. 统计X和Y频数相等的子矩阵"
aliases: ["yiduobo的每日leetcode 3212.统计X和Y频数相等的子矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/708370967"
zhihu_id: "708370967"
zhihu_title: "yiduobo的每日leetcode 3212.统计X和Y频数相等的子矩阵"
question_id: "3212"
question: "统计 X 和 Y 频数相等的子矩阵数量"
problem_url: "https://leetcode.cn/problems/count-submatrices-with-equal-frequency-of-x-and-y/"
difficulty: "Medium"
rating: 1673
created: "2024-07-12T03:25:02+08:00"
updated: "2024-07-12T03:25:02+08:00"
upvotes: 0
comments: 0
---

# 3212. 统计X和Y频数相等的子矩阵

> **[yiduobo的每日leetcode 3212.统计X和Y频数相等的子矩阵](https://zhuanlan.zhihu.com/p/708370967) · 知乎 · 2024-07-12 · 赞同 0**
> 力扣：[3212. 统计 X 和 Y 频数相等的子矩阵数量](https://leetcode.cn/problems/count-submatrices-with-equal-frequency-of-x-and-y/) · Medium · 灵茶山艾府：[两种方法：二维前缀和/维护每列字符个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3212.统计X和Y频数相等的子矩阵

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-submatrices-with-equal-frequency-of-x-and-y/description/)

题目给出一个由'X'、'Y'、'.'三种字符构成的二维矩阵grid，要求找出其中合法子矩阵的数量。合法子矩阵的定义为包含grid[0][0]，且包含至少一个'X'，同时矩阵中'X'的数量等于'Y'的数量的子矩阵。

注意到题目要求的子矩阵必须包含grid[0][0]，那么就说明合法子矩阵必然是前缀矩阵，于是可以使用二维前缀和来求解。令x[i][j]和y[i][j]分别表示以(0, 0)为左上角，(i, j)为右下角的子矩阵中包含的'X'以及'Y'的数目，接下来对于x[i][j]和y[i][j]，方便起见在这里定义两个变量delta_x和delta_y，当grid[i][j]为'X'时delta_x为1，否则为0，当grid[i][j]为'Y'时delta_y为1，否则为0，那么就有：

1、当i和j都为0时

此时只有(0, 0)这一个单元格，因此就有

x[i][j] \= delta_x

y[i][j] \= delta_y

2、当i为0且j不为0时：

此时可以认为x[i][j]和y[i][j]是分别在x[i][j - 1]和y[i][j - 1]的基础上加入了单元格(i, j)，那么就有

x[i][j] \= x[i][j - 1] + delta_x

y[i][j] \= y[i][j - 1] + delta_y

3、当i不为0且j为0时：

与情况2对称，可以认为x[i][j]和y[i][j]是分别在x[i - 1][j]和y[i - 1]的基础上加入了单元格(i, j)，那么就有

x[i][j] \= x[i - 1][j] + delta_x

y[i][j] \= y[i - 1][j] + delta_y

4、当i和j都不为0时：

这种情况下，可以认为x[i][j]和y[i][j]是分别在x[i - 1][j]和y[i - 1][j]的基础上，加入第i行中的所有元素。虽然按照x和y的定义无法直接表达第i行所有元素中'X'和'Y'的数目，但是可以通过x[i][j - 1] - x[i - 1][j - 1]来获取到第i行前j - 1列中'X'的数目，再配合上最后(i, j)，也就是delta_x就可以得到第i行中'X'的数目了。对于'Y'也是同样的方法处理，那么就有

x[i][j] \= x[i - 1][j] + x[i][j - 1] - x[i - 1][j - 1] + delta_x

y[i][j] \= y[i - 1][j] + y[i][j - 1] - y[i - 1][j - 1] + delta_y

得到x[i][j]和y[i][j]后，若当前的x[i][j] > 0且x[i][j] \= y[i][j]，那么就说明以(0, 0)为左上角，(i, j)为右下角的矩阵是合法矩阵，此时更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubmatrices(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        x = [[0] * n for _ in range(m)]
        y = [[0] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                delta_x, delta_y = 0, 0
                if grid[i][j] == 'X':
                    delta_x = 1
                elif grid[i][j] == 'Y':
                    delta_y = 1
                
                if i == 0:
                    if j == 0:
                        x[0][0] = delta_x
                        y[0][0] = delta_y
                    else:
                        x[0][j] = x[0][j - 1] + delta_x
                        y[0][j] = y[0][j - 1] + delta_y
                elif j == 0:
                    x[i][0] = x[i - 1][0] + delta_x
                    y[i][0] = y[i - 1][0] + delta_y
                else:
                    x[i][j] = x[i - 1][j] + x[i][j - 1] - x[i - 1][j - 1] + delta_x
                    y[i][j] = y[i - 1][j] + y[i][j - 1] - y[i - 1][j - 1] + delta_y
                
                if x[i][j] > 0 and x[i][j] == y[i][j]:
                    res += 1
        
        return res
```
