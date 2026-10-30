---
title: "644. 子数组最大平均数II"
aliases: ["yiduobo的每日leetcode 644.子数组最大平均数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603003308"
zhihu_id: "603003308"
zhihu_title: "yiduobo的每日leetcode 644.子数组最大平均数II"
question_id: "644"
question: "子数组最大平均数II"
problem_url: "https://leetcode.cn/problems/maximum-average-subarray-ii/"
created: "2023-02-02T23:08:56+08:00"
updated: "2023-02-02T23:08:56+08:00"
upvotes: 0
comments: 0
---

# 644. 子数组最大平均数II

> **[yiduobo的每日leetcode 644.子数组最大平均数II](https://zhuanlan.zhihu.com/p/603003308) · 知乎 · 2023-02-02 · 赞同 0**
> 力扣：[644. 子数组最大平均数II](https://leetcode.cn/problems/maximum-average-subarray-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

644.子数组最大平均数II

[力扣](https://leetcode.cn/problems/maximum-average-subarray-ii/)

对于子数组相关的问题，变长的滑动窗口总是值得考虑的一种方案。如果可以合理运用单调性，一般都可以得到一种O(n)的做法。

不过对于本题，单调性并不是那么好找。

按照常规的处理方法，一般是将左边界中较差的单个数组依次移出窗口，但是对于本题，要求解的是最大的平均值，那么在这里就可能出现好的数值为差的数值打掩护的情况。

例如[50, -100, -100, 150]这种情况，随着右边界的向右移动，得到的平均值分别是50、-25、-50、0。如果按照常规一个一个数处理的话，当右边界来到150时，左边界的50依然比当前的平均值0更优，因此不会将50移出窗口，也就是说这里的50实际上保护了后面的两个-100，拉低了整体的平均值。

为了应对这种情况，需要将窗口的移动从单个数值升级到整个区间。

对于上面的例子，区间[0, 2]的平均值为-50，而区间[3, 3]的平均值为150，因此需要将区间[0, 2]移出窗口。但是这里又有一个问题，即如何合理地划分这些区间，在这里为什么将[50, -100, -100]和[150]划分开来。

不妨从平均值的角度来进行分析。

对于两个都以p为终点的区间[i, p]以及[j, p]，在这里不妨设i \< j，那么当avg([i, p]) \< avg([j, p])时，就必然有avg([j, p]) > avg([i, j - 1]) > avg([i, p])。具体的数学推导可以列式子通分，在这里就不展开了。一个简单的理解是如果j左侧区间的平均值较差，那么将其合并起来后得到的区间平均值肯定比不上原来的平均值。

基于这个思路，就得到了一种划分的方法。

随着窗口右边界的向右移动，在保证了最后k个元素必须存在后，一定会出现一个本轮可以被移除的元素，其下标就是当前右边界的下标减去k。对于这个元素，将其视为一个独立的区间。那么对于这个区间：

1、如果其平均值比之前的区间要好，就应该将其保持独立

2、反过来，就应该将其融入到之前的区间中，这样做的理由是在这种情况下，如果选择了这个区间，那么就应该同时选择其左侧的区间，因为融合起来的平均值是比当前区间平均值更大的。

重复此过程直到出现情况1。

可以发现，这样一来就就得到了一个平均值单调递增的区间列表，这个列表记录了当前窗口中可移除的所有区间。接下来对于这个列表，若其头部的区间，也就是平均值最小的区间拉低了当前窗口中平均值的水平，那么就应该将其从窗口中移除，于是可以不断对比当前区间列表中最左侧区间的平均值以及当前窗口的平均值，若最左侧区间的平均值更小，那么就将其移除。重复此过程直到区间列表为空或者最左侧区间的平均值更优为止。

最后，使用当前窗口的平均值更新答案，然后继续将窗口向右移动。

上面算法中的窗口列表由于存在右侧进出以及左侧的弹出操作，因此需要使用一个双端队列来实现。这样一来，就得到了一种时间复杂度为O(n)的算法。

最后附上python代码：

```python
class Solution(object):
    def findMaxAverage(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: float
        """

        intervals = deque()

        now = sum(nums[:k]) * 1.0
        cnt = k
        res = now / cnt
        for index, num in enumerate(nums[k:]):
            now += num
            cnt += 1
            s = nums[index] * 1.0
            s_cnt = 1
            while intervals:
                last_s, last_cnt = intervals[-1]
                if last_s * s_cnt >= s * last_cnt:
                    intervals.pop()
                    s += last_s
                    s_cnt += last_cnt
                else:
                    break
            
            intervals.append([s, s_cnt])

            while intervals:
                first_s, first_cnt = intervals[0]
                if first_s * cnt <= now * first_cnt:
                    intervals.popleft()
                    now -= first_s
                    cnt -= first_cnt
                else:
                    break
            
            res = max(res, now / cnt)
        
        return res
```
