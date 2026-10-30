---
title: "774. 最小化去加油站的最大距离"
aliases: ["yiduobo的每日leetcode 774.最小化去加油站的最大距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606394438"
zhihu_id: "606394438"
zhihu_title: "yiduobo的每日leetcode 774.最小化去加油站的最大距离"
question_id: "774"
question: "最小化去加油站的最大距离"
problem_url: "https://leetcode.cn/problems/minimize-max-distance-to-gas-station/"
created: "2023-02-15T01:03:22+08:00"
updated: "2023-02-15T01:03:22+08:00"
upvotes: 0
comments: 0
---

# 774. 最小化去加油站的最大距离

> **[yiduobo的每日leetcode 774.最小化去加油站的最大距离](https://zhuanlan.zhihu.com/p/606394438) · 知乎 · 2023-02-15 · 赞同 0**
> 力扣：[774. 最小化去加油站的最大距离](https://leetcode.cn/problems/minimize-max-distance-to-gas-station/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

774.最小化去加油站的最大距离

[力扣](https://leetcode.cn/problems/minimize-max-distance-to-gas-station/)

乍一看感觉使用贪心法应该可以处理，不过在这里k的规模非常大，如果逐个考虑每个加油站放置的位置，那么最终时间复杂度必然与k挂钩。

另一种思路就是转化为判定问题，即对于某种情况，新增k个加油站是否足够，此时的k就变成了一个单纯的数值，最终时间复杂度就与之无关了。

根据这个思路，本题就应该使用二分法来进行求解。新增的加油站越多，最大距离必然就越小，那么在这里就可以二分这个最大距离mid。对于当前的mid，遍历所有初始的加油站位置，计算在相邻加油站之间需要新增多少个加油站才能使得最大距离不超过mid，并使用一个变量cnt记录需要新增的加油站数目。遍历完成后，若mid小于等于k，说明最终答案必然小于等于mid，此时应该更新二分上界为mid，反之，则需要更新二分下界为mid。

需要注意的是，本题是实数的二分，因此二分停止的边界不能再使用严格的大于或者小于，需要给出一个精度。即二分的上下界之差小于某个值时停止。对于本题，则可以直接使用10^(-6)。

最后附上python代码：

```python
class Solution(object):
    def minmaxGasDist(self, stations, k):
        """
        :type stations: List[int]
        :type k: int
        :rtype: float
        """

        left = 0.0
        right = 10 ** 8
        E = 0.1 ** 6

        while left < right - E:
            mid = (left + right) / 2
            cnt = 0
            for index in range(1, len(stations)):
                if stations[index] - stations[index - 1] > mid:
                    t = int((stations[index] - stations[index - 1]) / mid)
                    if stations[index - 1] + mid * t + E >= stations[index]:
                        t -= 1
                    
                    cnt += t

            if cnt <= k:
                right = mid
            else:
                left = mid
        
        return left
```
