---
title: "1292. 元素和小于等于阈值的正方形的最大边长"
aliases: ["yiduobo的每日leetcode 1292.元素和小于等于阈值的正方形的最大边长"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/prefix-sum", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390124624"
zhihu_id: "390124624"
zhihu_title: "yiduobo的每日leetcode 1292.元素和小于等于阈值的正方形的最大边长"
question_id: "1292"
question: "元素和小于等于阈值的正方形的最大边长"
problem_url: "https://leetcode.cn/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/"
difficulty: "Medium"
rating: 1735
created: "2021-07-15T23:17:14+08:00"
updated: "2021-07-15T23:17:14+08:00"
upvotes: 0
comments: 0
---

# 1292. 元素和小于等于阈值的正方形的最大边长

> **[yiduobo的每日leetcode 1292.元素和小于等于阈值的正方形的最大边长](https://zhuanlan.zhihu.com/p/390124624) · 知乎 · 2021-07-15 · 赞同 0**
> 力扣：[1292. 元素和小于等于阈值的正方形的最大边长](https://leetcode.cn/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/) · Medium · 灵茶山艾府：[无需二分，暴力枚举就是 O(mn)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1292.元素和小于等于阈值的正方形的最大边长

[力扣](https://leetcode-cn.com/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/)

首先，对于这类二维矩阵和的问题，可以使用类似于一维情况下前缀和的思路来求解矩阵的和。具体来说就是对于一个矩阵，设其左上角坐标为(a, b)，右下角坐标为(c, d)，设这个矩阵中的元素之和为s(a, b, c, d)，那么就有

s(a, b, c, d) \= s(0, 0, c, d) - s(0, 0, c, b - 1) - s(0, 0, a - 1, d) + s(0, 0, a - 1, b - 1)

也就是只需要求出所有左上角为(0, 0)的矩形的元素之和，就可以很快计算出其中任意矩形的元素之和了。而对于s(0, 0, a, b)，则有

s(0, 0, a, b) \= s(0, 0, a - 1, b) + s(0, 0, a, b - 1) - s(0, 0, a - 1, b - 1) + mat[a][b]

于是我们可以令s[i][j]表示以(0, 0)为左上角，以(i, j)为右下角的矩形的元素之和，那么可以使用上面的状态转移方程在O(mn)的时间复杂度之内计算出所有的s。

接下来我们需要找到最大的边长。一个可行的思路是遍历每一个格子，二分以这个格子为左上角的矩阵的最大合法边长，然后取其中的最大值作为答案。

不过注意到要求出最大的合法边长，因此并没有必要求出以每一个格子为左上角的最大合法边长，而是在枚举过程中对于当前格子，从当前已知的最大合法边长加1开始进行检测，若合法，那么就更新当前的最大合法边长，否则就跳过并检测下一个格子。这样一来，实际上总共检测的次数就只有mn + res次，其中res为最终的答案。

最后附上python代码：

```python
class Solution(object):
    def maxSideLength(self, mat, threshold):
        """
        :type mat: List[List[int]]
        :type threshold: int
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])
        s = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                s[i][j] = mat[i][j]
                if i == 0:
                    if j == 0:
                        continue
                    else:
                        s[i][j] += s[i][j - 1]
                elif j == 0:
                    s[i][j] += s[i - 1][j]
                else:
                    s[i][j] += s[i][j - 1] + s[i - 1][j] - s[i - 1][j - 1]
        
        f = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                while res < min(m - i, n - j):
                    if i == 0:
                        if j == 0:
                            tmp = s[i + res][j + res]
                        else:
                            tmp = s[i + res][j + res] - s[i + res][j - 1]
                    elif j == 0:
                        tmp = s[i + res][j + res] - s[i - 1][j + res]
                    else:
                        tmp = s[i + res][j + res] - s[i - 1][j + res] - s[i + res][j - 1] + s[i - 1][j - 1]

                    if tmp > threshold:
                        break
                
                    res += 1

        return res
```
