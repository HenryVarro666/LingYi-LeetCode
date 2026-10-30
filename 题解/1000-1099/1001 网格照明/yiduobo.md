---
title: "1001. 网格照明"
aliases: ["yiduobo的每日leetcode 1001.网格照明"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365862818"
zhihu_id: "365862818"
zhihu_title: "yiduobo的每日leetcode 1001.网格照明"
question_id: "1001"
question: "网格照明"
problem_url: "https://leetcode.cn/problems/grid-illumination/"
created: "2021-04-18T21:28:36+08:00"
updated: "2021-04-18T21:28:36+08:00"
upvotes: 0
comments: 0
---

# 1001. 网格照明

> **[yiduobo的每日leetcode 1001.网格照明](https://zhuanlan.zhihu.com/p/365862818) · 知乎 · 2021-04-18 · 赞同 0**
> 力扣：[1001. 网格照明](https://leetcode.cn/problems/grid-illumination/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1001.网格照明

[力扣](https://leetcode-cn.com/problems/grid-illumination/)

对于位于(x, y)的一盏灯，其可以照亮第x行，第j列，以及所在的两条对角线。对于"/"这条右上到左下的对角线，同一条对角线上的灯都满足x + y相等，而对于"\\"这条左上到右下的对角线，同一条对角线上的灯则满足x - y相等。

于是对于lamps中的灯，我们使用4个哈希表row、col、left、right分别表示行、列、左上到右下的对角线、右上到左下的对角线上分别有多少盏灯是亮的。同时还需要一个set表示当前哪些位置上的灯是开着的。

接下来，对于queries中的灯，首先通过row、col、left、right判断其所在行、列、左上到右下的对角线、右上到左下的对角线上是否有灯亮着，若有则将答案加上1。接下来枚举以当前位置为中心的九宫格的所有位置，并通过set判断对应位置上的灯是否亮着。若亮着，则需要将其关闭，此时需要将其移除set，同时将其所在行、列、左上到右下的对角线、右上到左下的对角线上亮灯的数目减去1。

最后附上python代码：

```python
class Solution(object):
    def gridIllumination(self, N, lamps, queries):
        """
        :type N: int
        :type lamps: List[List[int]]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        lamp_set = set()
        row = {}
        col = {}
        left = {}
        right = {}

        for x, y in lamps:
            if (x, y) not in lamp_set:
                lamp_set.add((x, y))
                self.add(x, y, N, row, col, left, right, 1)
        
        res = []
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        for x, y in queries:
            if row.get(x, 0) > 0 or col.get(y, 0) > 0 or left.get(x - y + N, 0) > 0 or right.get(x + y, 0) > 0:
                res.append(1)
            else:
                res.append(0)
            
            if (x, y) in lamp_set:
                lamp_set.remove((x, y))
                self.add(x, y, N, row, col, left, right, -1)

            for index in range(8):
                xx = x + dx[index]
                yy = y + dy[index]
                if (xx, yy) in lamp_set:
                    lamp_set.remove((xx, yy))
                    self.add(xx, yy, N, row, col, left, right, -1)
            
            

        return res
    
    def add(self, x, y, N, row, col, left, right, delta):
        row[x] = row.get(x, 0) + delta
        col[y] = col.get(y, 0) + delta
        left[x - y + N] = left.get(x - y + N, 0) + delta
        right[x + y] = right.get(x + y, 0) + delta
```
