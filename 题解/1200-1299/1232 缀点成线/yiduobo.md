---
title: "1232. 缀点成线"
aliases: ["yiduobo的每日leetcode 1232.缀点成线"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384231039"
zhihu_id: "384231039"
zhihu_title: "yiduobo的每日leetcode 1232.缀点成线"
question_id: "1232"
question: "缀点成线"
problem_url: "https://leetcode.cn/problems/check-if-it-is-a-straight-line/"
created: "2021-06-26T16:16:09+08:00"
updated: "2021-06-26T16:16:09+08:00"
upvotes: 1
comments: 0
---

# 1232. 缀点成线

> **[yiduobo的每日leetcode 1232.缀点成线](https://zhuanlan.zhihu.com/p/384231039) · 知乎 · 2021-06-26 · 赞同 1**
> 力扣：[1232. 缀点成线](https://leetcode.cn/problems/check-if-it-is-a-straight-line/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1232.缀点成线

[力扣](https://leetcode-cn.com/problems/check-if-it-is-a-straight-line/)

判断共线是经典的计算几何问题，一般是利用叉积来进行判断。

在这里只需要从第三个点开始向后枚举，判断当前点是否位于与第一个和第二点形成的直线上即可。

最后附上python代码：

```python
class Solution(object):
    def checkStraightLine(self, coordinates):
        """
        :type coordinates: List[List[int]]
        :rtype: bool
        """

        x1 = coordinates[1][0] - coordinates[0][0]
        y1 = coordinates[1][1] - coordinates[0][1]
        for index in range(2, len(coordinates)):
            x2 = coordinates[index][0] - coordinates[0][0]
            y2 = coordinates[index][1] - coordinates[0][1]
            if x1 * y2 != x2 * y1:
                return False
        
        return True
```
