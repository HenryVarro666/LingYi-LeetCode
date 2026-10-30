---
title: "3439. 重新安排会议得到的最多空余时间I"
aliases: ["yiduobo的每日leetcode 3439.重新安排会议得到的最多空余时间I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891293826875888707"
zhihu_id: "1891293826875888707"
zhihu_title: "yiduobo的每日leetcode 3439.重新安排会议得到的最多空余时间I"
question_id: "3439"
question: "重新安排会议得到最多空余时间 I"
problem_url: "https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-i/"
difficulty: "Medium"
rating: 1729
created: "2025-04-04T01:31:30+08:00"
updated: "2025-04-04T01:31:30+08:00"
upvotes: 2
comments: 0
---

# 3439. 重新安排会议得到的最多空余时间I

> **[yiduobo的每日leetcode 3439.重新安排会议得到的最多空余时间I](https://zhuanlan.zhihu.com/p/1891293826875888707) · 知乎 · 2025-04-04 · 赞同 2**
> 力扣：[3439. 重新安排会议得到最多空余时间 I](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-i/) · Medium · 灵茶山艾府：[转化成定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3439.重新安排会议得到的最多空余时间I

[3439. 重新安排会议得到最多空余时间 I - 力扣（LeetCode）](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-i/description/)

题目给出一个整数eventTime，表示一个活动的总时长。这个活动始于t \= 0，结束于t \= eventTime。另外给出两个长度为n的整数数组startTime和endTime，分别表示这次活动中n个时间没有重叠的会议，其中第index个会议为\[startTime\[index\], endTime\[index\]\]。

现在可以重新安排至多k个会议，安排的规则是将会议的时间平移，但是需要保证会议时长不会发生改变，同时会议之间的相对顺序也不能发生改变，会议也不能被安排到整个活动时间之外。

问重新安排会议后，两个相邻会议间最大的空余时间是多少。

首先可以明确的是，最终调整的会议必然是连续的k个会议，否则某些调整就没有发挥到作用。

根据这个结论，不妨设调整了第index到index + k - 1这些会议，那么无论怎样调整，这些会议的起始时间都不能小于endTime[index - 1]，结束时间也不能大于startTime[index + k]。更进一步的，相邻会议最大的空余时间的上限，就是区间总时间startTime[index + k] - endTime[index - 1]，再减去这k个会议需要消耗的时间。实际上，达成这个间隔上限是很容易的，一种可行的方案是将所有的k个会议紧挨着第index - 1个会议依次重新安排，那么第index + k - 1个会议与第index个会议间的空余时间就是这个时间间隔上限。

对于上面的问题，则可以使用大小为k的滑动窗口滑过所有连续的长度为k的区间，通过窗口下一个区间的起始时间，减去窗口前一个区间的终止时间，再减去窗口内所有区间长度之和，就可以得到调整当前窗口内这k个区间可以得到的最大空余时间，使用这个最大空余时间更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxFreeTime(self, eventTime, k, startTime, endTime):
        """
        :type eventTime: int
        :type k: int
        :type startTime: List[int]
        :type endTime: List[int]
        :rtype: int
        """
        
        s = 0
        pre = 0
        res = 0
        for index in range(k):
            s += endTime[index] - startTime[index]
        
        for index in range(k, len(startTime)):
            res = max(res, startTime[index] - pre - s)
            s -= (endTime[index - k] - startTime[index - k])
            s += (endTime[index] - startTime[index])
            pre = endTime[index - k]
        
        res = max(res, eventTime - pre - s)
        return res
```
