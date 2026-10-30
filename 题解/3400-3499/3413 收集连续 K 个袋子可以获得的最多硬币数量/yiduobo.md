---
title: "3413. 收集连续K个袋子可以获得的最多硬币数量"
aliases: ["yiduobo的每日leetcode 3413.收集连续K个袋子可以获得的最多硬币数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32250093664"
zhihu_id: "32250093664"
zhihu_title: "yiduobo的每日leetcode 3413.收集连续K个袋子可以获得的最多硬币数量"
question_id: "3413"
question: "收集连续 K 个袋子可以获得的最多硬币数量"
problem_url: "https://leetcode.cn/problems/maximum-coins-from-k-consecutive-bags/"
difficulty: "Medium"
rating: 2374
created: "2025-03-24T00:15:54+08:00"
updated: "2025-03-24T00:15:54+08:00"
upvotes: 1
comments: 0
---

# 3413. 收集连续K个袋子可以获得的最多硬币数量

> **[yiduobo的每日leetcode 3413.收集连续K个袋子可以获得的最多硬币数量](https://zhuanlan.zhihu.com/p/32250093664) · 知乎 · 2025-03-24 · 赞同 1**
> 力扣：[3413. 收集连续 K 个袋子可以获得的最多硬币数量](https://leetcode.cn/problems/maximum-coins-from-k-consecutive-bags/) · Medium · 灵茶山艾府：[滑动窗口滑两遍，附变形题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3413.收集连续K个袋子可以获得的最多硬币数量

[3413. 收集连续 K 个袋子可以获得的最多硬币数量 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-coins-from-k-consecutive-bags/)

题目给出一条无限长的数轴，数轴的每个整点上都有一个袋子，其中某些袋子中装有硬币。接下来给出一个二维数组coins，其中coins\[i\] \= \[l\[i\], r\[i\], c\[i\]\]，表示从坐标l\[i\]到r\[i\]之间的每个袋子中都有c\[i\]枚硬币，其中所有的l\[i\]和r\[i\]在1到10^9之间，且这些区间互不重叠。

现在要求从这条数轴上收集连续K个袋子，问最多可以获得多少硬币。

按题目描述看上去是个经典的滑动窗口问题，不过本题中下标的取值范围特别大，不能直接一格一格地滑动，需要想办法优化。

可以明确的是，对于本题中选出来最终区间，要么起点与某个coins[i]的起点对齐，要么终点与某个coins[i]的终点对齐。因为如果选出的区间两端都没有与某个coins[i]的起点或者终点对齐，那么可以分为两种情况：

1、选出的区间的起点或者终点不在某个coins的区间中：

这种情况下，可以将区间向前或者向后移动使得起点或者终点与某个coins的起点或者终点对齐

2、选出的区间的起点在某个区间coins[i]内，而终点则在另一个区间coins[j]内：

对于这种情况，若coins[i]对应的c[i]更大，则应该将区间的起点向前移动，直到与coins[i]对应的l[i]对齐。这样做的话虽然会随着移动损失掉部分coins[j]对应的c[j]，但是可以获得更多的c[i]，收益是更大的；反之，若coins[j]对应的c[j]更大，则应该将区间的终点向后移动直到与coins[j]对应的r[j]对齐。

根据上面的结论，就只需要判断最终选择的区间以coins中每个l[i]为起点，以及以每个r[i]为终点时可以收集到的硬币数量，取最大值即为最终答案。

于是只需先将coins排序，接下来正序一趟遍历，选择当前遍历到的l[i]作为起点，使用类似滑动窗口的方法计算当前区间的终点可以覆盖住哪些coins，并计算收集到的硬币数，最后再倒序一趟遍历，使用相同的方法枚举r[i]作为终点，然后计算起点可以覆盖住的coinse并计算收集到的硬币数即可。

需要特别注意可能出现仅覆盖住某个coins的部分的情况，这部分的硬币收益也同样需要计算进来，而在区间边界随着枚举移动时，需要将这部分收益去掉，避免重复计算。

最后附上python代码：

```python
class Solution(object):
    def maximumCoins(self, coins, k):
        """
        :type coins: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        n = len(coins)
        coins.sort()
        res = 0

        p = 0
        cnt = 0
        for index in range(n):
            end = coins[index][0] + k - 1
            while p < n and end >= coins[p][1]:
                cnt += (coins[p][1] - coins[p][0] + 1) * coins[p][2]
                p += 1
            
            if p < n and end >= coins[p][0]:
                cnt += (end - coins[p][0] + 1) * coins[p][2]
            
            res = max(res, cnt)

            if index == p:
                cnt -= (end - coins[index][0] + 1) * coins[index][2]
                p += 1
            else:
                cnt -= (coins[index][1] - coins[index][0] + 1) * coins[index][2]
                if p < n and end >= coins[p][0]:
                    cnt -= (end - coins[p][0] + 1) * coins[p][2]

        p = n - 1
        cnt = 0
        for index in range(n - 1, -1, -1):
            start = coins[index][1] - k + 1
            while p >= 0 and start <= coins[p][0]:
                cnt += (coins[p][1] - coins[p][0] + 1) * coins[p][2]
                p -= 1
            
            if p >= 0 and start <= coins[p][1]:
                cnt += (coins[p][1] - start + 1) * coins[p][2]
            
            res = max(res, cnt)

            if index == p:
                cnt -= (coins[index][1] - start + 1) * coins[index][2]
                p -= 1
            else:
                cnt -= (coins[index][1] - coins[index][0] + 1) * coins[index][2]
                if p >= 0 and start <= coins[p][1]:
                    cnt -= (coins[p][1] - start + 1) * coins[p][2]

        return res
```
