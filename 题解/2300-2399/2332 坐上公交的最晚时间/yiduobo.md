---
title: "2332. 坐上公交的最晚时间"
aliases: ["yiduobo的每日leetcode 2332.坐上公交的最晚时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558581461"
zhihu_id: "558581461"
zhihu_title: "yiduobo的每日leetcode 2332.坐上公交的最晚时间"
question_id: "2332"
question: "坐上公交的最晚时间"
problem_url: "https://leetcode.cn/problems/the-latest-time-to-catch-a-bus/"
difficulty: "Medium"
rating: 1841
created: "2022-08-27T22:50:39+08:00"
updated: "2022-08-27T22:50:39+08:00"
upvotes: 0
comments: 0
---

# 2332. 坐上公交的最晚时间

> **[yiduobo的每日leetcode 2332.坐上公交的最晚时间](https://zhuanlan.zhihu.com/p/558581461) · 知乎 · 2022-08-27 · 赞同 0**
> 力扣：[2332. 坐上公交的最晚时间](https://leetcode.cn/problems/the-latest-time-to-catch-a-bus/) · Medium · 灵茶山艾府：[插队（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2332.坐上公交的最晚时间

[力扣](https://leetcode.cn/problems/the-latest-time-to-catch-a-bus/)

首先可以对车和人的时间分别进行排序，然后使用类似二路归并的方式计算出每个乘客的乘车情况。

接下来，若最后一趟车没有坐满，那么最理想的情况就是在最后一趟车开车的时间点到达。若最后一趟车坐满了，那么最理想的情况则是恰好把最后一趟车上的最后一名乘客挤下去，也就是在该乘客到达时间点的前一时刻到达。

上面描述的是理想的到达时间，但是这个时间点已经被其他乘客占住了，因此若当前时间点被使用时，需要继续向前考虑上一时刻，直到当前时间点没有被其他乘客使用为止。由于乘客到达的时间点大于等于2，因此必然可以找出一个没有被其他乘客使用的时间点。

最后附上python代码：

```python
class Solution(object):
    def latestTimeCatchTheBus(self, buses, passengers, capacity):
        """
        :type buses: List[int]
        :type passengers: List[int]
        :type capacity: int
        :rtype: int
        """

        buses.sort()
        passengers.sort()

        passengers_set = set(passengers)

        p = 0
        for t in buses:
            cnt = 0
            while p < len(passengers) and cnt < capacity and passengers[p] <= t:
                cnt += 1
                p += 1

        if cnt < capacity:
            res = buses[-1]
        else:
            res = passengers[p - 1] - 1
        
        while res in passengers_set:
            res -= 1
        
        return res
```
