---
title: "1037. 有效的回旋镖"
aliases: ["yiduobo的每日leetcode 1037.有效的回旋镖"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370214691"
zhihu_id: "370214691"
zhihu_title: "yiduobo的每日leetcode 1037.有效的回旋镖"
question_id: "1037"
question: "有效的回旋镖"
problem_url: "https://leetcode.cn/problems/valid-boomerang/"
created: "2021-05-06T21:27:49+08:00"
updated: "2021-05-06T21:27:49+08:00"
upvotes: 0
comments: 0
---

# 1037. 有效的回旋镖

> **[yiduobo的每日leetcode 1037.有效的回旋镖](https://zhuanlan.zhihu.com/p/370214691) · 知乎 · 2021-05-06 · 赞同 0**
> 力扣：[1037. 有效的回旋镖](https://leetcode.cn/problems/valid-boomerang/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1037.有效的回旋镖

[力扣](https://leetcode-cn.com/problems/valid-boomerang/)

按照题目的定义，首先需要判断这三个点是否有重叠的情况。若有，那么返回false。

接下来，可以将p1 -> p0视作向量v1，将p2 -> p0视作向量v2，那么此时就需要判断v1和v2是否共线，那么就可以利用向量的外积。

向量外积的定义为

v1 × v2 \= |v1| \* |v2| \* sin(v1, v2)

那么当v1和v2共线时，二者夹角要么为0度，要么为180度，那么此时sin这一项就等于0。那么当v1和v2的外积等于0时，就说明二者共线。

外积在坐标形式下的计算为x1 \* y2 - x2 \* y1，那么若这个计算结果为0，说明v1和v2共线，返回false，否则返回true。

最后附上python代码：

```python
class Solution(object):
    def isBoomerang(self, points):
        """
        :type points: List[List[int]]
        :rtype: bool
        """

        if points[0][0] == points[1][0] and points[0][1] == points[1][1]:
            return False

        if points[0][0] == points[2][0] and points[0][1] == points[2][1]:
            return False
        
        if points[1][0] == points[2][0] and points[1][1] == points[2][1]:
            return False
        
        x1 = points[1][0] - points[0][0]
        y1 = points[1][1] - points[0][1]

        x2 = points[2][0] - points[0][0]
        y2 = points[2][1] - points[0][1]

        return x1 * y2 - x2 * y1 != 0
```
