---
title: "1701. 平均等待时间"
aliases: ["yiduobo的每日leetcode 1701.平均等待时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/448278916"
zhihu_id: "448278916"
zhihu_title: "yiduobo的每日leetcode 1701.平均等待时间"
question_id: "1701"
question: "平均等待时间"
problem_url: "https://leetcode.cn/problems/average-waiting-time/"
created: "2021-12-21T22:54:13+08:00"
updated: "2021-12-21T22:54:13+08:00"
upvotes: 0
comments: 0
---

# 1701. 平均等待时间

> **[yiduobo的每日leetcode 1701.平均等待时间](https://zhuanlan.zhihu.com/p/448278916) · 知乎 · 2021-12-21 · 赞同 0**
> 力扣：[1701. 平均等待时间](https://leetcode.cn/problems/average-waiting-time/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1701.平均等待时间

[力扣](https://leetcode-cn.com/problems/average-waiting-time/)

由于题目要求必须按照订单的先后顺序制作，同时只有当顾客到达时才会产生新的订单，因此在这里只能不存在什么规划算法，只需要老老实实模拟就行了。

使用一个变量now记录完成上一个顾客订单后的时间点，然后遍历每个顾客。对于第index个顾客，设其是在arr[index]到达，订单所需时间为time[index]：

1、若now > arr[index]，那么这位顾客需要先等到now这个时间点，然后该顾客的订单才会被制作，一共需要等待now - arr[index]的排队时间以及time[index]的制作时间，因此该顾客等待的时间就是now - arr[index] + time[index]。将这个值累加到总时间，然后将now更新为now + time[index]

2、若now \< arr[index]，那么这位顾客到达后订单会立即开始制作，该顾客只需要等待time[index]的制作时间，将这个值累加到总时间。与此对应的，需要将now更新为arr[index] + time[index]

遍历完成后，对总时长求平均即可

最后附上python代码：

```python
class Solution(object):
    def averageWaitingTime(self, customers):
        """
        :type customers: List[List[int]]
        :rtype: float
        """

        now = 0
        res = 0
        for arr, time in customers:
            if now > arr:
                res += now - arr + time
                now += time
            else:
                res += time
                now = arr + time

        return res * 1.0 / len(customers)
```
