---
title: "858. 镜面反射"
aliases: ["yiduobo的每日leetcode 858.镜面反射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348941991"
zhihu_id: "348941991"
zhihu_title: "yiduobo的每日leetcode 858.镜面反射"
question_id: "858"
question: "镜面反射"
problem_url: "https://leetcode.cn/problems/mirror-reflection/"
created: "2021-02-06T23:48:37+08:00"
updated: "2021-02-06T23:48:37+08:00"
upvotes: 1
comments: 0
---

# 858. 镜面反射

> **[yiduobo的每日leetcode 858.镜面反射](https://zhuanlan.zhihu.com/p/348941991) · 知乎 · 2021-02-06 · 赞同 1**
> 力扣：[858. 镜面反射](https://leetcode.cn/problems/mirror-reflection/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

858.镜面反射

[力扣](https://leetcode-cn.com/problems/mirror-reflection/)

拿到题目的第一想法是通过两条直角边的比例和相似三角形来计算每一条的位置，但是这样的复杂度较高，且情况会比较复杂。

既然是物理问题，那么就搞点物理的方法。对于射出的光，我们可以将其速度看成水平方向的速度和竖直方向速度的叠加。设光线与首次接触到东墙的时间为单位时间，那么就有其水平方向的速度为p，而竖直方向的速度为q。

为了让光线射入角落，光线在水平和竖直方向上都必须走完若干个完整的边长，于是有

p \* t \= m \* p

q \* t \= n \* p

通过式子1可知t就等于m，为了让t最小，实际上就是要让m最小。将t \= m带入式子2，可以得到q \* m \= n \* p，此时可以将式子变换为

m / n \= p / q

然后将式子右侧约分为最简分数之后，m和n就分别为分子和分母了。

对于约分操作，则可以先求解p和q的最大公约数gcd，然后让p和q分别除以gcd。

得到m和n之后，观察题目中的图片可以发现：

1、当m为偶数时，光线必然射入角落2

2、当m为奇数、n为偶数时，光线必然射入角落0

3、其他情况下，光线必然射入角落1

于是此时通过m和n的奇偶性就能得出答案了。

最后附上python代码：

```python
class Solution(object):
    def mirrorReflection(self, p, q):
        """
        :type p: int
        :type q: int
        :rtype: int
        """

        if p == q:
            return 1

        x, y = p, q
        while y != 0:
            x, y = y, x % y

        m = p / x
        n = q / x

        if m % 2 == 0:
            return 2
        elif n % 2 == 0:
            return 0
        else:
            return 1
```
