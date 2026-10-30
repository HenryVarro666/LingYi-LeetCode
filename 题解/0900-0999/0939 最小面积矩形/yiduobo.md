---
title: "939. 最小面积矩形"
aliases: ["yiduobo的每日leetcode 939.最小面积矩形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358188569"
zhihu_id: "358188569"
zhihu_title: "yiduobo的每日leetcode 939.最小面积矩形"
question_id: "939"
question: "最小面积矩形"
problem_url: "https://leetcode.cn/problems/minimum-area-rectangle/"
created: "2021-03-18T22:05:57+08:00"
updated: "2021-03-18T22:05:57+08:00"
upvotes: 1
comments: 0
---

# 939. 最小面积矩形

> **[yiduobo的每日leetcode 939.最小面积矩形](https://zhuanlan.zhihu.com/p/358188569) · 知乎 · 2021-03-18 · 赞同 1**
> 力扣：[939. 最小面积矩形](https://leetcode.cn/problems/minimum-area-rectangle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

939.最小面积矩形

[力扣](https://leetcode-cn.com/problems/minimum-area-rectangle/)

注意到题目要求矩形的边平行于x轴和y轴，那么我们如果能确定矩形的左下角和右上角坐标，那么就能推出另外两个角的坐标。

设左下角为(x1, y1)，右上角为(x2, y2)，那么只有当存在两点(x1, y2)以及(x2, y1)时，才可能构成矩形。于是我们可以使用哈希表来储存所有节点的坐标，然后枚举左下角和右上角的坐标，并判断哈希表中是否存在左上角和右下角对应的坐标。若存在，则计算矩形面积并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minAreaRect(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        point_set = set()
        for x, y in points:
            point_set.add(x * 40001 + y)
        
        res = None
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                if x1 == x2 or y1 == y2:
                    continue
                
                if (x2 * 40001 + y1) in point_set and (x1 * 40001 + y2) in point_set:
                    area = abs(x2 - x1) * abs(y2 - y1)
                    if res is None or res > area:
                        res = area
        if res is None:
            res = 0
        return res
```
