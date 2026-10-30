---
title: "LCP 02. 分式化简"
aliases: ["yiduobo的每日leetcode LCP02.分式化简"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569972445"
zhihu_id: "569972445"
zhihu_title: "yiduobo的每日leetcode LCP02.分式化简"
question_id: "LCP 02"
question: "分式化简"
problem_url: "https://leetcode.cn/problems/deep-dark-fraction/"
created: "2022-10-01T17:30:30+08:00"
updated: "2022-10-01T17:30:30+08:00"
upvotes: 0
comments: 0
---

# LCP 02. 分式化简

> **[yiduobo的每日leetcode LCP02.分式化简](https://zhuanlan.zhihu.com/p/569972445) · 知乎 · 2022-10-01 · 赞同 0**
> 力扣：[LCP 02. 分式化简](https://leetcode.cn/problems/deep-dark-fraction/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP02.分式化简

[力扣](https://leetcode.cn/problems/deep-dark-fraction/)

一开始想着手推一下公式化简，但是发现低估了化简的复杂度程度，最后还是只能老老实实从后向前模拟整个计算过程。

由于题目保证了每个cont都非负，且cont的最后一项不为零，那么在整个计算过程中分母都不可能等于零，可以放心大胆地进行操作。

设当前结果的分子为x，分母为y，那么x和y的初始值就是1和cont[-1]。接下来从倒数第二个cont开始向前遍历，对于当前的cont[index]，得到的式子是1 / (cont[index] + x / y)。通分后就是1 / ((y \* cont[index] + x) / y)，那么最终的结果就是y / (y \* cont[index] + x)，也就是将x和y分别迭代成y和y \* cont[index] + x。接下来可以先进行一次约分，即找出最新的x和y的最大公约数，然后让x和y都除以这个最大公约数。

遍历完成后，最后这一轮得到的x和y就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def fraction(self, cont):
        """
        :type cont: List[int]
        :rtype: List[int]
        """

        x = 1
        y = cont[-1]

        for index in range(len(cont) - 2, -1, -1):
            x += y * cont[index]
            x, y = y, x

            a, b = x, y
            while b:
                a, b = b, a % b

            x /= a
            y /= a
        
        return [y, x]
```
