---
title: "1237. 找出给定方程的正整数解"
aliases: ["yiduobo的每日leetcode 1237.找出给定方程的正整数解"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/two-pointers", "leetcode/interactive", "题单/贪心算法", "题单/贪心算法/七-交互题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384849561"
zhihu_id: "384849561"
zhihu_title: "yiduobo的每日leetcode 1237.找出给定方程的正整数解"
question_id: "1237"
question: "找出给定方程的正整数解"
problem_url: "https://leetcode.cn/problems/find-positive-integer-solution-for-a-given-equation/"
difficulty: "Medium"
created: "2021-06-28T22:21:40+08:00"
updated: "2021-06-28T22:21:40+08:00"
upvotes: 0
comments: 0
---

# 1237. 找出给定方程的正整数解

> **[yiduobo的每日leetcode 1237.找出给定方程的正整数解](https://zhuanlan.zhihu.com/p/384849561) · 知乎 · 2021-06-28 · 赞同 0**
> 力扣：[1237. 找出给定方程的正整数解](https://leetcode.cn/problems/find-positive-integer-solution-for-a-given-equation/) · Medium · 灵茶山艾府：[相向双指针，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1237.找出给定方程的正整数解

[力扣](https://leetcode-cn.com/problems/find-positive-integer-solution-for-a-given-equation/)

首先，对于f[x, y] \< f[x + 1, y]以及f[x, y] \< f[x, y + 1]，如果我们将f的值写成按x和y排列的矩阵的形式，那么就可以得到一个1000 \* 1000的矩阵，而这个矩阵则有某种奇妙的性质。

在这里先写出一个简化版的矩阵，例如3 \* 4的矩阵，那么就是

f[3, 1] \< f[3, 2] \< f[3, 3] \< f[3, 4]

V V V V

f[2, 1] \< f[2, 2] \< f[2, 3] \< f[2, 4]

V V V V

f[1, 1] \< f[1, 2] \< f[1, 3] \< f[1, 4]

这里的单调性是可以加以利用的。例如若我们现在知道了f[2, 2] > z，那么对于以位置(2, 2)为左下角，(3, 4)为右上角的矩阵来说，里面的每个元素都大于f[2, 2]，也就是意味着矩阵中的数都大于z，不可能是要找的答案。

根据上面这个结论，我们可以设计一种算法，即从整个矩阵的右下角(1, 1000)开始执行。每次对于x对应的这一行：

1、我们不断缩小y，直到f[x, y] \<\= z。若当前的f[x, y]等于z，那么将(x, y)加入到答案当中。

2、接下来我们将x加1，考虑更上面的一行。根据上面的结论，以(x, y + 1)为左下角，(1000, 1000)为右上角的矩阵中的数都大于z，因此可以直接省略，于是对于当前行我们可以直接从当前的y开始执行操作1，而不需要从1000重新开始执行。

这样一来，每个x和y都最多从1到1000遍历一次，因此最终得到一个线性的算法。

最后附上python代码：

```python
"""
   This is the custom function interface.
   You should not implement it, or speculate about its implementation
   class CustomFunction:
       # Returns f(x, y) for any given positive integers x and y.
       # Note that f(x, y) is increasing with respect to both x and y.
       # i.e. f(x, y) < f(x + 1, y), f(x, y) < f(x, y + 1)
       def f(self, x, y):
"""

class Solution(object):
    def findSolution(self, customfunction, z):
        """
        :type num: int
        :type z: int
        :rtype: List[List[int]]
        """

        y = 1000
        res = []
        for x in range(1, 1001):
            while y > 0:
                v = customfunction.f(x, y)
                if v <= z:
                    break
                y -= 1
            if y == 0:
                break
            
            if v == z:
                res.append([x, y])
                y -= 1
        
        return res
```
