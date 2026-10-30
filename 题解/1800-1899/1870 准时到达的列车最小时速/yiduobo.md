---
title: "1870. 准时到达的列车最小时速"
aliases: ["yiduobo的每日leetcode 1870.准时到达的列车最小时速"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/474959504"
zhihu_id: "474959504"
zhihu_title: "yiduobo的每日leetcode 1870.准时到达的列车最小时速"
question_id: "1870"
question: "准时到达的列车最小时速"
problem_url: "https://leetcode.cn/problems/minimum-speed-to-arrive-on-time/"
difficulty: "Medium"
rating: 1676
created: "2022-03-02T23:13:07+08:00"
updated: "2022-03-02T23:13:08+08:00"
upvotes: 0
comments: 0
---

# 1870. 准时到达的列车最小时速

> **[yiduobo的每日leetcode 1870.准时到达的列车最小时速](https://zhuanlan.zhihu.com/p/474959504) · 知乎 · 2022-03-02 · 赞同 0**
> 力扣：[1870. 准时到达的列车最小时速](https://leetcode.cn/problems/minimum-speed-to-arrive-on-time/) · Medium · 灵茶山艾府：[极致优化！避免浮点误差的写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1870.准时到达的列车最小时速

[力扣](https://leetcode-cn.com/problems/minimum-speed-to-arrive-on-time/)

列车的速度越快，到达的时间就越早，那么在这里就可以二分答案，每次根据当前到达时间以及hour的大小来确定需要降速还是提速。

对于二分的边界，下界显然是1，而上界题目已经给出了是10^7。

接下来开始二分。对于当前处理的速度mid，先计算按这个速度行驶需要的时间。需要注意的是，在这里前n - 1站的时间需要向上取整，但最后一站的时间不需要。计算出总耗时后，若耗时小于等于hour，那么说明当前速度可能可以适当放慢，因此更新右边界为mid，否则说明必须提速，因此更新左边界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minSpeedOnTime(self, dist, hour):
        """
        :type dist: List[int]
        :type hour: float
        :rtype: int
        """

        if len(dist) - 1 >= hour:
            return -1

        l = 1
        r = 10 ** 7
        while l < r:
            mid = (l + r) >> 1
            cnt = 0.0
            for d in dist[:-1]:
                cnt += d / mid
                if d % mid != 0:
                    cnt += 1

            cnt += float(dist[-1]) / mid
            if cnt <= hour:
                r = mid
            else:
                l = mid + 1
        
        return l
```
