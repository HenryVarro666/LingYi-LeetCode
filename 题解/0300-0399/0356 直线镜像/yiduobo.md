---
title: "356. 直线镜像"
aliases: ["yiduobo的每日leetcode 356.直线镜像"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597363920"
zhihu_id: "597363920"
zhihu_title: "yiduobo的每日leetcode 356.直线镜像"
question_id: "356"
question: "直线镜像"
problem_url: "https://leetcode.cn/problems/line-reflection/"
created: "2023-01-07T21:06:23+08:00"
updated: "2023-01-07T21:06:23+08:00"
upvotes: 0
comments: 0
---

# 356. 直线镜像

> **[yiduobo的每日leetcode 356.直线镜像](https://zhuanlan.zhihu.com/p/597363920) · 知乎 · 2023-01-07 · 赞同 0**
> 力扣：[356. 直线镜像](https://leetcode.cn/problems/line-reflection/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

356.直线镜像

[力扣](https://leetcode.cn/problems/line-reflection/)

对于出现同一竖直高度的所有点而言，如果这些点关于某竖直的直线对称，那么这条直线必然位于这些点横坐标的正中心。更具体的，若这些点总数为奇数时，这条直线必然经过中间那个点；若这些点总数为偶数时，这条直线必然经过正中间两点的中点。根据这个结论，就可以求出这条直线的方程，接下来只需要从两侧向中心两个点一组判断是否关于这条直线对称即可。

若不对称，那么直接返回false，否则将这个直线的方程记录下来，并与其他竖直高度上的点求得的直线方程进行比较。若所有的直线方程都一样，那么返回true，否则返回false。

需要特别注意的是，由于题目中的点可能存在重复，因此一开始按照竖直高度聚合点时需要去除掉重复的点。

最后附上python代码：

```python
class Solution(object):
    def isReflected(self, points):
        """
        :type points: List[List[int]]
        :rtype: bool
        """

        points_set = {}
        for x, y in points:
            if y not in points_set:
                points_set[y] = set()
            
            if x not in points_set[y]:
                points_set[y].add(x)
        
        def get(x_list):
            x_list.sort()
            n = len(x_list)
            check_pos = x_list[0] + x_list[-1]
            left, right = 0, n - 1
            while left <= right:
                if x_list[left] + x_list[right] != check_pos:
                    return None
                left += 1
                right -= 1
            return check_pos

        check_x = None
        for y in points_set:
            tmp = get(list(points_set[y]))
            if tmp is None:
                return False
            if check_x is None:
                check_x = tmp
            elif check_x != tmp:
                return False
        
        return True
```
