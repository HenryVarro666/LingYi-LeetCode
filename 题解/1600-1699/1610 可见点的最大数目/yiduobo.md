---
title: "1610. 可见点的最大数目"
aliases: ["yiduobo的每日leetcode 1610.可见点的最大数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/434568451"
zhihu_id: "434568451"
zhihu_title: "yiduobo的每日leetcode 1610.可见点的最大数目"
question_id: "1610"
question: "可见点的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-visible-points/"
created: "2021-11-18T00:12:34+08:00"
updated: "2021-11-18T00:12:34+08:00"
upvotes: 0
comments: 0
---

# 1610. 可见点的最大数目

> **[yiduobo的每日leetcode 1610.可见点的最大数目](https://zhuanlan.zhihu.com/p/434568451) · 知乎 · 2021-11-18 · 赞同 0**
> 力扣：[1610. 可见点的最大数目](https://leetcode.cn/problems/maximum-number-of-visible-points/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1610.可见点的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-visible-points/)

首先判断特殊情况。若某个点与location重叠，那么其必然是可见的，此时应该将答案加一。

接下来考虑一般情况。实际上题目就要要求一个固定角度的扇形区域内最多包含多少个点。

对于任意点而言，由于location是固定不动的，因此如果以location作为原点建立坐标系，该点与location以及坐标系横轴的正半轴形成的夹角，也就是极坐标表示下的极角就可以通过三角函数计算出来。这样一来，题目就变成了找出一些点，这些点极角的最大值和最小值之差小于等于angle。实际上这就是一个环形上的区间覆盖问题，那么将这些极角排序后使用双指针就可以很快解决。

需要特别注意的是，由于这里是环形，因此可能出现起点在四象限，终点在一象限的情况。一种可行的做法是对于每个极角，设为tmp，都额外将一个tmp + 2π加入到极角的数组当中，这样一来就可以解决起点在四象限而终点在一象限的情况了。另外，由于angle小于360°，因此tmp以及tmp + 2π是必然不会被同一个区间覆盖的，因此也不需要担心重复计算的问题。

最后附上python代码：

```python
class Solution(object):
    def visiblePoints(self, points, angle, location):
        """
        :type points: List[List[int]]
        :type angle: int
        :type location: List[int]
        :rtype: int
        """

        angel_list = []
        overlap = 0
        for x, y in points:
            if x == location[0] and y == location[1]:
                overlap += 1
            else:
                tmp = math.atan2(location[1] - y, location[0] - x)
                angel_list.append(tmp)
                angel_list.append(tmp + 2 * math.pi)
        
        angel_list = sorted(angel_list)
        l = r = 0
        res = 0
        while r < len(angel_list):
            while l < r and angel_list[r] - angel_list[l] > angle * math.pi / 180.0:
                l += 1
            res = max(res, r - l + 1)
            r += 1

        return res + overlap
```
