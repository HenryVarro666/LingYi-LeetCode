---
title: "4025. 交通灯的最大等待时间"
aliases: ["yiduobo的每日leetcode 4025.交通灯的最大等待时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073547873447317658"
zhihu_id: "2073547873447317658"
zhihu_title: "yiduobo的每日leetcode 4025.交通灯的最大等待时间"
question_id: "4025"
question: "交通灯的最大等待时间"
problem_url: "https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/"
difficulty: "Medium"
created: "2026-08-19T23:21:56+08:00"
updated: "2026-08-19T23:22:00+08:00"
upvotes: 2
comments: 0
---

# 4025. 交通灯的最大等待时间

> **[yiduobo的每日leetcode 4025.交通灯的最大等待时间](https://zhuanlan.zhihu.com/p/2073547873447317658) · 知乎 · 2026-08-19 · 赞同 2**
> 力扣：[4025. 交通灯的最大等待时间](https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4025.交通灯的最大等待时间

<https://leetcode.cn/problems/minimize-the-maximum-waiting-time-at-synchronized-traffic-lights/description/>

题目给出一个整数period和一个整数数组lights，其中lights[index]表示第index个交通信号灯绿灯阶段的持续时间，单位为秒。

在时刻0，所有交通信号灯均从绿灯阶段开始运行。它们的周期是同步的：所有交通信号灯会同时开始新的周期，并且每个周期的持续时间恰好为period秒。因此，第index个信号灯的红灯阶段持续period - lights[index]秒。

另外给出一个整数数组arrivalTime，其中arrivalTime[index]表示第index台汽车到达的时间，单位同样为秒。

每辆汽车都必须被分配到恰好一个交通信号灯，多辆汽车可以被分配到同一个信号灯。绿灯亮起时，任意数量的汽车都可以同时通过同一个交通信号灯。汽车之间不会互相阻挡或者造成延误。

对于分配到第index个信号灯的汽车p，令r \= arrivalTime[p] % period。若r \< lights[index]，那么其等待时间就为0，否则其需要等红灯，具体的等待时间为period - r。

要求找出一种分配方案，使得所有汽车等待时间中的最大值最小。问最大惩罚值最小可能是多少。

由于可以让多辆汽车分配到同一个信号灯，那么为了让等待时间最小，就应该让所有汽车都走绿灯时间持续最长的那个信号灯。于是只需找出lights中的最大值ma，然后对arrivalTime进行一趟遍历，计算对应的r。若r >\= ma，就用等待时间period - r更新答案。

最后附上python代码:

```python
class Solution(object):
    def minPenalty(self, period, lights, arrivalTime):
        """
        :type period: int
        :type lights: List[int]
        :type arrivalTime: List[int]
        :rtype: int
        """
        
        res = 0
        ma = max(lights)
        for t in arrivalTime:
            t %= period
            if t >= ma:
                res = max(res, period - t)
        
        return res
```
