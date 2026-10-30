---
title: "2943. 最大化网格图中正方形空洞的面积"
aliases: ["yiduobo的每日leetcode 2943.最大化网格图中正方形空洞的面积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691394322"
zhihu_id: "691394322"
zhihu_title: "yiduobo的每日leetcode 2943.最大化网格图中正方形空洞的面积"
question_id: "2943"
question: "最大化网格图中正方形空洞的面积"
problem_url: "https://leetcode.cn/problems/maximize-area-of-square-hole-in-grid/"
difficulty: "Medium"
created: "2024-04-08T23:48:27+08:00"
updated: "2024-04-08T23:48:27+08:00"
upvotes: 1
comments: 0
---

# 2943. 最大化网格图中正方形空洞的面积

> **[yiduobo的每日leetcode 2943.最大化网格图中正方形空洞的面积](https://zhuanlan.zhihu.com/p/691394322) · 知乎 · 2024-04-08 · 赞同 1**
> 力扣：[2943. 最大化网格图中正方形空洞的面积](https://leetcode.cn/problems/maximize-area-of-square-hole-in-grid/) · Medium · 灵茶山艾府：[不排序，线性时间复杂度（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2943.最大化网格图中正方形空洞的面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-area-of-square-hole-in-grid/description/)

题目的描述感觉不是太清楚。实际上应该是给出一个(n + 1) \* (m + 1)的网格，网格中的部分横杠和竖杠可以消除，问消除后可以得到的最大空洞正方形。

由于水平和竖直方向的消除互不相关，因此在这里可以分别考虑水平和竖直方向如何进行消除，而最终答案就是消除后水平和竖直方向上连续空白较小值的平方。

在这里以处理横杠为例，竖杠的处理方法可以照搬处理方式。对于横杠，由于原始网格中横杠的存在，那么一旦消除的横杠之间不连续，那么就会被原生的横杠隔断，无法达成题目的要求。换言之，在这里就是要找出可消除横杠中最长的横杠组，于是只需将横杠进行排序，然后一趟遍历找出最长的连续值就行了。

需要特别注意的是，连续的k个横杠可以形成长度为k + 1的空格，因此计算最终面积时需要加上1之后再做平方。

最后附上python代码：

```python
class Solution(object):
    def maximizeSquareHoleArea(self, n, m, hBars, vBars):
        """
        :type n: int
        :type m: int
        :type hBars: List[int]
        :type vBars: List[int]
        :rtype: int
        """

        def calc(bars):
            bars.sort()
            p = 0
            ma = 0
            while p < len(bars):
                start = p
                p += 1
                while p < len(bars) and bars[p] == bars[p - 1] + 1:
                    p += 1
                
                ma = max(ma, p - start)
            
            return ma
            
        return (min(calc(hBars), calc(vBars)) + 1) ** 2
```
