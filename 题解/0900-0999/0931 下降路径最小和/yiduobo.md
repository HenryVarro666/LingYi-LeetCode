---
title: "931. 下降路径的最小和"
aliases: ["yiduobo的每日leetcode 931.下降路径的最小和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357082229"
zhihu_id: "357082229"
zhihu_title: "yiduobo的每日leetcode 931.下降路径的最小和"
question_id: "931"
question: "下降路径最小和"
problem_url: "https://leetcode.cn/problems/minimum-falling-path-sum/"
difficulty: "Medium"
rating: 1573
created: "2021-03-14T22:30:43+08:00"
updated: "2021-03-14T22:30:43+08:00"
upvotes: 0
comments: 0
---

# 931. 下降路径的最小和

> **[yiduobo的每日leetcode 931.下降路径的最小和](https://zhuanlan.zhihu.com/p/357082229) · 知乎 · 2021-03-14 · 赞同 0**
> 力扣：[931. 下降路径最小和](https://leetcode.cn/problems/minimum-falling-path-sum/) · Medium · 灵茶山艾府：[从递归到递推，教你一步步思考动态规划！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

931.下降路径的最小和

[力扣](https://leetcode-cn.com/problems/minimum-falling-path-sum/)

经典的动态规划问题。

令f[i][j]表示以第i层第j个数结尾的下降路径最小和是多少，那么对于f[i][j]：

1、在任何情况下，当前层的位置j都可以从上一层的j过来，因此可以初始化f[i][j]为

f[i][j] \= f[i - 1][j] + matrix[i][j]

2、若此时的j > 0，那么当前位置j可以从上一层的j - 1过来，因此有

f[i][j] \= min(f[i][j]，f[i - 1][j - 1] + matrix[i][j]

3、若此时的j \< n - 1，那么当前位置j可以从上一层的j + 1过来，因此有

f[i][j] \= min(f[i][j]，f[i - 1][j + 1] + matrix[i][j]

动态规划结束后，f[n - 1]这一层的最小值即为最终答案。

注意到每一层的状态只与上一层有关，因此也可以使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def minFallingPathSum(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        n = len(matrix)
        f = [[0] * n for _ in range(2)]

        for i in range(n):
            f[0][i] = matrix[0][i]
        
        flag = 0
        for i in range(1, n):
            flag = 1 - flag
            for j in range(n):
                tmp = f[1 - flag][j]
                if j > 0:
                    tmp = min(tmp, f[1 - flag][j - 1])
                if j < n - 1:
                    tmp = min(tmp, f[1 - flag][j + 1])
                f[flag][j] = tmp + matrix[i][j]
        
        return min(f[flag])
```
