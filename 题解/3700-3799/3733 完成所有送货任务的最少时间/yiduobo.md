---
title: "3733. 完成所有送货任务的最少时间"
aliases: ["yiduobo的每日leetcode 3733.完成所有送货任务的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "leetcode/number-theory", "题单/二分算法", "题单/数学算法", "题单/二分算法/二-二分答案", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968508718950883651"
zhihu_id: "1968508718950883651"
zhihu_title: "yiduobo的每日leetcode 3733.完成所有送货任务的最少时间"
question_id: "3733"
question: "完成所有送货任务的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-complete-all-deliveries/"
difficulty: "Medium"
rating: 2513
created: "2025-11-03T19:41:15+08:00"
updated: "2025-11-03T19:41:15+08:00"
upvotes: 2
comments: 0
---

# 3733. 完成所有送货任务的最少时间

> **[yiduobo的每日leetcode 3733.完成所有送货任务的最少时间](https://zhuanlan.zhihu.com/p/1968508718950883651) · 知乎 · 2025-11-03 · 赞同 2**
> 力扣：[3733. 完成所有送货任务的最少时间](https://leetcode.cn/problems/minimum-time-to-complete-all-deliveries/) · Medium · 灵茶山艾府：[两种方法：二分答案 / 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3733.完成所有送货任务的最少时间

[3733. 完成所有送货任务的最少时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-complete-all-deliveries/description/)

题目给出两个大小为2的整数数组d \= [d1, d2]以及r \= [r1, r2]。

其中d表示两架送货无人机需要完成送货的任务的数量，即第一台无人机需要完成d1次送货任务，第二台无人机需要完成d2次送货任务。每次送货任务需要花费一小时，且每个小时只有一台无人机可以送货。

r则表示对应的无人机必须每隔特定时间就充电一小时，即第一台无人机需要每r1小时就充电一小时，第二台无人机需要每r2小时就充电一小时。

问完成所有送货任务所需的最小总时间。

首先，由于无人机有充电的需求，那么可以使用r1与r2的最大公倍数l作为一个计算周期来进行分析。这样做的好处是在一个周期内，不会出现两台无人机需要同时充电的情况，那么在这个周期内的时间段可以分为三种，分别为只有第一台无人机可以送货，只有第二台无人机可以送货，以及两台无人机都可以送货。

分别记一个周期内的这三种时间段的数量为o1、o2、both，那么就有

o1 \= (l - 1) // r2，也就是第二台无人机所有充电的时间，都只有第一台无人机可以送货

o2 \= (l - 1) // r1，与上面对称，所有第一台无人机充电的时间，都只有第二台无人机可以送货

both \= l - 1 - o1 - o2，剩下的时间，就是两台都可以送货的时间

接下来需要想办法计算最少需要多少个小时才能完成送货。通过上面的分析其实可以得到形式不太好的方程，但是不太好计算，于是可以改成二分答案的方式，将问题转化为判定问题。

二分答案的成立是很明显的，因为时间越长，就越可能完成任务。二分的下界显然为1，但是上界不太好计算。我在这里给了一个比较大的上界，假设一个周期内只能完成一次送货任务，那么就需要(d1 + d2) \* l个小时，使用这个值作为二分的上界。

对于二分到的mid，可以明确的是两台无人机都应该优先使用只有这台无人机可以送货的时段，不够的时候再通过占用两台都可以送货的时段来进行补充。于是可以先通过mid // l计算出经过的周期数rnd，以及剩余的时间t \= mid % l。

在这rnd个周期内，不占用两台都可以送货的时间段的话，第一台无人机最多可以完成rnd \* o1次送货任务，再加上剩余时间t内还可以完成t // r2次，一共可以完成rnd \* o1 + t // r2次任务。若这个值小于d1，那么就还需要占用d1 - rnd \* o1 - t // r2次共用的时间段，反之则无需占用，可以将其写成max(d1 - rnd \* o1 - t // r2, 0)。同样的，第二台无人机需要的为max(d2 - rnd \* o2 - t // r1, 0)。

记这两个值分别为need_both1以及need_both2，若这两个值之和小于等于所有的两台都可以送货的时间段，也就是这rnd轮中的rnd \* both再加上剩余时间内的t - t // r1 - t // r2，那么就说明在mid的时间内可以完成所有的送货任务，调整二分上界为mid，否则调整二分的下界为mid + 1即可。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, d, r):
        """
        :type d: List[int]
        :type r: List[int]
        :rtype: int
        """
        
        x, y = r
        l = x * y
        while y:
            x, y = y, x % y
        
        l //= x

        o = [(l - 1) // r[1], (l - 1) // r[0]]
        both = l - 1 - o[0] - o[1]
        
        left = 1
        right = (d[0] + d[1]) * l
        while left < right:
            mid = (left + right) // 2
            rnd = mid // l
            t = mid % l
            need_both = [max(0, d[0] - o[0] * rnd - t // r[1]), max(0, d[1] - o[1] * rnd - t // r[0])]
            if need_both[0] + need_both[1] <= both * rnd + t - t // r[1] - t // r[0]:
                right = mid
            else:
                left = mid + 1
        
        return left
```
