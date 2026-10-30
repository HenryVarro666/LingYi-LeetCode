---
title: "1779. 找到最近的有相同X或Y坐标的点"
aliases: ["yiduobo的每日leetcode 1779.找到最近的有相同X或Y坐标的点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462245585"
zhihu_id: "462245585"
zhihu_title: "yiduobo的每日leetcode 1779.找到最近的有相同X或Y坐标的点"
question_id: "1779"
question: "找到最近的有相同X或Y坐标的点"
problem_url: "https://leetcode.cn/problems/find-nearest-point-that-has-the-same-x-or-y-coordinate/"
created: "2022-01-27T00:18:58+08:00"
updated: "2022-01-27T00:18:59+08:00"
upvotes: 1
comments: 0
---

# 1779. 找到最近的有相同X或Y坐标的点

> **[yiduobo的每日leetcode 1779.找到最近的有相同X或Y坐标的点](https://zhuanlan.zhihu.com/p/462245585) · 知乎 · 2022-01-27 · 赞同 1**
> 力扣：[1779. 找到最近的有相同X或Y坐标的点](https://leetcode.cn/problems/find-nearest-point-that-has-the-same-x-or-y-coordinate/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1779.找到最近的有相同X或Y坐标的点

[力扣](https://leetcode-cn.com/problems/find-nearest-point-that-has-the-same-x-or-y-coordinate/)

比较基础的题目，直接一趟扫描，根据曼哈顿距离的定义计算所有具有相同x或y的点到(x, y)的距离，然后取距离最小且最靠前的点作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def nearestValidPoint(self, x, y, points):
        """
        :type x: int
        :type y: int
        :type points: List[List[int]]
        :rtype: int
        """

        res = -1
        max_dis = None
        for index in range(len(points)):
            px, py = points[index]
            if px == x or py == y:
                if max_dis is None or abs(px - x) + abs(py - y) < max_dis:
                    max_dis = abs(px - x) + abs(py - y)
                    res = index
        
        return res
```
