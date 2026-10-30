---
title: "2245. 转角路径的乘积中最多能有几个尾随零"
aliases: ["yiduobo的每日leetcode 2245.转角路径的乘积中最多能有几个尾随零"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546071234"
zhihu_id: "546071234"
zhihu_title: "yiduobo的每日leetcode 2245.转角路径的乘积中最多能有几个尾随零"
question_id: "2245"
question: "转角路径的乘积中最多能有几个尾随零"
problem_url: "https://leetcode.cn/problems/maximum-trailing-zeros-in-a-cornered-path/"
difficulty: "Medium"
rating: 2037
created: "2022-07-26T01:36:17+08:00"
updated: "2022-07-26T01:36:17+08:00"
upvotes: 0
comments: 0
---

# 2245. 转角路径的乘积中最多能有几个尾随零

> **[yiduobo的每日leetcode 2245.转角路径的乘积中最多能有几个尾随零](https://zhuanlan.zhihu.com/p/546071234) · 知乎 · 2022-07-26 · 赞同 0**
> 力扣：[2245. 转角路径的乘积中最多能有几个尾随零](https://leetcode.cn/problems/maximum-trailing-zeros-in-a-cornered-path/) · Medium · 灵茶山艾府：[前缀和 + 从上往下/从下往上 + 左拐/右拐（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2245.转角路径的乘积中最多能有几个尾随零

[力扣](https://leetcode.cn/problems/maximum-trailing-zeros-in-a-cornered-path/)

首先，对于乘积尾随0的问题，常见的做法是计算乘数中因子2和因子5的个数，其中较小的一项就是乘积末尾0的数目。于是可以先遍历原始矩阵中的每个数，计算出因子2和因子5的数目。

接下来开始寻找转角路径。对于这类有明确分割点的问题，还是按照通常的做法，枚举这个分割点的位置，即枚举转角这个角的坐标。由于矩阵中没有0，因此数字是越多越好的，那么在确定了角的坐标(x, y)之后，只需从(x, y)到四个边界的两条水平路径和两条竖直路径中选择一横一竖两条组合起来，就得到了一个合法的转角路径。具体来说，水平路径为(x, 0)到(x, y)、(x, y)到(x, n - 1)，竖直路径则是(0, y)到(x, y)、(x, y)到(m - 1, y)。

到了这里，就只需分别计算出每条路径上因子2和因子5的总数，然后就可以枚举所有横竖路径的组合，计算出选择(x, y)作为转角时的最优解了。而对于计算路径上因子2和因子5的总数，则是经典的区间和问题，可以先枚举每一行和每一列，预处理出当前行或列上因子2和因子5的前缀和，然后就可以利用前缀和高效计算出区间和了。

最后附上python代码：

```python
class Solution(object):
    def maxTrailingZeros(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        two = [[0] * n for _ in range(m)]
        five = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                now = grid[i][j]
                while now % 2 == 0:
                    two[i][j] += 1
                    now /= 2
                while now % 5 == 0:
                    five[i][j] += 1
                    now /= 5

        v_two =[[0] * n for _ in range(m)]
        v_five = [[0] * n for _ in range(m)]
        h_two = [[0] * n for _ in range(m)]
        h_five = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    v_two[i][j] = two[i][j]
                    v_five[i][j] = five[i][j]
                else:
                    v_two[i][j] = v_two[i - 1][j] + two[i][j]
                    v_five[i][j] = v_five[i - 1][j] + five[i][j]

                if j == 0:
                    h_two[i][j] = two[i][j]
                    h_five[i][j] = five[i][j]
                else:
                    h_two[i][j] = h_two[i][j - 1] + two[i][j]
                    h_five[i][j] = h_five[i][j - 1] + five[i][j]
        
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    up_two = 0
                    up_five = 0
                else:
                    up_two = v_two[i - 1][j]
                    up_five = v_five[i - 1][j]
                
                down_two = v_two[m - 1][j] - v_two[i][j]
                down_five = v_five[m - 1][j] - v_five[i][j]

                if j == 0:
                    left_two = 0
                    left_five = 0
                else:
                    left_two = h_two[i][j - 1]
                    left_five = h_five[i][j - 1]
                
                right_two = h_two[i][n - 1] - h_two[i][j]
                right_five = h_five[i][n - 1] - h_five[i][j]

                up_left = min(up_two + left_two + two[i][j], up_five + left_five + five[i][j])
                up_right = min(up_two + right_two + two[i][j], up_five + right_five + five[i][j])
                down_left = min(down_two + left_two + two[i][j], down_five + left_five + five[i][j])
                down_right = min(down_two + right_two + two[i][j], down_five + right_five + five[i][j])

                res = max(res, up_left, up_right, down_left, down_right)
        
        return res
```
