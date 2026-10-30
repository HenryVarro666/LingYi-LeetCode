---
title: "1482. 制作m束花所需的最少天数"
aliases: ["yiduobo的每日leetcode 1482.制作m束花所需的最少天数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415904804"
zhihu_id: "415904804"
zhihu_title: "yiduobo的每日leetcode 1482.制作m束花所需的最少天数"
question_id: "1482"
question: "制作m束花所需的最少天数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-days-to-make-m-bouquets/"
created: "2021-09-30T21:53:23+08:00"
updated: "2021-09-30T21:53:23+08:00"
upvotes: 0
comments: 0
---

# 1482. 制作m束花所需的最少天数

> **[yiduobo的每日leetcode 1482.制作m束花所需的最少天数](https://zhuanlan.zhihu.com/p/415904804) · 知乎 · 2021-09-30 · 赞同 0**
> 力扣：[1482. 制作m束花所需的最少天数](https://leetcode.cn/problems/minimum-number-of-days-to-make-m-bouquets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1482.制作m束花所需的最少天数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-days-to-make-m-bouquets/)

随着时间的向后推移，都会有新的花盛开，那么可以将现在盛开的花视为若干个区间，每次有新的花盛开时，就可以合并某些区间。在这里可以使用离散化加线段树的方式来优化这个区间操作。这种做法的时间复杂度为O(mlogm)。

另一种做法则是二分答案。由于时间越晚开的花就越多，因此在这里是符合二分的要求的。那么此时只需要二分答案，然后对于当前二分的日期mid，每次都进行一趟扫描，确定哪些花是盛开的，并在这个过程中统计是否存在m长度为k的连续盛开的花，并根据这个结果修正边界。这种做法的时间复杂度位O(mlog(max-min))，这里的max和min分别表示花朵盛开最晚和最早的时间。

两种做法时间复杂度差别不大，而第二种做法实现起来简单得多，因此我在这里采用的第第二种做法。

最后附上python代码：

```python
class Solution(object):
    def minDays(self, bloomDay, m, k):
        """
        :type bloomDay: List[int]
        :type m: int
        :type k: int
        :rtype: int
        """

        if m * k > len(bloomDay):
            return -1
        
        l = None
        r = None
        for day in bloomDay:
            if l is None or day < l:
                l = day
            if r is None or day > r:
                r = day
        
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            deal = 0
            for day in bloomDay:
                if day <= mid:
                    cnt += 1
                    if cnt == k:
                        deal += 1
                        cnt = 0
                else:
                    cnt = 0
            
            if deal >= m:
                r = mid
            else:
                l = mid + 1
        
        return l
```
