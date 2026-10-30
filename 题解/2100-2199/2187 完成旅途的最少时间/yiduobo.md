---
title: "2187. 完成旅途的最少时间"
aliases: ["yiduobo的每日leetcode 2187.完成旅途的最少时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536709778"
zhihu_id: "536709778"
zhihu_title: "yiduobo的每日leetcode 2187.完成旅途的最少时间"
question_id: "2187"
question: "完成旅途的最少时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-complete-trips/"
difficulty: "Medium"
rating: 1641
created: "2022-07-02T15:42:01+08:00"
updated: "2022-07-02T15:42:01+08:00"
upvotes: 0
comments: 0
---

# 2187. 完成旅途的最少时间

> **[yiduobo的每日leetcode 2187.完成旅途的最少时间](https://zhuanlan.zhihu.com/p/536709778) · 知乎 · 2022-07-02 · 赞同 0**
> 力扣：[2187. 完成旅途的最少时间](https://leetcode.cn/problems/minimum-time-to-complete-trips/) · Medium · 灵茶山艾府：[二分答案，附题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2187.完成旅途的最少时间

[力扣](https://leetcode.cn/problems/minimum-time-to-complete-trips/)

时间越长，完成旅途的趟数就越多，反过来，时间越短，完成旅途的趟数就越少，因此在这里可以二分最终的答案，对于当前二分到的时间mid，计算在mid的时间内可以完成旅途的总数，并与totalTrips进行比较然后调整二分的边界。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, time, totalTrips):
        """
        :type time: List[int]
        :type totalTrips: int
        :rtype: int
        """

        l = 1
        r = (1 + totalTrips / len(time)) * max(time)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for t in time:
                cnt += mid / t
            
            if cnt >= totalTrips:
                r = mid
            else:
                l = mid + 1
        
        return l
```
