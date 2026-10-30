---
title: "2054. 两个最好的不重叠活动"
aliases: ["yiduobo的每日leetcode 2054.两个最好的不重叠活动"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "leetcode/monotonic-stack", "题单/动态规划", "题单/单调栈", "题单/贪心算法", "题单/动态规划/七-其他线性-DP", "题单/单调栈/一-单调栈", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/512340804"
zhihu_id: "512340804"
zhihu_title: "yiduobo的每日leetcode 2054.两个最好的不重叠活动"
question_id: "2054"
question: "两个最好的不重叠活动"
problem_url: "https://leetcode.cn/problems/two-best-non-overlapping-events/"
difficulty: "Medium"
rating: 1883
created: "2022-05-10T22:17:54+08:00"
updated: "2022-05-10T22:17:54+08:00"
upvotes: 0
comments: 0
---

# 2054. 两个最好的不重叠活动

> **[yiduobo的每日leetcode 2054.两个最好的不重叠活动](https://zhuanlan.zhihu.com/p/512340804) · 知乎 · 2022-05-10 · 赞同 0**
> 力扣：[2054. 两个最好的不重叠活动](https://leetcode.cn/problems/two-best-non-overlapping-events/) · Medium · 灵茶山艾府：[排序 + 单调栈二分（通用做法是 DP）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2054.两个最好的不重叠活动

[力扣](https://leetcode.cn/problems/two-best-non-overlapping-events/)

题目要求找出两个不重叠的活动，且二者的价值之和最大。

由于数据规模比较大，因此使用朴素的二重枚举算法肯定是行不通的，只能想办法枚举其中一场活动，然后从剩下可用的活动中选出最优的。由于两场活动是等价的，那么不妨枚举前一场活动，然后就只需选择开始时间在这场活动结束时间后的活动当中，价值最大的那一场。

对于这个问题，直接去找依然是O(n^2)的时间复杂度，不过在这里可以借助排序和单调性来进行优化。

首先将所有活动按照startTime和endTime分别从小到大进行排序，得到两个数组start和end。其中start[i]表示原数组中的第i场活动，按startTime从小到大排序后的下标。同样的，end[i]则表示原数组中的第i场活动，按endTime从小到大排序后的下标。

接下来，令f[i]表示按endTime排序后，第i到第n - 1场活动中的最大价值，那么对于f[i]，就有

f\[i\] \= max(f\[i + 1\], values\[end\[i\]\])

得到f之后，就可以按起始时间从小到大枚举所有活动。对于当前枚举到的活动index，需要找出所有开始时间大于等于index的结束时间的活动，也就是所有满足endTime\[end\[index\]\] \<\= startTime\[start\[p\]\]。对于p的求解，由于start和end是按startTime和endTime排好序的，因此当index先后移动时，p也会跟着向后移动，从而在均摊O(1)的时间内找出每个index对应的p。

得到p之后，end\[p\]到end\[n - 1\]之间的活动都是可选的，而其中价值最大的活动就是上面求出来的f\[p\]，于是可以用values\[end\[index\]\] + f\[p\]来更新最终答案。

需要注意的时，在这里可能出现找不到合法的p的情况，此时则需要直接使用values\[end\[index\]\]来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxTwoEvents(self, events):
        """
        :type events: List[List[int]]
        :rtype: int
        """

        n = len(events)
        start = sorted(range(n), key=lambda d:events[d][0])
        end = sorted(range(n), key=lambda d:events[d][1])

        f = [events[start[-1]][2]]
        for index in range(n - 2, -1, -1):
            f.append(max(f[-1], events[start[index]][2]))
        
        f.reverse()
        
        p = 0
        res = 0
        now = 0
        for index in range(n):
            while p < n and events[start[p]][0] <= events[end[index]][1]:
                p += 1
            
            if p != n:
                res = max(res, events[end[index]][2] + f[p])
            else:
                res = max(res, events[end[index]][2])
        
        return res
```
