---
title: "3025. 人员站位的方案数I & 3027. 人员站位的方案数II"
aliases: ["yiduobo的每日leetcode 3025.人员站位的方案数I && 3027.人员站位的方案数II", "3025. 人员站位的方案数I", "3027. 人员站位的方案数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧", "题单/常用数据结构/十-CDQ-分治-/-值域分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695126788"
zhihu_id: "695126788"
zhihu_title: "yiduobo的每日leetcode 3025.人员站位的方案数I && 3027.人员站位的方案数II"
question_id: ["3025", "3027"]
question: ["人员站位的方案数 I", "人员站位的方案数 II"]
problem_url: ["https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-i/", "https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2020
created: "2024-04-29T02:31:01+08:00"
updated: "2024-04-29T02:31:01+08:00"
upvotes: 0
comments: 0
---

# 3025. 人员站位的方案数I & 3027. 人员站位的方案数II

> **[yiduobo的每日leetcode 3025.人员站位的方案数I && 3027.人员站位的方案数II](https://zhuanlan.zhihu.com/p/695126788) · 知乎 · 2024-04-29 · 赞同 0**
> 力扣：[3025. 人员站位的方案数 I](https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-i/) · Medium · 灵茶山艾府：[O(n^2) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[3027. 人员站位的方案数 II](https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-ii/) · Hard · 灵茶山艾府：[利用排序简化问题（Python/Java/C++/C/Go/JS/Rust）](../3027%20人员站位的方案数%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3025.人员站位的方案数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-i/description/)

3027.人员站位的方案数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-ii/description/)

两题的题设一样，第二题的数据规模相比更大一点，但是使用O(n^2)的算法依然是没问题的。

对于这类多个维度比较的问题，常规的做法是先对其中一个维度进行排序，然后通过归并排序，对另一个维度进行排序的同时通过某些数据结构来维护其他维度的有序性。但是对于本题，由于允许使用O(n^2)的算法，同时比较的条件也比较松，要求的是不存在符合要求的节点而不是统计符合要求的节点的数目，因此通过排序后暴力枚举就能解决。

具体来说，先对所有节点按横坐标升序，纵坐标降序进行排序，这样做的理由是可以保证对于任意一组j \< k，其要么满足x[j] \< x[k]，要么满足y[j] > y[k]。换言之，对于任意的i \< j \< k，k都不可能出现在以i为左上角，j为右下角的矩形中。

有了这一点，就可以按顺序枚举所有的左上角坐标i，然后从i + 1开始枚举所有的右下角坐标j，此时需要考虑的就是位于i + 1到j - 1之间的点中是否存在某个点位于矩形中。

这些点的横坐标是一定处于矩形范围内，那么需要考虑的就是这些点中是否存在某个点的纵坐标大于j的纵坐标，同时又小于等于i的纵坐标。于是可以使用一个变量ma统计当前遍历过的点的纵坐标中，小于等于i的纵坐标的最大值。这样一来，只需检测j的纵坐标是否大于ma且小于等于i的纵坐标即可。若满足，则需要更新答案，并使用j的纵坐标来更新ma。

最后附上python代码：

```python
class Solution(object):
    def numberOfPairs(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        points.sort(key=lambda d: (d[0], -d[1]))
        res = 0
        for i in range(len(points) - 1):
            ma = -10 ** 9 - 1
            for j in range(i + 1, len(points)):
                if ma < points[j][1] <= points[i][1]:
                    ma = points[j][1]
                    res += 1
        
        return res
```
