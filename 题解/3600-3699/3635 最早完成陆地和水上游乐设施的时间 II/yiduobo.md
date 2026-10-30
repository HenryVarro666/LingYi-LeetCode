---
title: "3633. 最早完成陆地和水上游乐设施的时间I & 3635. 最早完成陆地和水上游乐设施的时间II"
aliases: ["yiduobo的每日leetcode 3633.最早完成陆地和水上游乐设施的时间I && 3635.最早完成陆地和水上游乐设施的时间II", "3633. 最早完成陆地和水上游乐设施的时间I", "3635. 最早完成陆地和水上游乐设施的时间II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1946705235293737548"
zhihu_id: "1946705235293737548"
zhihu_title: "yiduobo的每日leetcode 3633.最早完成陆地和水上游乐设施的时间I && 3635.最早完成陆地和水上游乐设施的时间II"
question_id: ["3633", "3635"]
question: ["最早完成陆地和水上游乐设施的时间 I", "最早完成陆地和水上游乐设施的时间 II"]
problem_url: ["https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-i/", "https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1870
created: "2025-09-04T02:21:49+08:00"
updated: "2025-09-04T02:21:49+08:00"
upvotes: 0
comments: 0
---

# 3633. 最早完成陆地和水上游乐设施的时间I & 3635. 最早完成陆地和水上游乐设施的时间II

> **[yiduobo的每日leetcode 3633.最早完成陆地和水上游乐设施的时间I && 3635.最早完成陆地和水上游乐设施的时间II](https://zhuanlan.zhihu.com/p/1946705235293737548) · 知乎 · 2025-09-04 · 赞同 0**
> 力扣：[3633. 最早完成陆地和水上游乐设施的时间 I](https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-i/) · Easy · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/Go）](../3633%20最早完成陆地和水上游乐设施的时间%20I/灵茶山艾府.md)
> 力扣：[3635. 最早完成陆地和水上游乐设施的时间 II](https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-ii/) · Medium · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3633.最早完成陆地和水上游乐设施的时间I

[3633. 最早完成陆地和水上游乐设施的时间 I - 力扣（LeetCode）](https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-i/description/)

3635.最早完成陆地和水上游乐设施的时间II

[3635. 最早完成陆地和水上游乐设施的时间 II - 力扣（LeetCode）](https://leetcode.cn/problems/earliest-finish-time-for-land-and-water-rides-ii/description/)

题目给出两种类别的游乐园项目，分别是陆地游乐设施和水上游乐设施。

对于陆地游乐设施，给出两个数组landStartTime以及landDuration，其中landStartTime[index]表示第index个陆地游乐设施最早可以开始的时间，landDuration[index]表示第index个陆地游乐设施持续的时间。

对于水上游乐设施，同样给出两个数组waterStartTime以及waterDuration，含义与陆地的设施类似。

一位乘客必须体验一个陆地游乐设施以及一个水上游乐设施，顺序不限。对于每个游乐设施，都必须在其开方之后才能体验，如果在时间t开始体验，那么将在t + duration时结束。完成一个游乐设施后，游客可以立即乘坐另一个已经开放的游乐设施，或者等待它开放。

问游客可以完成这两个游乐设施的最早可能时间。

两题的题设一致，第二题的数据规模较大。

由于题目只要求体验陆地和水上游乐设施各一种，那么一个自然的想法就是分别计算先玩陆地再玩水上，以及先玩水上再玩陆地的最早结束时间，然后取二者的较小值就行了。

无论是先玩哪一边，都应该玩结束时间最早的那个游乐设施，也就是说可以通过一趟遍历，找出当前目标中最早结束的游乐设施进行游玩，然后在结束后再去玩另一边的设施。不妨设先玩的这一边结束时间为t，那么也只需遍历另一边所有的游乐设施，如果其开放时间s小于等于t，那么总的结束时间就是t加上该设施的duration，否则就必须先等到该设施的开放时间再体验，结束时间就是该设施的开放时间s加上该设施的duration。

分别计算两种情况的最早结束时间，取其中的较小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
        """
        :type landStartTime: List[int]
        :type landDuration: List[int]
        :type waterStartTime: List[int]
        :type waterDuration: List[int]
        :rtype: int
        """
        
        def calc(first_start, first_duration, second_start, second_duration):
            t = min([s + d for s, d in zip(first_start, first_duration)])
            res = None
            for s, d in zip(second_start, second_duration):
                if s > t:
                    finish = s + d
                else:
                    finish = t + d
                if res is None or res > finish:
                    res = finish
            return res

        return min(calc(landStartTime, landDuration, waterStartTime, waterDuration), calc(waterStartTime, waterDuration, landStartTime, landDuration))
```
