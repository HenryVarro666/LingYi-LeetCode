---
title: "861. 翻转矩阵后的得分"
aliases: ["yiduobo的每日leetcode 861.翻转矩阵后的得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349807921"
zhihu_id: "349807921"
zhihu_title: "yiduobo的每日leetcode 861.翻转矩阵后的得分"
question_id: "861"
question: "翻转矩阵后的得分"
problem_url: "https://leetcode.cn/problems/score-after-flipping-matrix/"
created: "2021-02-07T12:29:39+08:00"
updated: "2021-02-07T12:29:39+08:00"
upvotes: 0
comments: 0
---

# 861. 翻转矩阵后的得分

> **[yiduobo的每日leetcode 861.翻转矩阵后的得分](https://zhuanlan.zhihu.com/p/349807921) · 知乎 · 2021-02-07 · 赞同 0**
> 力扣：[861. 翻转矩阵后的得分](https://leetcode.cn/problems/score-after-flipping-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

861.翻转矩阵后的得分

[力扣](https://leetcode-cn.com/problems/score-after-flipping-matrix/)

由于最终计算得分时，是按照每一行来计算，且左侧为高位，因此我们应当保证每一行的首位为1。那么若某行首位为0，我们有下面两种选择：

1、直接翻转该行

2、翻转首列，但此时首位为1的所有行在翻转后首位变成了0，因此还需要对这些行再进行翻转

可以发现，选择2实际上就等价于执行选择1之后将除首列之外的所有列进行翻转，因此我们可以不考虑选择2，直接先将首列为0的行进行翻转。

完成这一步之后，后续的部分列可能需要进行调整。由于同一列上的1提供的值是一样的，因此对于任意列而言，若其中0的数量比1的数量要多，那么就应该将其翻转。

由于最终需要计算的是二进制值之和，因此所谓的执行翻转操作只需要使用2的幂减去当前行或列的值即可。

最后附上python代码：

```
class Solution(object):
    def matrixScore(self, A):
        """
        :type A: List[List[int]]
        :rtype: int
        """

        m = len(A)
        n = len(A[0])
        pow2 = [1]
        for index in range(1, n):
            pow2.append(pow2[-1] + pow2[-1])
        
        num = []
        for i in range(m):
            num.append(0)
            for j in range(n):
                num[-1] += pow2[j] * A[i][n - j - 1]

            if A[i][0] == 0:
                num[-1] = pow2[-1] + pow2[-1] - 1 - num[-1]
        
        res = sum(num)
        for i in range(n):
            cnt = 0
            for j in range(m):
                if num[j] & pow2[i]:
                    cnt += 1
            if cnt < m - cnt:
                res += (m - cnt - cnt) * pow2[i]
            
        return res
```
