---
title: "3538. 合并得到最小旅行时间"
aliases: ["yiduobo的每日leetcode 3538.合并得到最小旅行时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907214973001774296"
zhihu_id: "1907214973001774296"
zhihu_title: "yiduobo的每日leetcode 3538.合并得到最小旅行时间"
question_id: "3538"
question: "合并得到最小旅行时间"
problem_url: "https://leetcode.cn/problems/merge-operations-for-minimum-travel-time/"
difficulty: "Hard"
rating: 2461
created: "2025-05-17T23:55:14+08:00"
updated: "2025-05-17T23:55:14+08:00"
upvotes: 1
comments: 0
---

# 3538. 合并得到最小旅行时间

> **[yiduobo的每日leetcode 3538.合并得到最小旅行时间](https://zhuanlan.zhihu.com/p/1907214973001774296) · 知乎 · 2025-05-17 · 赞同 1**
> 力扣：[3538. 合并得到最小旅行时间](https://leetcode.cn/problems/merge-operations-for-minimum-travel-time/) · Hard · 灵茶山艾府：[相邻相关划分型 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3538.合并得到最小旅行时间

[3538. 合并得到最小旅行时间 - 力扣（LeetCode）](https://leetcode.cn/problems/merge-operations-for-minimum-travel-time/description/)

题目给出一个长度为l公立的直路，以及一个整数n、一个整数k和两个长度为n的整数数组position和time。

position列出了路边的位置，单位为公立。position是单调递增的，其中position[0] \= 0，position[n - 1] \= l。

而每个time[index]则表示位于position[index]到position[index + 1]之间时，行驶1公立所需的时间。

现在要求执行恰好k次合并操作，在一次合并操作中，需要选择一个大于0且小于n - 1的下标index，将time[index]累加到time[index + 1]上，同时将position[index]以及time[index]从数组中删去。

问执行恰好k次合并操作后，从0到l的最小总旅行时间。

对于这类划分或者合并类的问题，依然是考虑使用动态规划进行求解。

常规来说，令f[index][merge_time]表示position[0]到position[index]中执行了merge_time次合并后得到的最小总时间，然后枚举最后一个位置position[index]向前合并到的上一个position下标pre_index，那么对于最后这个下标index，其一共执行了index - pre_index - 1次合并操作，因此在pre_index之前一共执行了merge_time - (index - pre_index - 1)次合并操作，于是就可以用f[pre_index][merge_time - (index - pre_index) - 1]来更新f[index][merge_time]了。

然而对于本题，position和index是存在位置差异的。具体来说，一段路径的时间系数对应于这段路径的起点下标，但是上面状态中保留的是终点，因此如果不清楚起点坐标往前合并了多少次，就无法确定其对应的time值，也就无法计算转移的代价。不过好在本题的数据规模不大，直接将需要的东西往里加就行了。

更新状态为f[index][merge_time][last_merge]表示position[0]到position[index]中执行了merge_time次合并操作，且position[index]往前执行了last_merge次合并操作时的最小总时间，那么对于f[index][merge_time][last_merge]，可以先通过index - last_merge - 1计算区间起点pre_index，同时使用merge_time - last_merge计算之前的合并次数pre_merge_time。

接下来，枚举pre_index往前合并的次数pre_last_merge，若f[pre_index][pre_merge_time][pre_last_merge]存在，那么就可以使用其更新f[index][merge_time][last_merge]，最后这一段所需的代价则为距离之差position[index] - position[pre_index]，乘以合并后时间系数time[pre_index] + time[pre_index - 1] + ... + time[pre_index - pre_last_merge]。最后这一段是time的一个区间和，可以采用前缀和来优化。

计算完成后，枚举f[n - 1][k]中所有可行的last_merge，取其中的最小值作为最终答案即可。

这样一来，就得到了一种O(n \* k^3)的算法，在本体的数据规模下是完全没有问题的。

在具体实现上，对于当前的index，merge_time的上限为min(k, index - 1)，而last_merge的上限自然是merge_time，在限制了合并次数后就可以自然避免下标和数组越界的问题。

最后附上python代码：

```python
class Solution(object):
    def minTravelTime(self, l, n, k, position, time):
        """
        :type l: int
        :type n: int
        :type k: int
        :type position: List[int]
        :type time: List[int]
        :rtype: int
        """
        
        intervals = [position[index] - position[index - 1] for index in range(1, n)]
        f = [[[None] * (k + 1) for _ in range(k + 1)] for _ in range(n)]
        f[0][0][0] = 0

        st = [0]
        for t in time:
            st.append(st[-1] + t)

        for index in range(1, n):
            for merge_time in range(min(k + 1, index)):
                for last_merge in range(merge_time + 1):
                    pre_index = index - last_merge - 1
                    pre_merge_time = merge_time - last_merge
                    for pre_last_merge in range(pre_merge_time + 1):
                        if f[pre_index][pre_merge_time][pre_last_merge] is not None:
                            cost = f[pre_index][pre_merge_time][pre_last_merge] + (position[index] - position[pre_index]) * (st[pre_index + 1] - st[pre_index - pre_last_merge])
                            if f[index][merge_time][last_merge] is None or f[index][merge_time][last_merge] > cost:
                                f[index][merge_time][last_merge] = cost

        res = None
        for last_merge in range(k + 1):
            if f[-1][-1][last_merge] is not None and (res is None or res > f[-1][-1][last_merge]):
                res = f[-1][-1][last_merge]
        return res
```
