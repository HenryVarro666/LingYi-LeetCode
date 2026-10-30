---
title: "436. 寻找右区间"
aliases: ["yiduobo的每日leetcode 436.寻找右区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/199757330"
zhihu_id: "199757330"
zhihu_title: "yiduobo的每日leetcode 436.寻找右区间"
question_id: "436"
question: "寻找右区间"
problem_url: "https://leetcode.cn/problems/find-right-interval/"
created: "2020-08-26T23:12:19+08:00"
updated: "2020-08-26T23:12:19+08:00"
upvotes: 2
comments: 0
---

# 436. 寻找右区间

> **[yiduobo的每日leetcode 436.寻找右区间](https://zhuanlan.zhihu.com/p/199757330) · 知乎 · 2020-08-26 · 赞同 2**
> 力扣：[436. 寻找右区间](https://leetcode.cn/problems/find-right-interval/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

436.寻找右区间<https://leetcode-cn.com/problems/find-right-interval/>

又是区间相关的问题，在这里题目保证起点不重复，那么一个自然的想法就是再按起点进行排序。那么对于区间index的终点y[index]，我们的目标就是找到最小的x[p]，满足x[p] >\= y[index]。由于此时的起点x已经是排好序了的，因此直接在x里面做二分就可以了。

排序的时间复杂度为O(nlogn)，而后续的二分操作总的操作次数为

logn + log(n - 1) + log(n - 2) + ... log(2) \= log(n!)

这一步的时间复杂度同样是O(nlogn)，因此最终的时间复杂度就是O(nlogn)

最后附上python代码：

```python
class Solution(object):
    def findRightInterval(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[int]
        """

        if not intervals:
            return []
        
        n = len(intervals)

        res = [-1] * n
        sorted_intervals = sorted([x + [index] for index, x in enumerate(intervals)], key=lambda d:d[0])
        
        for index, interval in enumerate(sorted_intervals):
            left, right, pos = interval
            if index < n - 1 and right <= sorted_intervals[-1][0]:
                l = index + 1
                r = n - 1
                while l < r:
                    mid = (l + r) / 2
                    if sorted_intervals[mid][0] >= right:
                        r = mid
                    else:
                        l = mid + 1
                res[pos] = sorted_intervals[l][2]

        return res
```
