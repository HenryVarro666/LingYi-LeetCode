---
title: "3344. 最大尺寸数组"
aliases: ["yiduobo的每日leetcode 3344.最大尺寸数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25690308198"
zhihu_id: "25690308198"
zhihu_title: "yiduobo的每日leetcode 3344.最大尺寸数组"
question_id: "3344"
question: "最大尺寸数组"
problem_url: "https://leetcode.cn/problems/maximum-sized-array/"
created: "2025-02-23T00:24:13+08:00"
updated: "2025-02-23T00:24:13+08:00"
upvotes: 1
comments: 0
---

# 3344. 最大尺寸数组

> **[yiduobo的每日leetcode 3344.最大尺寸数组](https://zhuanlan.zhihu.com/p/25690308198) · 知乎 · 2025-02-23 · 赞同 1**
> 力扣：[3344. 最大尺寸数组](https://leetcode.cn/problems/maximum-sized-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3344.最大尺寸数组

[3344. 最大尺寸数组 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-sized-array/description/)

题目给出一个正整数s，令A为一个n \* n \* n的三维数组，其中A[i][j][k] \= i \* (j or k)，这里的or是按位或运算。现在要求找出最大的n，满足A中所有元素之和不超过s。

手动跑几个n可以发现A数组元素之和的增长速度还是可以的，因此在这里直接从1开始向上枚举n，在过程中计算数组和now。

接下来考察如何计算数组之和。对于A[i][j][k] \= i \* (j or k)这个式子，括号内的按位或的处理方法不太直观，但是外面的i是很容提出来的。具体来说，不妨先考虑将所有i相同的项求和，那么就有

A[0][0][0] + A[0][0][1] + ... + A[0][1][0] + ... + A[0][n - 1][n - 1] \= 0 \* ((0 | 0) + (0 | 1) + ... + (1 | 0) + ... + (n - 1) | (n - 1))

而

A[1][0][0] + A[1][0][1] + ... + A[1][1][0] + ... + A[1][n - 1][n - 1] \= 1 \* ((0 | 0) + (0 | 1) + ... + (1 | 0) + ... + (n - 1) | (n - 1))

不妨设后面按位或之和的部分为pair[n]，那么就有

A[i][0][0] + A[i][0][1] + ... + A[i][1][0] + ... + A[i][n - 1][n - 1] \= i \* pair[n]

因此A中的元素之和就是

0 \* pair[n] + 1 \* pair[n] + ... + (n - 1) \* pair[n]

化简后就是

pair[n] \* n \* (n - 1) // 2

接下来需要考虑pair[n]应该如何计算。

对于pair[n] \= ((0 | 0) + (0 | 1) + ... + (1 | 0) + ... + (n - 1) | (n - 1))，其在pair[n - 1]的基础上多出了n - 1的部分。更具体的，多出了(0 | n - 1)、(1 | n - 1)、...、(n - 2 | n - 1)、(n - 1 | 0)、(n - 1 | 1)、...、(n - 1 | n - 1)这些项。由于按位或是满足交换律的，那么不妨设t \= (0 | n - 1) + (1 | n - 1) + ... + (n - 1 | n - 1)，那么多出来的这些项就等于t \* 2 - (n - 1)，即pair[n] \= pair[n - 1] + t \* 2 - (n - 1)。

对于t的计算方法目前没有想到特别好的方法，不过在这里使用O(n)的时间暴力遍历计算t在时间复杂度方面也是没有什么问题的。

最后附上python代码：

```python
class Solution(object):
    def maxSizedArray(self, s):
        """
        :type s: int
        :rtype: int
        """
        
        now = 0
        n = 0
        pair = 0
        while now <= s:
            n += 1
            t = 0
            for i in range(n):
                t += (i | (n - 1))
            pair += t + t - (n - 1)
            now = pair * n * (n - 1) // 2

        return n - 1
```
