---
title: "3951. 维持亮度的最小总能量"
aliases: ["yiduobo的每日leetcode 3951.维持亮度的最小总能量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047457471061562427"
zhihu_id: "2047457471061562427"
zhihu_title: "yiduobo的每日leetcode 3951.维持亮度的最小总能量"
question_id: "3951"
question: "维持亮度的最小总能量"
problem_url: "https://leetcode.cn/problems/minimum-energy-to-maintain-brightness/"
difficulty: "Medium"
rating: 1530
created: "2026-06-08T23:46:57+08:00"
updated: "2026-06-08T23:47:00+08:00"
upvotes: 1
comments: 0
---

# 3951. 维持亮度的最小总能量

> **[yiduobo的每日leetcode 3951.维持亮度的最小总能量](https://zhuanlan.zhihu.com/p/2047457471061562427) · 知乎 · 2026-06-08 · 赞同 1**
> 力扣：[3951. 维持亮度的最小总能量](https://leetcode.cn/problems/minimum-energy-to-maintain-brightness/) · Medium · 灵茶山艾府：[合并区间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3951.维持亮度的最小总能量

<https://leetcode.cn/problems/minimum-energy-to-maintain-brightness/>

题目给出一个整数n，表示有n个灯泡排成一排，下标从0到n - 1。

另外给出一个整数数组brightness和一个二维整数数组intervals，其中intervals\[index\] \= \[start\[index\], end\[index\]\]，表示一个闭时间区间，在该时间区间内必须满足照明需求。

在每个单位时间内，每个灯泡都可以独立地开启或关闭。开启的灯泡会照亮其自身的位置及其相邻的位置。

某个单位时间的总照明度是被照亮的位置数量，每个位置至多只计算一次。

对于一个单位时间，如果它被intervals中至少一个时间区间覆盖，那么这个单位时间内总照明度必须至少为brightness。如果一个单位时间没有被任何时间区间覆盖，那么所有灯泡可以保持关闭。一个单位内开启的一个灯泡消耗1单位的能量。

返回一个整数，表示所需的最小总能量。

首先，由于单个灯泡可以照亮自身及相邻位置，且每个位置至多计算以此，因此在开灯时应该打开1、4、7这写模3余1的位置，也就是说尽量让一个灯泡能cover三个位置。更进一步的，每次照明所需的灯泡数量，就是(brightness - 1) // 3 + 1。

接下来，还需要计算有多少时刻需要开灯。这是一个标准的区间合并问题，只需将区间按照起点排序然后一趟遍历，使用一组变量pre_x, pre_y分别表示当前正在考虑的区间的起点和终点。

接下来对于当前遍历到的区间[x, y]：

若x \<\= pre_y，说明这两个区间重叠。由于区间按照起点排过序，因此pre_x必然小于等于x，也就是说重叠区间的起点依然是pre_x不变，而终点则应该取max(pre_y, y)。

反之，若x > pre_y，同样是由于区间按照起点排过序，因此后续所有区间的起点都必然大于等于x，也必然大于pre_y，也就是说区间[pre_x, pre_y]不会与后续的任何区间重叠，此时[pre_x, pre_y]就形成了独立的区间。接下来，需要将pre_x和pre_y分别置为x和y。

得到合并后的区间之后，只需计算这些区间长度之和，就可以得到照明需要覆盖的总时间，再乘以每次照明所需的灯泡数量即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minEnergy(self, n, brightness, intervals):
        """
        :type n: int
        :type brightness: int
        :type intervals: List[List[int]]
        :rtype: int
        """
        
        intervals.sort()
        pre_x, pre_y = intervals[0]
        res = 0
        for x, y in intervals[1:]:
            if x <= pre_y:
                pre_y = max(y, pre_y)
            else:
                res += pre_y - pre_x + 1
                pre_x, pre_y = x, y
        
        res += pre_y - pre_x + 1
        return res * ((brightness - 1) // 3 + 1)
```
