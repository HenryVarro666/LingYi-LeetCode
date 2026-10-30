---
title: "1074. 元素和为目标值的子矩阵数量"
aliases: ["yiduobo的每日leetcode 1074.元素和为目标值的子矩阵数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372593754"
zhihu_id: "372593754"
zhihu_title: "yiduobo的每日leetcode 1074.元素和为目标值的子矩阵数量"
question_id: "1074"
question: "元素和为目标值的子矩阵数量"
problem_url: "https://leetcode.cn/problems/number-of-submatrices-that-sum-to-target/"
difficulty: "Hard"
rating: 2189
created: "2021-05-15T19:45:42+08:00"
updated: "2021-05-15T19:45:42+08:00"
upvotes: 0
comments: 0
---

# 1074. 元素和为目标值的子矩阵数量

> **[yiduobo的每日leetcode 1074.元素和为目标值的子矩阵数量](https://zhuanlan.zhihu.com/p/372593754) · 知乎 · 2021-05-15 · 赞同 0**
> 力扣：[1074. 元素和为目标值的子矩阵数量](https://leetcode.cn/problems/number-of-submatrices-that-sum-to-target/) · Hard · 灵茶山艾府：[枚举上下边界，转化成 560 题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1074.元素和为目标值的子矩阵数量

[力扣](https://leetcode-cn.com/problems/number-of-submatrices-that-sum-to-target/)

目前只想出了三次方的做法，但是感觉应该也存在平方log的做法。

对于一个矩阵而言，我们在计算其元素和的时候可以先分别计算出每一行元素之后，然后再将这些行上的和加起来。那么如果我们优先枚举每一行的起始与结束，那么通过行的前缀和，我们就可以高效地计算出当前行在这个列区间之内的和，接下来问题就转化成了给出一个数组，求这个数组区间和等于target的区间数目，那么可以再次利用前缀和，并配合哈希表来解决。

具体做法为：

1、对于每一行，维护当前行的前缀和s_row

2、枚举起始列l和结束列r，再从上往下枚举每一行。设当前行为index，那么此时行的区间和就是s_row[index][r] - s_row[index][l - 1]，将其累加到列前缀和now当中。接下来检测now - target在哈希表中出现的次数，并将这个次数累加到答案当中。最后将now也加入到哈希表中，然后处理下一行即可。当处理完所有行之后，则继续枚举下一组(l, r)直到末尾。

最后附上python代码：

```python
class Solution(object):
    def numSubmatrixSumTarget(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: int
        """

        m = len(matrix)
        n = len(matrix[0])
        s_row = []
        for i in range(m):
            s_row.append([matrix[i][0]])
            for j in range(1, n):
                s_row[-1].append(s_row[-1][-1] + matrix[i][j])
        
        res = 0
        for l in range(n):
            for r in range(l, n):
                f = {0:1}
                s = 0
                for index in range(m):
                    if l == 0:
                        now = s_row[index][r]
                    else:
                        now = s_row[index][r] - s_row[index][l - 1]
                    
                    s += now
                    res += f.get(s - target, 0)
                    f[s] = f.get(s, 0) + 1
        
        return res
```
