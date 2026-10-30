---
title: "853. 车队"
aliases: ["yiduobo的每日leetcode 853.车队"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/sorting", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/三-栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348649206"
zhihu_id: "348649206"
zhihu_title: "yiduobo的每日leetcode 853.车队"
question_id: "853"
question: "车队"
problem_url: "https://leetcode.cn/problems/car-fleet/"
difficulty: "Medium"
rating: 1678
created: "2021-02-02T23:54:10+08:00"
updated: "2021-02-02T23:54:10+08:00"
upvotes: 0
comments: 0
---

# 853. 车队

> **[yiduobo的每日leetcode 853.车队](https://zhuanlan.zhihu.com/p/348649206) · 知乎 · 2021-02-02 · 赞同 0**
> 力扣：[853. 车队](https://leetcode.cn/problems/car-fleet/) · Medium · 灵茶山艾府：[两种方法：正序遍历+栈 / 倒序遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

853.车队

[力扣](https://leetcode-cn.com/problems/car-fleet/)

根据题目描述，首先可以明确的是初始位置最靠前的车必然是某个车队的领头车辆，而对于后续的车辆而言，其要么就是追上前车并驾齐驱，要么就是成为一个新车队的领头车辆。而这里判断的依据则是若该车在有限时间内可以追上前车，那么该车就属于前车的车队，否则该车就是一个新车队的领头车辆。

于是现在的做法为：

1、将所有车按照起始位置从小到大进行排序，并指定起始位置最靠前的车辆为当前车队的起始车辆，将答案初始化为1

2、计算当前车队起始车辆到达重点所需的时间t

3、往后遍历剩余的车辆，若当前车辆在时间t内可以到达终点，那么当前车辆就属于当前车队，继续往后遍历；若当前车辆在时间t内无法到达终点，那么当前车辆就是新车队的领头车辆，此时将答案加1，然后回到步骤2

最后附上python代码：

```python
class Solution(object):
    def carFleet(self, target, position, speed):
        """
        :type target: int
        :type position: List[int]
        :type speed: List[int]
        :rtype: int
        """

        sorted_info = sorted(zip(position, speed), key=lambda d:-d[0])
        now = 0
        res = 0
        while now < len(position):
            res += 1
            now_dis = target - sorted_info[now][0]
            now_v = sorted_info[now][1]
            while now + 1 < len(position):
                next_dis = target - sorted_info[now + 1][0]
                next_v = sorted_info[now + 1][1]
                if now_dis * next_v < next_dis * now_v:
                    break
                now += 1
            
            now += 1
        
        return res
```
