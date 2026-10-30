---
title: "1401. 圆和矩形是否有重叠"
aliases: ["yiduobo的每日leetcode 1401.圆和矩形是否有重叠"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/math", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404767405"
zhihu_id: "404767405"
zhihu_title: "yiduobo的每日leetcode 1401.圆和矩形是否有重叠"
question_id: "1401"
question: "圆和矩形是否有重叠"
problem_url: "https://leetcode.cn/problems/circle-and-rectangle-overlapping/"
difficulty: "Medium"
rating: 1709
created: "2021-08-29T17:16:09+08:00"
updated: "2021-08-29T17:16:09+08:00"
upvotes: 0
comments: 0
---

# 1401. 圆和矩形是否有重叠

> **[yiduobo的每日leetcode 1401.圆和矩形是否有重叠](https://zhuanlan.zhihu.com/p/404767405) · 知乎 · 2021-08-29 · 赞同 0**
> 力扣：[1401. 圆和矩形是否有重叠](https://leetcode.cn/problems/circle-and-rectangle-overlapping/) · Medium · 灵茶山艾府：[找距离圆心最近的点，三行代码（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1401.圆和矩形是否有重叠

[力扣](https://leetcode-cn.com/problems/circle-and-rectangle-overlapping/)

若圆和矩形有重叠，那么必然存在一个点(x, y)，其位于圆的内部，即

(x - x_center) ^ 2 + (y - y_center) ^ 2 \<\= radius \* radius

同时其也需要位于矩形的内部，那么就有

x1 \<\= x \<\= x2

y1 \<\= y \<\= y2

观察第一个不等式，是两个非负项之和小于一个常数，那么我们希望那两个非负项越小越好，也就是当x越接近x_center，y越接近y_center时，不等式越有可能成立。

再考察矩形的那两个不等式，可以分几种情况讨论：

1、若x_center \< x1，我们选择x1作为x时可以使得第一个平方项最小

2、若x_center > x2，我们选择x2作为x时可以使得第一个平方项最小

3、若x1 \<\= x_center \<\= x2，我们可以直接选择x_center作为x，此时可以使得平方项为0

同样地，对于y我们也可以做出类似的选择。选定了x和y之后，只需要检测是否满足圆的不等式即可。

最后附上python代码：

```python
class Solution(object):
    def checkOverlap(self, radius, x_center, y_center, x1, y1, x2, y2):
        """
        :type radius: int
        :type x_center: int
        :type y_center: int
        :type x1: int
        :type y1: int
        :type x2: int
        :type y2: int
        :rtype: bool
        """

        if x2 < x_center:
            x = x2
        elif x1 > x_center:
            x = x1
        else:
            x = x_center

        if y2 < y_center:
            y = y2
        elif y1 > y_center:
            y = y1
        else:
            y = y_center

        return (x - x_center) ** 2 + (y - y_center) ** 2 <= radius * radius
```
