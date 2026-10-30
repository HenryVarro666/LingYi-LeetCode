---
title: "335. 路径交叉"
aliases: ["yiduobo的每日leetcode 335.路径交叉"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161957038"
zhihu_id: "161957038"
zhihu_title: "yiduobo的每日leetcode 335.路径交叉"
question_id: "335"
question: "路径交叉"
problem_url: "https://leetcode.cn/problems/self-crossing/"
created: "2020-07-20T22:01:24+08:00"
updated: "2020-07-20T22:01:24+08:00"
upvotes: 1
comments: 0
---

# 335. 路径交叉

> **[yiduobo的每日leetcode 335.路径交叉](https://zhuanlan.zhihu.com/p/161957038) · 知乎 · 2020-07-20 · 赞同 1**
> 力扣：[335. 路径交叉](https://leetcode.cn/problems/self-crossing/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

335.路径交叉<https://leetcode-cn.com/problems/self-crossing/>

这个题目我是在纸上画出解法的，但是反过来并不知道应该怎么严格推导。

首先，对于任意一些连续的线段，如果旋转坐标轴并平移这些线段的话，都可以看成是从原点开始，按上左下右的顺序画出来的。因此我们对于任意一段连续的x[k]到x[k + m]，都可以看成从原点开始，先往上走x[k]，然后往左走-x[k + 1]，然后往右走x[k + 2]，然后往下走x[k + 3]，依次类推。

不妨设第一次出现相交时，较早画出来的线段是移动x[k]步画出来的。通过上面的结论，我们可以假设这条线段的两端分别为(0，0)，(0，x[k])，那么之后的点分别为

(-x[k + 1]，x[k])

(-x[k + 1]，x[k] - x[k + 2])

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2])

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2] + x[k + 4])

(-x[k + 1] + x[k + 3] - x[k +5]，x[k] - x[k + 2] + x[k + 4])

以此类推。

那么，可能与第一条线段(0，0)，(0，x[k])相交的情况有：

1、第四条线段产生交点，这种情况如样例所示。这条线段的两端为

(-x[k + 1]，x[k] - x[k + 2])

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2])

需要满足第四条线段的两端在y轴两端，且第四条线段的高度在0到x[k]之间，于是有

-x[k + 1] \<\= 0 \<\= -x[k + 1] + x[k + 3]

0 \<\= x[k] - x[k + 2] \<\= x[k]

2、第五条线段产生交点。第五条线段是从下往上的竖直线段，如果与第一条线段相交，那么一定是形成了长方形或者d字型。这条线段的两端为

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2])

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2] + x[k + 4])

需要满足两个点处于y轴上，且高度处在原点的两端，于是有

-x[k + 1] + x[k + 3] \= 0

x[k] - x[k + 2] \<\= 0 \<\= x[k] - x[k + 2] + x[k + 4]

3、第六条线段产生交点。首先，如果第五条线段在y轴的左侧，那么第六条线段不可能与第一条线段相交。若第五条线段在y轴上，第六条线段也不可能与第一条线段相交。那么第五条线段必须在y轴右侧，那么最终会形成某种阶梯的形状，极端条件下则是从阶梯变成长方形。线段的两端为

(-x[k + 1] + x[k + 3]，x[k] - x[k + 2] + x[k + 4])

(-x[k + 1] + x[k + 3] - x[k +5]，x[k] - x[k + 2] + x[k + 4])

需要满足两个端点在y轴的两侧，同时高度位于0到x[k]之间，于是有

-x[k + 1] + x[k + 3] - x[k + 5] \<\= 0 \<\= -x[k + 1] + x[k + 3]

0 \<\= x[k] - x[k + 2] + x[k + 4] \<\= x[k]

4、第七条线段产生交点。可以发现，如果第六条线段不相交，那么第六条线段可能位于第二条线段的上面，平齐或者下面。当位于第二条线段上面时，第七条线段必须位于y轴上才可能与第一条线段相交，而这种情况可以抛去第一条线段，视为与第二条线段相交，成为情况3。当与第二条线段平齐或位于第二条线段下方时，第七条线段不可能与第一条线段相交。更一般的，之后的第m条线段，如果要与第一条线段发生相交，那么必然会先与其它线段相交。设其与线段n相交，那么我们可以抛去线段一至线段n - 1，将线段n视为线段一，那么这次相交又可以归于上面三种情况之一了。

于是只需要一趟扫描，考察第k个点与其前5个点形成的六条线段的相交情况即可。

最后附上python代码：

```python
class Solution(object):
    def isSelfCrossing(self, x):
        """
        :type x: List[int]
        :rtype: bool
        """

        if len(x) <= 3:
            return False

        for index in range(3, len(x)):
            if x[index] >= x[index - 2] and x[index - 3] >= x[index - 1]:
                return True

            if index >= 4:
                if x[index - 1] == x[index - 3] and x[index] - x[index - 2] + x[index - 4] >= 0:
                    return True

            if index >= 5:
                if x[index - 2] >= x[index - 4] and x[index] - x[index - 2] + x[index - 4] >= 0 and x[index - 1] <= x[index - 3] and x[index - 1] - x[index - 3] + x[index - 5] >= 0:
                    return True

        return False
```
