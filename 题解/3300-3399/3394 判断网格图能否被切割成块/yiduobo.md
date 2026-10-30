---
title: "3394. 判断网格图能否被切割成块"
aliases: ["yiduobo的每日leetcode 3394.判断网格图能否被切割成块"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30519725736"
zhihu_id: "30519725736"
zhihu_title: "yiduobo的每日leetcode 3394.判断网格图能否被切割成块"
question_id: "3394"
question: "判断网格图能否被切割成块"
problem_url: "https://leetcode.cn/problems/check-if-grid-can-be-cut-into-sections/"
difficulty: "Medium"
rating: 1916
created: "2025-03-16T00:41:11+08:00"
updated: "2025-03-16T00:41:11+08:00"
upvotes: 1
comments: 0
---

# 3394. 判断网格图能否被切割成块

> **[yiduobo的每日leetcode 3394.判断网格图能否被切割成块](https://zhuanlan.zhihu.com/p/30519725736) · 知乎 · 2025-03-16 · 赞同 1**
> 力扣：[3394. 判断网格图能否被切割成块](https://leetcode.cn/problems/check-if-grid-can-be-cut-into-sections/) · Medium · 灵茶山艾府：[合并区间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3394.判断网格图能否被切割成块

[3394. 判断网格图能否被切割成块 - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-grid-can-be-cut-into-sections/)

题目给出一个整数n，表示有一个n \* n的网格图，左边原点位于网格图的左下角。另外给出一个二维坐标数组rectangles，其中rectangles\[i\]的格式为\[start\[x\], start\[y\], end\[x\], end\[y\]\]，(start\[x\], start\[y\])表示矩阵的左下角左边，(end\[x\], end\[y\])表示矩阵的右上角左边。

题目保证矩阵间不会重叠，现在需要判断能否找出两条都水平或者两条都垂直的分割线，可以将网格图分割成三个部分，每个部分中都包含至少一个矩形，且每个矩形都恰好仅属于其中的一个部分。

题目要求判断能否找出两条都水平或者两条都垂直的分割线，也就是说题目中的横纵坐标是互相独立的，于是可以根据所有矩形的横坐标来判断能否找出合法的垂直分割线，同时根据所有矩形的纵坐标来判断能否找出合法的水平分割线。可以发现，问题在这里就转化成了给出一条线段以及若干个区间，问能否在线段上找出两个分割点，将线段分割成三个部分，每个部分中都包含至少一个区间，且每个区间都恰好仅属于其中的一个部分。

由于题目要求每个区间仅属于其中一个部分，这也就意味着相交的区间必须被分配到同一个部分内，于是可以将这些区间按起点排序，然后一趟遍历执行区间合并，若合并完的区间数量大于等于3个，那么就说明可以找到合法的分割点。

最后附上python代码：

```python
class Solution(object):
    def checkValidCuts(self, n, rectangles):
        """
        :type n: int
        :type rectangles: List[List[int]]
        :rtype: bool
        """
        
        x_list = []
        y_list = []
        for x1, y1, x2, y2 in rectangles:
            x_list.append((x1, x2))
            y_list.append((y1, y2))
        
        def check(index_list):
            index_list.sort()
            start, end = index_list[0]
            cnt = 1

            for now_start, now_end in index_list[1:]:
                if now_start < end:
                    end = max(end, now_end)
                else:
                    cnt += 1
                    start, end = now_start, now_end

            return cnt >= 3

        return check(x_list) or check(y_list)
```
