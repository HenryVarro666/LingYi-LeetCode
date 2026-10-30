---
title: "593. 有效的正方形"
aliases: ["yiduobo的每日leetcode 593.有效的正方形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268202601"
zhihu_id: "268202601"
zhihu_title: "yiduobo的每日leetcode 593.有效的正方形"
question_id: "593"
question: "有效的正方形"
problem_url: "https://leetcode.cn/problems/valid-square/"
created: "2020-10-23T22:39:37+08:00"
updated: "2020-10-23T22:39:37+08:00"
upvotes: 0
comments: 0
---

# 593. 有效的正方形

> **[yiduobo的每日leetcode 593.有效的正方形](https://zhuanlan.zhihu.com/p/268202601) · 知乎 · 2020-10-23 · 赞同 0**
> 力扣：[593. 有效的正方形](https://leetcode.cn/problems/valid-square/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

593.有效的正方形<https://leetcode-cn.com/problems/valid-square/>

判断正方形就是要求四条边的长度相等，且形成的是四个直角。在这里，必须要判断直角，因为正方形可能是斜着放的，此时不能简单通过水平线或者垂直线来进行判断。

首先，若存在两点重合，那么必然无法形成正方形，直接返回false。

接下来，考察四个点的顺序。理论上来说，应该有4\*3\*2\*1\=24种可能的情况，但是点的先后其实并不重要，例如p1、p2、p3、p4这种情况实际上与p2、p3、p4、p1这种情况完全等价。同时，顺时针和逆时针也完全等价，例如p1、p2、p3、p4这种情况实际上与p4、p3、p2、p1这种情况完全等价。

因此，实际上最后只有三种情况，分别为：

p1、p2、p3、p4

p1、p2、p4、p3

p1、p3、p2、p4

最后分别考察这三种顺序下四个点能否形成正方形。

边长的判断比较简单，而直角的判断则可以运用之前凸包那一题用过的向量差积。差积为0时，两向量垂直。

最后附上python代码：

```python
class Solution(object):
    def validSquare(self, p1, p2, p3, p4):
        """
        :type p1: List[int]
        :type p2: List[int]
        :type p3: List[int]
        :type p4: List[int]
        :rtype: bool
        """

        if p1 == p2 or p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4 or p3 == p4:
            return False

        return self.check(p1, p2, p3, p4) or self.check(p1, p2, p4, p3) or self.check(p1, p3, p2, p4)

    def check(self, p1, p2, p3, p4):
        l1 = [p1[0] - p2[0], p1[1] - p2[1]]
        l2 = [p2[0] - p3[0], p2[1] - p3[1]]
        l3 = [p3[0] - p4[0], p3[1] - p4[1]]
        l4 = [p4[0] - p1[0], p4[1] - p1[1]]

        len1 = l1[0] ** 2 + l1[1] ** 2
        len2 = l2[0] ** 2 + l2[1] ** 2
        len3 = l3[0] ** 2 + l3[1] ** 2
        len4 = l4[0] ** 2 + l4[1] ** 2
        if len1 == len2 and len1 == len3 and len1 == len4:
            if l1[0] * l2[0] + l1[1] * l2[1] == 0 and l2[0] * l3[0] + l2[1] * l3[1] == 0 and l3[0] * l4[0] + l3[1] * l4[1] == 0:
                return True

        return False
```
