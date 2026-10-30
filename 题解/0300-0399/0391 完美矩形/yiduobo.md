---
title: "391. 完美矩形"
aliases: ["yiduobo的每日leetcode 391.完美矩形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/174835311"
zhihu_id: "174835311"
zhihu_title: "yiduobo的每日leetcode 391.完美矩形"
question_id: "391"
question: "完美矩形"
problem_url: "https://leetcode.cn/problems/perfect-rectangle/"
created: "2020-08-08T23:47:22+08:00"
updated: "2020-08-08T23:47:22+08:00"
upvotes: 0
comments: 0
---

# 391. 完美矩形

> **[yiduobo的每日leetcode 391.完美矩形](https://zhuanlan.zhihu.com/p/174835311) · 知乎 · 2020-08-08 · 赞同 0**
> 力扣：[391. 完美矩形](https://leetcode.cn/problems/perfect-rectangle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

391.完美矩形<https://leetcode-cn.com/problems/perfect-rectangle/>

看上去应该跟计算几何有一定的联系，主要是会用到一些线段相交的判断，不过我在这里采用的是比较trick的方法。

1、如果拼出来的矩形是完美矩形，那么通过一趟扫描找到左下角以及右上角的点之后，可以先判断所有矩形的面积之后是否刚好等于通过左下角和右上角计算出来的面积。

2、如果拼出来的矩形是完美矩形，那么除了完美矩形的四个角只属于某一个矩形之外，其他矩形四个角上的点必然是偶数个矩形共享的。

到了这里，就可以通过一趟扫描，找出左下角以及右上角的点，同时统计矩形的面积和以及每个矩形四个角上的点出现的次数。接下来通过面积以及出现次数进行判断即可。

最后附上python代码：

```python
class Solution(object):
    def isRectangleCover(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: bool
        """

        lx, ly, rx, ry = rectangles[0]
        sum_area = (rx - lx) * (ry - ly)
        
        point_cnt = {}
        point_cnt[(lx, ly)] = 1
        point_cnt[(lx, ry)] = 1
        point_cnt[(rx, ly)] = 1
        point_cnt[(rx, ry)] = 1

        for x1, y1, x2, y2 in rectangles[1:]:
            if x1 < lx or y1 < ly:
                lx = x1
                ly = y1
            if x2 > rx or y2 > ry:
                rx = x2
                ry = y2
            sum_area += (y2 - y1) * (x2 - x1)
            point_cnt[(x1, y1)] = point_cnt.get((x1, y1), 0) + 1
            point_cnt[(x1, y2)] = point_cnt.get((x1, y2), 0) + 1
            point_cnt[(x2, y1)] = point_cnt.get((x2, y1), 0) + 1
            point_cnt[(x2, y2)] = point_cnt.get((x2, y2), 0) + 1

        if (ry - ly) * (rx - lx) != sum_area:
            return False
        if point_cnt.get((lx, ly), 0) != 1 or point_cnt.get((lx, ry), 0) != 1 or point_cnt.get((rx, ly), 0) != 1 or point_cnt.get((rx, ry), 0) != 1:
            return False
        cnt = 0
        for key in point_cnt:
            if point_cnt[key] % 2 == 1:
                cnt += 1
        return cnt == 4
```
