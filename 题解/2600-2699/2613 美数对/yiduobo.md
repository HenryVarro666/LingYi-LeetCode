---
title: "2613. 美数对"
aliases: ["yiduobo的每日leetcode 2613.美数对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645685915"
zhihu_id: "645685915"
zhihu_title: "yiduobo的每日leetcode 2613.美数对"
question_id: "2613"
question: "美数对"
problem_url: "https://leetcode.cn/problems/beautiful-pairs/"
created: "2023-07-25T04:44:23+08:00"
updated: "2023-07-25T04:44:23+08:00"
upvotes: 0
comments: 0
---

# 2613. 美数对

> **[yiduobo的每日leetcode 2613.美数对](https://zhuanlan.zhihu.com/p/645685915) · 知乎 · 2023-07-25 · 赞同 0**
> 力扣：[2613. 美数对](https://leetcode.cn/problems/beautiful-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2613.美数对

[力扣](https://leetcode.cn/problems/beautiful-pairs/)

经典的平面最近点对问题，不过是在曼哈顿距离下的，处理方法与欧氏距离的处理方法类似，也还是采用分治法。

将所有位置按x为第一优先级，y为第二优先级排序。接下来按数组划分成左右两个部分，并花一条中线。接下来分别递归求解这两个部分中的最近点对距离，取两侧最短距离的最小值dis，然后从中线向左侧和右侧画一个宽度为2 \* dis的矩形，接下来就只考虑矩形内的左右配对就行了。

对于欧式距离而言，可以通过鸽笼原理证明每个左侧点需要考虑的右侧配对点最多只有6个，而对于曼哈顿距离则应该只需要考虑12个点。不过本题的数据比较友好，不需要这个优化就已经够用了。

需要注意的是，再执行分治法时，当点的总数不超过3个时就无法继续向下分，此时需要写if语句暴力求解。另外，本题还需要满足在距离相等时点对的下标字典序最小，因此在计算最短距离时还需要考虑点对的下标。

最后附上python代码：

```python
class Solution(object):
    def beautifulPair(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        def dis(p1, p2):
            return abs(points[p1][0] - points[p2][0]) + abs(points[p1][1] - points[p2][1])

        def smaller(p1, p2, q1, q2):
            d1 = dis(p1, p2)
            d2 = dis(q1, q2)
            if d1 < d2:
                return True
            if d1 > d2:
                return False

            if min(points[p1][2], points[p2][2]) < min(points[q1][2], points[q2][2]):
                return True
            if min(points[p1][2], points[p2][2]) > min(points[q1][2], points[q2][2]):
                return False
            
            return max(points[p1][2], points[p2][2]) < max(points[q1][2], points[q2][2])

        points = []
        for index, (x, y) in enumerate(zip(nums1, nums2)):
            points.append([x, y, index])
        
        points.sort()
        p1 = p2 = None
        for i in range(1, len(points)):
            if points[i][0] == points[i - 1][0] and points[i][1] == points[i - 1][1]:
                if p1 is None or smaller(i, i - 1, p1, p2):
                    p1, p2 = i, i - 1
        
        if p1 is not None:
            return [min(points[p1][2], points[p2][2]), max(points[p1][2], points[p2][2])]

        def calc(left, right):
            if left == right - 1:
                return left, right

            elif left == right - 2:
                if smaller(left, left + 1, left, left + 2):
                    if smaller(left, left + 1, left + 1, left + 2):
                        return left, left + 1
                    else:
                        return left + 1, left + 2
                elif smaller(left, left + 2, left + 1, left + 2):
                    return left, left + 2
                else:
                    return left + 1, left + 2
                    
            else:
                mid = (left + right) / 2
                left_p1, left_p2 = calc(left, mid)
                right_p1, right_p2 = calc(mid + 1, right)
                if smaller(left_p1, left_p2, right_p1, right_p2):
                    p1, p2 = left_p1, left_p2
                else:
                    p1, p2 = right_p1, right_p2

                min_dis = dis(p1, p2)
                mid_x = (points[mid][0] + points[mid + 1][0]) / 2
                for i in range(mid, left - 1, -1):
                    if mid_x - points[i][0] > min_dis:
                        break
                
                    for j in range(mid + 1, right + 1):
                        if points[j][0] - mid_x > min_dis:
                            break
                        
                        if smaller(i, j, p1, p2):
                            p1, p2 = i, j
                            min_dis = dis(p1, p2)

                return p1, p2

        p1, p2 = calc(0, len(points) - 1)
        return [min(points[p1][2], points[p2][2]), max(points[p1][2], points[p2][2])]
```
