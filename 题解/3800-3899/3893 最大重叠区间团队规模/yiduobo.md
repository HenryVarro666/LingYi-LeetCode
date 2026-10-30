---
title: "3893. 最大重叠区间团队规模"
aliases: ["yiduobo的每日leetcode 3893.最大重叠区间团队规模"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2026799092475372990"
zhihu_id: "2026799092475372990"
zhihu_title: "yiduobo的每日leetcode 3893.最大重叠区间团队规模"
question_id: "3893"
question: "最大重叠区间团队规模"
problem_url: "https://leetcode.cn/problems/maximum-team-size-with-overlapping-intervals/"
created: "2026-04-13T23:40:18+08:00"
updated: "2026-04-13T23:40:21+08:00"
upvotes: 1
comments: 0
---

# 3893. 最大重叠区间团队规模

> **[yiduobo的每日leetcode 3893.最大重叠区间团队规模](https://zhuanlan.zhihu.com/p/2026799092475372990) · 知乎 · 2026-04-13 · 赞同 1**
> 力扣：[3893. 最大重叠区间团队规模](https://leetcode.cn/problems/maximum-team-size-with-overlapping-intervals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3893.最大重叠区间团队规模

<https://leetcode.cn/problems/maximum-team-size-with-overlapping-intervals/description/>

题目给出两个长度为n的整数数组startTime和endTime，其中startTime[index]和endTime[index]分别表示第index个员工工作的开始时间和结束时间。

若两个员工的时间区间至少有一个公共时间点，那么他们就可以进行互动。

若一个团队中存在至少一个员工，可以与其他的所有员工互动，那么这个团队就是有效的。

问有效团队的最大可能规模是多少。

根据题目对有效团队的定义，在这里实际上就要需要计算每个员工最多可以与多少其他的员工互动。直接判断区间是否相交其实是相对麻烦的，不妨反过来计算，判断对于每个员工，有多少其他员工的时间区间与该员工的时间区间不重叠。

对于一个时间区间[s, e]，所有终止时间小于s，以及所有起始时间大于e的区间都不与[s, e]重叠，基于这一点，就可以在排序后通过单调性进行求解。具体来说：

1、先将startTime和endTime以及对应的下标整合起来，得到员工区间数组info，接下来将startTime和endTime分别排序

2、将info按起始时间排序然后一趟遍历，期间使用一个变量p在endTime中从头开始向后移动。对于当前的info[index]，不妨设其起始时间为s，那么若当前的p小于n，且endTime[p]小于s，就将p向后移动，直到p无法移动为止。这样一来，就找出了所有终止时间小于s的区间，一共是p个。

3、同样的，将info按终止时间排序然后倒序遍历，期间使用一个变量p在startTime中从末尾向前移动。对于当前的info[index]，不妨设其终止时间为e，那么若当前的p大于等于0，且startTime[p]大于e，就将p向前移动，直到p无法移动为止。这样一来，就找出了所有起始时间大于e的区间，一共是n - 1 - p个。

4、最后，只需要遍历info中的每个区间，就可以通过步骤2和步骤3中计算得到的非相交区间的数量计算出与当前区间相交区间的数量，并更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumTeamSize(self, startTime, endTime):
        """
        :type startTime: List[int]
        :type endTime: List[int]
        :rtype: int
        """
        
        n = len(startTime)

        info = [(index, startTime[index], endTime[index]) for index in range(n)]
        startTime.sort()
        endTime.sort()
        
        info.sort(key=lambda d:d[1])
        left_miss = [0] * n
        p = 0
        for index, s, _ in info:
            while p < n and endTime[p] < s:
                p += 1
            left_miss[index] = p
        
        info.sort(key=lambda d:d[2])
        right_miss = [0] * n
        p = n - 1
        for index, _, e in info[::-1]:
            while p >= 0 and startTime[p] > e:
                p -= 1
            right_miss[index] = n - 1 - p
        
        res = 0
        for index in range(n):
            res = max(res, n - left_miss[index] - right_miss[index])
        return res
```
