---
title: "3111. 覆盖所有点的最少矩形数目"
aliases: ["yiduobo的每日leetcode 3111.覆盖所有点的最少矩形数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700813360"
zhihu_id: "700813360"
zhihu_title: "yiduobo的每日leetcode 3111.覆盖所有点的最少矩形数目"
question_id: "3111"
question: "覆盖所有点的最少矩形数目"
problem_url: "https://leetcode.cn/problems/minimum-rectangles-to-cover-points/"
difficulty: "Medium"
rating: 1401
created: "2024-05-30T23:44:02+08:00"
updated: "2024-05-30T23:44:02+08:00"
upvotes: 0
comments: 0
---

# 3111. 覆盖所有点的最少矩形数目

> **[yiduobo的每日leetcode 3111.覆盖所有点的最少矩形数目](https://zhuanlan.zhihu.com/p/700813360) · 知乎 · 2024-05-30 · 赞同 0**
> 力扣：[3111. 覆盖所有点的最少矩形数目](https://leetcode.cn/problems/minimum-rectangles-to-cover-points/) · Medium · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3111.覆盖所有点的最少矩形数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-rectangles-to-cover-points/description/)

题目给出二维平面上的一些点，要求使用一些水平方向上的宽度不超过w的矩形来覆盖这些点，问至少要多少个矩形才能覆盖所有点。

由于矩形没有高度限制，因此在这里实际上就是给出一条直线上的一些点，使用长为w的线段来覆盖这些点，问至少需要多少条线段。

由于需要覆盖所有点，因此最左侧的线段的左端点就应该放置在最左侧点所处的位置上，此时就可以计算有哪些点被这条线段覆盖，接下来对于剩下的点，只需重复此过程，每次找出剩下点中最左侧的那一个，将下一个矩形的左边界放置在这个位置即可。为了可以方便地计算有哪些点被当前线段覆盖，以及剩下点中最左侧的是哪个，在这里可以先将所有点从小到大排序，这样一来就可以使用双指针迭代的方法来放置所有线段了。

最后附上python代码：

```python
class Solution(object):
    def minRectanglesToCoverPoints(self, points, w):
        """
        :type points: List[List[int]]
        :type w: int
        :rtype: int
        """

        points.sort()
        p = 0
        res = 0
        while p < len(points):
            q = p + 1
            while q < len(points) and points[q][0] - points[p][0] <= w:
                q += 1
            
            res += 1
            p = q
        
        return res
```
