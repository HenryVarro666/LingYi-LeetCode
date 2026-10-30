---
title: "1326. 灌溉花园的最少水龙头数目"
aliases: ["yiduobo的每日leetcode 1326.灌溉花园的最少水龙头数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394474925"
zhihu_id: "394474925"
zhihu_title: "yiduobo的每日leetcode 1326.灌溉花园的最少水龙头数目"
question_id: "1326"
question: "灌溉花园的最少水龙头数目"
problem_url: "https://leetcode.cn/problems/minimum-number-of-taps-to-open-to-water-a-garden/"
difficulty: "Hard"
rating: 1885
created: "2021-07-29T23:30:34+08:00"
updated: "2021-07-29T23:30:34+08:00"
upvotes: 0
comments: 0
---

# 1326. 灌溉花园的最少水龙头数目

> **[yiduobo的每日leetcode 1326.灌溉花园的最少水龙头数目](https://zhuanlan.zhihu.com/p/394474925) · 知乎 · 2021-07-29 · 赞同 0**
> 力扣：[1326. 灌溉花园的最少水龙头数目](https://leetcode.cn/problems/minimum-number-of-taps-to-open-to-water-a-garden/) · Hard · 灵茶山艾府：[一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1326.灌溉花园的最少水龙头数目

[力扣](https://leetcode-cn.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/)

每个水龙头灌溉的范围实际上可以视为一个区间，那么我们的目的就是用最少的区间来覆盖0到n。由于整个区间都需要覆盖住，那么我们不妨从边界开始考虑。

首先，我们必须选择一个可以覆盖住0的区间，那么显然就应该选择一个可以覆盖住0，且右边界最大的区间，设此时的右边界为r。

接下来，为了保证区间可以覆盖，我们需要从左边界小于等于r的区间中继续进行选择。另外，我们不应该选择左边界为0的区间，因为在上一步中已经可知左边界为0的区间中右边界不会超过r，因此不应该选择左边界为0的区间。那么此时，就应当选择左边界在1到r之间，右边界尽量大的区间。

于是现在就有了一种做法，先设当前的l和r为0，然后每一轮，我们都选择左边界在l到r之间，右边界最大的区间，设这个右边界为r'，那么此时我们将l更新为r + 1，将r更新为r'，然后重复这个操作，直到可以覆盖整个区间，或者无法继续扩展区间。

注意到l和r是单调递增的，因此我们可以先将所有区间按左边界从小到大进行排序，那么就可以一趟扫描解决问题了。

最后附上python代码：

```python
class Solution(object):
    def minTaps(self, n, ranges):
        """
        :type n: int
        :type ranges: List[int]
        :rtype: int
        """

        intervals = []
        for index, r in enumerate(ranges):
            l = max(index - r, 0)
            r = min(index + r, n)
            intervals.append([l, r])
        
        intervals = sorted(intervals, key=lambda d:d[0])
        now = 0
        p = 0
        res = 0
        while now < n:            
            next = now
            while p <= n and intervals[p][0] <= now:
                next = max(next, intervals[p][1])
                p += 1

            if now == next:
                return -1

            res += 1
            now = next
            

        return res
```
