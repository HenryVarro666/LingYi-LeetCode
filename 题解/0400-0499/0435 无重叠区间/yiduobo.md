---
title: "435. 无重叠区间"
aliases: ["yiduobo的每日leetcode 435.无重叠区间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/199737488"
zhihu_id: "199737488"
zhihu_title: "yiduobo的每日leetcode 435.无重叠区间"
question_id: "435"
question: "无重叠区间"
problem_url: "https://leetcode.cn/problems/non-overlapping-intervals/"
difficulty: "Medium"
rating: 1700
created: "2020-08-26T23:03:52+08:00"
updated: "2020-08-26T23:03:52+08:00"
upvotes: 0
comments: 0
---

# 435. 无重叠区间

> **[yiduobo的每日leetcode 435.无重叠区间](https://zhuanlan.zhihu.com/p/199737488) · 知乎 · 2020-08-26 · 赞同 0**
> 力扣：[435. 无重叠区间](https://leetcode.cn/problems/non-overlapping-intervals/) · Medium · 灵茶山艾府：[贪心+证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

435.无重叠区间<https://leetcode-cn.com/problems/non-overlapping-intervals/>

贪心法的题目。

将所有区间按起点从小到大进行排序，然后从头开始一趟扫描。不妨设我们当前考察的区间为(x[index]，y[index])，那么对于区间(x[index + 1]，y[index + 1])而言：

1、若x[index + 1] >\= y[index]，那么此时区间index与区间index + 1不重叠。由于x是单调递增的，因此对于区间index + 1后面的区间来说，其起点必然大于等于x[index + 1]，因此同样不会与区间index重叠，即后续没有区间与区间index重叠，因此我们在这里就没有必要再考察区间index了，应该继续往后扫描，即考察区间index + 1。

2、若x[index + 1] \< y[index]，说明两个区间重叠，必须删去其中某一个。为了尽量少删除区间，很明显应该删去右边界较大的那一个区间，保留另一个，那么此时应该将答案加一，同时将考察的对象变为右边界较小的那个区间。

最后附上python代码：

```python
class Solution(object):
    def eraseOverlapIntervals(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """

        if not intervals:
            return 0

        sorted_intervals = sorted(intervals, key=lambda d:(d[0], d[1]))
        left, right = sorted_intervals[0]
        res = 0
        for x, y in sorted_intervals[1:]:
            if x >= right:
                left, right = x, y
            else:
                res += 1
                right = min(right, y)

        return res
```
