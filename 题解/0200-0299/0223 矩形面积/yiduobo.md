---
title: "223. 矩形面积"
aliases: ["yiduobo的每日leetcode 223.矩形面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149067295"
zhihu_id: "149067295"
zhihu_title: "yiduobo的每日leetcode 223.矩形面积"
question_id: "223"
question: "矩形面积"
problem_url: "https://leetcode.cn/problems/rectangle-area/"
created: "2020-06-17T23:39:43+08:00"
updated: "2020-06-17T23:39:43+08:00"
upvotes: 1
comments: 2
---

# 223. 矩形面积

> **[yiduobo的每日leetcode 223.矩形面积](https://zhuanlan.zhihu.com/p/149067295) · 知乎 · 2020-06-17 · 赞同 1**
> 力扣：[223. 矩形面积](https://leetcode.cn/problems/rectangle-area/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

223.矩形面积<https://leetcode-cn.com/problems/rectangle-area/>

题目要求两个长方形叠加后的总面积，这个面积S \= S(方形1) + S(方形2) - S(重合)

计算两个方形的面积很简单，于是现在题目就变成了如何求重叠部分的面积。

不妨设两个方形中左边的那个为R1，右边那个为R2，若两个方形重合的话，一定满足R2的左边在R1中间，即R2的左下角坐标中的横坐标位于R1的两个横坐标之间。如果不满足这个条件，那么重合面积就是0，否则接下来需要判断R2是否整个位于R1中间。这时只需要判断R2右上角的横坐标是否位于R1的两个横坐标中间即可。如果是，那么重合部分的水平边长就是R2的水平边长，否则就需要用R1的右侧横坐标减去R2的左侧横坐标。

对于重合部分的竖直边长也可以通过区分上面的方形和下面的方形，然后判断下面方形的纵坐标与上面方形的纵坐标之间的关系来得出。

以样例说明：

R1的左下角为(A, B): (-3, 0)，右上角为(C, D): (3, 4)

R2的左小角为(E, F): (0, -1)，右上角为(G, H): (9, 2)

R1是位于左侧的那个方形，于是首先判断R2的左边是否在R1中间，即判断E是否在A和C中间，发现E在A和C中间，于是接下来需要判断R2的右边是否也在R1中间，即判断G是否在A和C中间，答案是否定的，于是水平方向的边长就是R1的右横坐标减去R2的左横坐标，即3- 0 \= 3

同样的方法，将两个方形区分上下之后，判断下面的方形是否在上面的里面，可以得到竖直方向的边长为下面方形的上纵坐标减去上面方形的下纵坐标，即2 - 0 \= 2

于是现在得到重合部分的面积为3\* 2 \= 6那么最终的答案就是6 \* 4 + 9 \* 3 - 6\= 45

最后附上python代码，简单起见我一律认为A、B、C、D代表左侧和上面方形的坐标，如果不满足的话则优先交换坐标之后再进行运算：

```python
class Solution(object):
    def computeArea(self, A, B, C, D, E, F, G, H):
        """
        :type A: int
        :type B: int
        :type C: int
        :type D: int
        :type E: int
        :type F: int
        :type G: int
        :type H: int
        :rtype: int
        """

        if A > E:
            A, B, C, D, E, F, G, H = E, F, G, H, A, B, C, D

        if E >= A and E <= C:
            if G < C:
                x = G - E
            else:
                x = C - E
        else:
            x = 0

        if H > D:
            A, B, C, D, E, F, G, H = E, F, G, H, A, B, C, D

        if H <= D and H >= B:
            if F > B:
                y = H - F
            else:
                y = H - B
        else:
            y = 0

        return (C - A) * (D - B) + (G - E) * (H - F) - x * y
```
