---
title: "3288. 最长上升路径的长度"
aliases: ["yiduobo的每日leetcode 3288.最长上升路径的长度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/874955536"
zhihu_id: "874955536"
zhihu_title: "yiduobo的每日leetcode 3288.最长上升路径的长度"
question_id: "3288"
question: "最长上升路径的长度"
problem_url: "https://leetcode.cn/problems/length-of-the-longest-increasing-path/"
difficulty: "Hard"
rating: 2450
created: "2024-10-08T21:59:38+08:00"
updated: "2024-10-08T21:59:38+08:00"
upvotes: 1
comments: 0
---

# 3288. 最长上升路径的长度

> **[yiduobo的每日leetcode 3288.最长上升路径的长度](https://zhuanlan.zhihu.com/p/874955536) · 知乎 · 2024-10-08 · 赞同 1**
> 力扣：[3288. 最长上升路径的长度](https://leetcode.cn/problems/length-of-the-longest-increasing-path/) · Hard · 灵茶山艾府：[排序 + LIS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3288.最长上升路径的长度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/length-of-the-longest-increasing-path/description/)

题目给出长度为的n的二维整数数组coordinates，其中coordinates\[i\] \= \[x\[i\], y\[i\]\]表示二维平面中的一个点(x\[i\], y\[i\])。另外给出一个整数k，满足0 \<\= k \< n。

现在要求从coordinates中找出包含coordinates[k]的最长上升路径的长度。上升路径指的是对于一个点序列(x1, y1), (x2, y2), ..., (xm, ym)，所有的1 \<\= i \< m都满足x[i] \< x[i + 1]且y[i] \< y[i + 1]。

由于题目中要找的最长上升序列必须包含coordinates[k]，那么如果coordinates[k]为界切分这个上升序列，可以得到一个由满足x[i] \< x[k]且y[i] \< y[k]的点组成的最长上升序列，以及另一个由满足x[i] > x[k]且y[i] > y[k]的点组成的最长上升序列。于是可以先将对coordinates进行一趟遍历，将满足x[i] \< x[k]且y[i] \< y[k]的点加入到候选集left中，将满足x[i] > x[k]且y[i] > y[k]的点加入到候选集right中，这样一来就拜托了必须包含coordinates[k]的影响，只需专心求解left和right中可以得到的二维最长上升子序列就行了。

对于多维有序问题，一种常见的处理方法是先通过静态排序或者动态的多轮排序来保证某些维度有序，在这个前提下再想办法计算其他维度有序时的状况。

对于本题，可以先对x从小到大进行排序，此时问题就变成了给出一个y序列，要求从中找出最长上升子序列。理由是只要是按顺序找出的y的上升序列，其对应的x也必然是单调递增的。需要特别注意的是，由于这里的子序列中x和y必须严格递增，那么在排序时就必须以x升序，y降序进行排序，这样一来x相同的点的y将会按照逆序排布，才能避免x相同但y递增的情况出现。

最后附上python代码：

```python
class Solution(object):
    def maxPathLength(self, coordinates, k):
        """
        :type coordinates: List[List[int]]
        :type k: int
        :rtype: int
        """

        left = []
        right = []
        for x, y in coordinates:
            if x < coordinates[k][0] and y < coordinates[k][1]:
                left.append([x, y])
            elif x > coordinates[k][0] and y > coordinates[k][1]:
                right.append([x, y])

        def calc(points):
            if not points:
                return 0

            points.sort(key=lambda d:(d[0], -d[1]))
            f = [points[0][1]]
            for x, y in points[1:]:
                if y > f[-1]:
                    f.append(y)
                else:
                    lo = 0
                    hi = len(f) - 1
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if y > f[mid]:
                            lo = mid + 1
                        else:
                            hi = mid
                    f[lo] = y

            return len(f)

        return calc(left) + 1 + calc(right)
```
