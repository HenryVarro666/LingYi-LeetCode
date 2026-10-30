---
title: "640. 求解方程"
aliases: ["yiduobo的每日leetcode 640.求解方程"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/272853984"
zhihu_id: "272853984"
zhihu_title: "yiduobo的每日leetcode 640.求解方程"
question_id: "640"
question: "求解方程"
problem_url: "https://leetcode.cn/problems/solve-the-equation/"
created: "2020-11-03T22:39:34+08:00"
updated: "2020-11-03T22:39:34+08:00"
upvotes: 1
comments: 0
---

# 640. 求解方程

> **[yiduobo的每日leetcode 640.求解方程](https://zhuanlan.zhihu.com/p/272853984) · 知乎 · 2020-11-03 · 赞同 1**
> 力扣：[640. 求解方程](https://leetcode.cn/problems/solve-the-equation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

640.求解方程

[力扣](https://leetcode-cn.com/problems/solve-the-equation/)

题目保证了这里的方程只有简单的加减操作，而且是一次方程，那么我们可以先分别统计出等号两边的常数项之和以及系数之和。若两边的系数相等，那么根据常数是否相等确定是无穷解还是无解，若系数不相等，则直接除法求解即可。

最后附上python代码：

```python
class Solution(object):
    def solveEquation(self, equation):
        """
        :type equation: str
        :rtype: str
        """

        left, right = equation.split('=')
        a1, b1 = self.get_para(left)
        a2, b2 = self.get_para(right)

        if a1 == a2:
            if b1 == b2:
                return 'Infinite solutions'
            else:
                return 'No solution'
        else:
            return 'x=%d' % ((b2 - b1) / (a1 - a2))

    def get_para(self, s):
        flag = 1
        now = None
        a = b = 0
        x_flag = False
        for char in s:
            if char == '+' or char == '-':
                if now is not None:
                    if x_flag:
                        a += now * flag
                    else:
                        b += now * flag
                
                if char == '+':
                    flag = 1
                else:
                    flag = -1

                x_flag = False
                now = None

            elif char == 'x':
                x_flag = True
                if now is None:
                    now = 1
            
            elif now is None:
                now = int(char)
            else:
                now = now * 10 + int(char)

        if x_flag:
            a += now * flag
        else:
            b += now * flag
        return a, b
```
