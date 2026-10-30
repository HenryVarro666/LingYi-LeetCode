---
title: "452. 用最少数量的箭引爆气球"
aliases: ["yiduobo的每日leetcode 452.用最少数量的箭引爆气球"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/面试经典-150-题", "题单/贪心算法/二-区间贪心", "题单/面试经典-150-题/区间"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/212876062"
zhihu_id: "212876062"
zhihu_title: "yiduobo的每日leetcode 452.用最少数量的箭引爆气球"
question_id: "452"
question: "用最少数量的箭引爆气球"
problem_url: "https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/"
difficulty: "Medium"
rating: 1700
created: "2020-09-02T20:55:32+08:00"
updated: "2020-09-02T20:55:32+08:00"
upvotes: 0
comments: 0
---

# 452. 用最少数量的箭引爆气球

> **[yiduobo的每日leetcode 452.用最少数量的箭引爆气球](https://zhuanlan.zhihu.com/p/212876062) · 知乎 · 2020-09-02 · 赞同 0**
> 力扣：[452. 用最少数量的箭引爆气球](https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/) · Medium · 灵茶山艾府：[教你如何思考这题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

452.用最少数量的箭引爆气球<https://leetcode-cn.com/problems/minimum-number-of-arrows-to-burst-balloons/>

题目说的是气球，但是实际上可以抽象从一维区间，寻找重叠的区间，于是可以按照435题相同的做法来解决（传送门在这里[yiduobo：yiduobo的每日leetcode 435.无重叠区间](https://zhuanlan.zhihu.com/p/199737488)）。

具体实现起来有细小的差别，435题是对于重叠上的区间不进行计数，而这一题则是对重叠不上的区间进行计数。

最后附上python代码：

```python
class Solution(object):
    def findMinArrowShots(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        if not points:
            return 0

        sorted_points = sorted(points, key=lambda d:(d[0], d[1]))
        left, right = sorted_points[0]
        res = 0
        for x, y in sorted_points[1:]:
            if x > right:
                left, right = x, y
                res += 1
            else:
                right = min(right, y)

        return res + 1
```
