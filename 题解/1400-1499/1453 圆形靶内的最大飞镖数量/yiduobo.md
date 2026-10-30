---
title: "1453. 圆形靶内的最大飞镖数量"
aliases: ["yiduobo 1453.圆形靶内的最大飞镖数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412104865"
zhihu_id: "412104865"
zhihu_title: "yiduobo 1453.圆形靶内的最大飞镖数量"
question_id: "1453"
question: "圆形靶内的最大飞镖数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/"
created: "2021-09-19T22:00:33+08:00"
updated: "2021-09-19T22:00:33+08:00"
upvotes: 0
comments: 0
---

# 1453. 圆形靶内的最大飞镖数量

> **[yiduobo 1453.圆形靶内的最大飞镖数量](https://zhuanlan.zhihu.com/p/412104865) · 知乎 · 2021-09-19 · 赞同 0**
> 力扣：[1453. 圆形靶内的最大飞镖数量](https://leetcode.cn/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1453.圆形靶内的最大飞镖数量

[力扣](https://leetcode-cn.com/problems/maximum-number-of-darts-inside-of-a-circular-dartboard/)

与几何有关的题目总是不太好做的，这里碰到的是还是与圆有关的，涉及到了二元二次方程，就更不好做了。

首先可以明确的是，总是可以通过平移操作，使得某个飞镖是落在靶子边缘上的。于是可以枚举所有的飞镖，设当前飞镖p(x, y)恰好落在靶子的边缘上，那么以(x, y)为圆心，半径为r画一个圆，靶子的中心c就必然落在这个圆上。如果以p为原点，坐标轴与原始坐标轴平行建立新的坐标系，此时线段cp与横轴的夹角就一定在0到360度之间。

对于其他飞镖而言，只有当靶子的圆心c与当前枚举的飞镖p之间的夹角在一定度数之间时，才有可能落在靶子上。换言之，就是对于其他飞镖来说，要么其不可能落在靶子上，要么可以找出一个角度的区间[l, r]，满足当圆心c与p以及新的横轴形成的夹角在l到r之间时，该飞镖也会落在靶子上。

于是这里可以对其他所有飞镖都求出这个夹角区间，接下就只需要找到重叠次数最多的区间，就是飞镖p落在靶子边缘时靶内最多的飞镖数目。

逐个枚举飞镖作为p，然后枚举其他飞镖求出夹角区间，并进行区间合并即可得到最终答案。这里的时间复杂度为O(n^2 \* log(n))。不过这个做法在实现上是比较麻烦的。首先是求解夹角时涉及到了三角函数，可能产生比较严重的精度问题。另一方面是这个区间在0到360度这一段时并不是传统意义上的区间，而是环状区间，在合并时也比较麻烦。

注意到这里区间合并的结果必然由其中一个或两个区间的边界构成，而这个边界代表的就是对应的飞镖也落在靶子边缘上，于是可以采用一个低配的做法，即枚举飞镖p以及这里另一个落在靶子边缘上的飞镖，通过这两点确定圆的圆心。这里二元二次方程应该可以找出两个圆心，这两个圆心关于这两个飞镖的连线是对称的，接下来判断其他飞镖是否在靶子上即可。

设枚举的两个飞镖坐标分别为(x1, y1)以及(x2, y2)，设圆心坐标为(cx, cy)，那么首选飞镖连线的终点位置就是((x1 + x2) / 2, (y1 + y2) / 2)，设为(midx, midy)。

接下来设p_dis \= (x2 - x1)^2 + (y2 - y1)^2，那么sqrt(p_dis)就是两个飞镖之间的距离。若这个距离大于r \* 2，即靶子的直径，那么这两个飞镖不可能同时落在靶子上，也就不存在所谓的圆心需要求解了。接下来考虑圆心存在的情况：

1、（cx, cy)到(midx, midy)的连线垂直与(x1, y1)到(x2, y2)的连线，将其写成向量的形式，即(cx - midx, cy - midy)与(x2 - x1, y2 - y1)垂直，于是有

(cx - midx) \* (x2 - x1) + (cy - midy) \* (y2 - y1) \= 0

2、另外，这里这个直角三角形也满足勾股定理，即(cx, cy)到(midx, midy)的距离的平方加上(midx, midy)到(x1, y1)的距离的平方恰好等于斜边，也就是靶子半径r的平方，即

(cx - midx)^2 + (cy - midy)^2 + (midx - x1)^2 + (midy - y1)^2 \= r^2

对于后面这两个括号中的midx以及midy，则可以使用(x1 + x2) / 2以及(y1 + y2) / 2带入，于是有

(cx - midx)^2 + (cy - midy)^2 + ((x2 - x1)^2 + (y2 - y1)^2) / 4 \= r^2

又由于之前定义的p_dis \= (x2 - x1)^2 + (y2 - y1)^2，这里则可以写成

(cx - midx)^2 + (cy - midy)^2 + p_dis / 4 \= r^2

接下来联立这两个方程求解。

1、先判断特殊情况，当y1 \= y2时：

(cx - midx) \* (x2 - x1) \= 0

由于两个飞镖不会重合，因此这里x1必然不等于x2，于是有cx \= midx，再将其带入勾股定理的方程，就有

(cy - midy)^2 + p_dis / 4 \= r^2

解得cy \= midy ± sqrt(r^2 - p_dis / 4)

2、当y1 !\= y2时，则可以对垂直方程进行变形，即

cy - midy \= -(cx - midx) \* (x2 - x1) / (y2 - y1)

将其带入勾股定理的方程，就有

(cx - midx)^2 + ((x2 - x1)/(y2 - y1))^2 \* (cx - midx)^2 + p_dis / 4 \= r^2

化简之后就有

记得cx \= midx ± sqrt((r^2 - p_dis/4) / (1 + ((x2 - x1)/(y2 - y1))^2))

将解出来的两个cx分别带回垂直方程就可以求出对应的cy了

解得cx和cy后，枚举所有飞镖，判断有多少飞镖满足(x - cx)^2 + (y - cy)^2 \<\= r^2，并更新答案即可。

上面的做法时间复杂度为O(n^3)，相比之前的方法时间效率差了一些，但是实现起来简单很多。不过这里的实现依然出现了开方操作，是很有可能引起精度问题的，因此在最终判断时可以适当给一个精度误差。

```python
class Solution(object):
    def numPoints(self, points, r):
        """
        :type points: List[List[int]]
        :type r: int
        :rtype: int
        """

        n = len(points)
        res = 1
        for i in range(n - 1):
            for j in range(i + 1, n):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                p_dis = (x1 - x2) ** 2 + (y1 - y2) ** 2

                if p_dis > 4 * (r ** 2):
                    continue
                else:
                    mid_x = (x1 + x2) / 2.0
                    mid_y = (y1 + y2) / 2.0
                    a = (x2 - x1) * 1.0
                    b = (y2 - y1) * 1.0
                    if b == 0:
                        center_x1 = mid_x
                        center_y1 = mid_y - sqrt(r ** 2 - p_dis / 4.0)
                        center_x2 = mid_x
                        center_y2 = mid_y + sqrt(r ** 2 - p_dis / 4.0)
                    else:
                        tmp = sqrt((r ** 2 - p_dis / 4.0) / (1 + ((a/b) ** 2)))
                        center_x1 = mid_x - tmp
                        center_y1 = a/b * (mid_x - center_x1) + mid_y
                        center_x2 = mid_x + tmp
                        center_y2 = a/b * (mid_x - center_x2) + mid_y
                    

                    cnt1 = cnt2 = 0
                    for x, y in points:
                        if (x - center_x1) ** 2 + (y - center_y1) ** 2 <= r ** 2 + 0.00001:
                            cnt1 += 1
                        if (x - center_x2) ** 2 + (y - center_y2) ** 2 <= r ** 2 + 0.00001:
                            cnt2 += 1

                    res = max(res, cnt1, cnt2)
        
        return res
```
