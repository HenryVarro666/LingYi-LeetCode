---
title: "836. 矩形重叠"
aliases: ["yiduobo的每日leetcode 836.矩形重叠"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/geometry", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346531248"
zhihu_id: "346531248"
zhihu_title: "yiduobo的每日leetcode 836.矩形重叠"
question_id: "836"
question: "矩形重叠"
problem_url: "https://leetcode.cn/problems/rectangle-overlap/"
difficulty: "Easy"
rating: 1443
created: "2021-01-25T13:04:11+08:00"
updated: "2021-01-25T13:04:11+08:00"
upvotes: 0
comments: 0
---

# 836. 矩形重叠

> **[yiduobo的每日leetcode 836.矩形重叠](https://zhuanlan.zhihu.com/p/346531248) · 知乎 · 2021-01-25 · 赞同 0**
> 力扣：[836. 矩形重叠](https://leetcode.cn/problems/rectangle-overlap/) · Easy · 灵茶山艾府：[转化成一维问题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

836.矩形重叠

[力扣](https://leetcode-cn.com/problems/rectangle-overlap/)

之前好像做过一个同样的题目，但是忘记题号了。我的做法是判断矩形在水平和竖直维度上是否重叠，设(A, B)为rec1的左下角坐标，(C, D)为rec1的右上角坐标，(E, F)为rec2的左下角坐标，(G, H)为rec2的右下角坐标：

1、若A等于C，或B等于D，说明rec1此时是没有面积的，因此也不可能重叠，返回false

2、同上，若E等G，或F等于H，返回false

3、若rec1与rec2在水平维度上没有重叠，那么rec1可能在rec2的左侧，此时有C \<\= E，另一种可能是rec1在rec2的右侧，此时有A>\=G。因此如果C\<\=E或者G\<\=A，则返回false。

4、若rec1与rec2在竖直维度上没有重叠，那么rec1可能在rec2的上方，此时有B >\= H，另一种可能是rec1在rec2的下方，此时有D\<\=F。因此如果D\<\=F或者H\<\=B，则返回false。

5、其他情况下，rec1和rec2在水平和竖直维度上都相交，说明二者重叠，返回true。

最后附上python代码：

```python
class Solution(object):
    def isRectangleOverlap(self, rec1, rec2):
        """
        :type rec1: List[int]
        :type rec2: List[int]
        :rtype: bool
        """

        A, B, C, D = rec1
        E, F, G, H = rec2

        if A == C or B == D:
            return False

        if E == G or F == H:
            return False

        if C <= E or G <= A:
            return False
        
        if D <= F or H <= B:
            return False

        return True
```
