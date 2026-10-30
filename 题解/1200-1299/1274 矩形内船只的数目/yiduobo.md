---
title: "1274. 矩形内船只的数目"
aliases: ["yiduobo的每日leetcode 1274.矩形内船只的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615916080"
zhihu_id: "615916080"
zhihu_title: "yiduobo的每日leetcode 1274.矩形内船只的数目"
question_id: "1274"
question: "矩形内船只的数目"
problem_url: "https://leetcode.cn/problems/number-of-ships-in-a-rectangle/"
created: "2023-03-22T00:00:16+08:00"
updated: "2023-03-22T00:00:16+08:00"
upvotes: 0
comments: 0
---

# 1274. 矩形内船只的数目

> **[yiduobo的每日leetcode 1274.矩形内船只的数目](https://zhuanlan.zhihu.com/p/615916080) · 知乎 · 2023-03-22 · 赞同 0**
> 力扣：[1274. 矩形内船只的数目](https://leetcode.cn/problems/number-of-ships-in-a-rectangle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1274.矩形内船只的数目

[力扣](https://leetcode.cn/problems/number-of-ships-in-a-rectangle/)

非常标准的二分查找问题。对于一个给定区间，通过hasShips检测其中是否存在船只。若不存在，那么就不需要继续向下查找了，反之若存在，则可以根据区间的长宽将其分为上半区和下半区，或者左半区和右半区。接下来只需分别递归求解这两个半区，找出其中船只的数量求和之后返回即可。

对于边界情况，若当前区间的面积为0，那么自然不可能存在船只。另一方面，若当前区间的面积为1，且存在船只，那么必然只存在一艘船。

由于题目的地图大小在1000\*1000之内，因此在20次查找内必然可以精确定位到一艘船，从而保证上面的做法不会超出次数限制。

更进一步的，也存在一些优化的小技巧。最直观的就是对于一个存在船只的区间，若已经知道其某个半区没有船只，那么船只就必然出现在另一个半区，也就是说没必要检测另一个半区中是否存在船只了。

最后附上python代码：

```python
# """
# This is Sea's API interface.
# You should not implement it, or speculate about its implementation
# """
#class Sea(object):
#    def hasShips(self, topRight, bottomLeft):
#        """
#        :type topRight: Point
#		 :type bottomLeft: Point
#        :rtype bool
#        """
#
#class Point(object):
#	def __init__(self, x, y):
#		self.x = x
#		self.y = y

class Solution(object):
    def countShips(self, sea, topRight, bottomLeft):
        """
        :type sea: Sea
        :type topRight: Point
        :type bottomLeft: Point
        :rtype: integer
        """

        def check(sea, topRight, bottomLeft, flag):
            if topRight.x < bottomLeft.x or topRight.y < bottomLeft.y:
                return 0
            
            if not flag and not sea.hasShips(topRight, bottomLeft):
                return 0
            
            if topRight.x == bottomLeft.x and topRight.y == bottomLeft.y:
                return 1
            
            if topRight.x - bottomLeft.x <= topRight.y - bottomLeft.y:
                mid_y = (topRight.y + bottomLeft.y) / 2
                top_cnt = check(sea, topRight, Point(bottomLeft.x, mid_y + 1), False)
                bottom_cnt = check(sea, Point(topRight.x, mid_y), bottomLeft, top_cnt == 0)
                return top_cnt + bottom_cnt
            
            else:
                mid_x = (topRight.x + bottomLeft.x) / 2
                right_cnt = check(sea, topRight, Point(mid_x + 1, bottomLeft.y), False)
                left_cnt = check(sea, Point(mid_x, topRight.y), bottomLeft, right_cnt == 0)
                return left_cnt + right_cnt
        
        return check(sea, topRight, bottomLeft, False)
```
