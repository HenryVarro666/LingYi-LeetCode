---
title: "759. 员工空闲时间"
aliases: ["yiduobo的每日leetcode 759.员工空闲时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/sorting", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606079644"
zhihu_id: "606079644"
zhihu_title: "yiduobo的每日leetcode 759.员工空闲时间"
question_id: "759"
question: "员工空闲时间"
problem_url: "https://leetcode.cn/problems/employee-free-time/"
difficulty: "Hard"
created: "2023-02-14T00:35:27+08:00"
updated: "2023-02-14T00:35:27+08:00"
upvotes: 0
comments: 0
---

# 759. 员工空闲时间

> **[yiduobo的每日leetcode 759.员工空闲时间](https://zhuanlan.zhihu.com/p/606079644) · 知乎 · 2023-02-14 · 赞同 0**
> 力扣：[759. 员工空闲时间](https://leetcode.cn/problems/employee-free-time/) · Hard · 灵茶山艾府：[Go 差分+位运算压缩状态](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

759.员工空闲时间

[力扣](https://leetcode.cn/problems/employee-free-time/)

题目要求找出所有员工的空闲时间区间，但是给出的是忙碌的时间段。在逻辑上来看，应该是一个取补然后取交的过程，感觉就比较复杂度的。注意到集合运算中存在补集的交集相当于并集的补集这个说法，那么在这里可以先求这些忙碌时间段的并集，然后再反推空闲的时间。

换言之，问题可以转化为给出若干区间，先求出区间的并，然后求出其补集。

对于区间的并，是非常经典的区间合并问题，可以采用常规的排序后合并的处理方法。不过注意到每个人的时间段都已经排好序了，那么也可以采用堆辅助的多路归并的方法来合并区间。

区间合并以及多路归并的处理思路可以参考之前的

[yiduobo：yiduobo的每日leetcode 56.合并区间](https://zhuanlan.zhihu.com/p/128126787)

以及

[yiduobo：yiduobo的每日leetcode 23.合并K个排序链表](https://zhuanlan.zhihu.com/p/116101679)

这里就不展开了。

得到合并后的区间之后，还需要找出空闲的区间。可以发现，前一个区间的终点到后一个区间的起点就是一个空闲的区间，那么可以一趟遍历，两两枚举相邻的区间，找出这两个区间之间的空闲区间加入到答案中。

最后附上python代码：

```python
"""
# Definition for an Interval.
class Interval(object):
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
"""

class Solution(object):
    def employeeFreeTime(self, schedule):
        """
        :type schedule: [[Interval]]
        :rtype: [Interval]
        """

        heap = []
        n = len(schedule)
        pos = [0] * n
        for index, sch in enumerate(schedule):
            if len(sch) > 0:
                heapq.heappush(heap, [sch[0].start, sch[0].end, index])
                pos[index] += 1
        
        nowx, nowy = None, None
        busy_time = []
        while heap:
            x, y, index = heapq.heappop(heap)
            if nowx is None or nowy < x:
                if nowx is not None:
                    busy_time.append([nowx, nowy])
                nowx, nowy = x, y
            else:
                nowy = max(nowy, y)
            
            if pos[index] < len(schedule[index]):
                heapq.heappush(heap, [schedule[index][pos[index]].start, schedule[index][pos[index]].end, index])
                pos[index] += 1

        busy_time.append([nowx, nowy])

        res = []
        for index in range(1, len(busy_time)):
            if busy_time[index][0] > busy_time[index - 1][1]:
                res.append(Interval(busy_time[index - 1][1], busy_time[index][0]))
        
        return res
```
