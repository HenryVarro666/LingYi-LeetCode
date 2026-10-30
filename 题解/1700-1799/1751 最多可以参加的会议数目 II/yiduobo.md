---
title: "1751. 最多可以参加的会议数目II"
aliases: ["yiduobo的每日leetcode 1751.最多可以参加的会议数目II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/455254649"
zhihu_id: "455254649"
zhihu_title: "yiduobo的每日leetcode 1751.最多可以参加的会议数目II"
question_id: "1751"
question: "最多可以参加的会议数目 II"
problem_url: "https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended-ii/"
difficulty: "Hard"
rating: 2041
created: "2022-01-10T00:30:36+08:00"
updated: "2022-01-10T00:40:22+08:00"
upvotes: 1
comments: 0
---

# 1751. 最多可以参加的会议数目II

> **[yiduobo的每日leetcode 1751.最多可以参加的会议数目II](https://zhuanlan.zhihu.com/p/455254649) · 知乎 · 2022-01-10 · 赞同 1**
> 力扣：[1751. 最多可以参加的会议数目 II](https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended-ii/) · Hard · 灵茶山艾府：[动态规划 + 二分查找优化（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1751.最多可以参加的会议数目II

[力扣](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/)

经典的动态规划问题，令f[i][j]表示到时刻i为止，参加j个会议所能获得的最大价值。

首先，由于这里会议的时刻只需要关心相对的大小关系，而具体的时间节点是无所谓的，因此可以按照顺序从小到大排序，然后建立起时间节点到顺序的映射。由于每个会议只有开始和结束两个时间节点，那么对于一共n个会议而言，即使每个时间节点都不重复，最多也就只有n \* 2个时间节点，这样一来时间节点的取值范围就是10^9缩小到了n \* 2，从而使得f[i]这种表示方法不会有内存上的限制。

接下来对于f[i][j]：

1、i时刻可以不参加任何会议，因此可以初始化f[i][j] \= f[i - 1][j]

2、i时刻也可以参加结束时间为i的会议，那么此时需要枚举所有结束时间为i的会议，设当前枚举到第p个会议，那么就有f[i][j] \= f[s[p] - 1][j - 1] + values[p]，其中s[p]表示p的开始时间，values[p]表示p的价值

在这里如果直接枚举的话，转移的时间复杂度也是O(n)的，这样肯定是不行的。一个常规的做法就是将所有会议按照结束时间从小到大进行排序，这样一来随着i的向后推移，p也必然是向后移动的。由于每个会议只会被枚举到一次，那么这里转移的复杂度均摊下来就优化成O(1)了。

需要注意的是，这里不一定需要参加满k个会议，因此最终答案应该是max(f[-1])而不是f[-1][-1]。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, events, k):
        """
        :type events: List[List[int]]
        :type k: int
        :rtype: int
        """

        date_set = set()
        for s, e, v in events:
            date_set.add(s)
            date_set.add(e)
        
        mapping_dict = {}
        for index, date in enumerate(sorted(list(date_set))):
            mapping_dict[date] = index + 1
        
        n = len(mapping_dict) + 1
        f = [[None] * (k + 1) for _ in range(n)]
        f[0][0] = 0
        sorted_events = sorted(events, key=lambda d:d[1])
        p = 0
        for i in range(1, n):
            for j in range(k + 1):
                if f[i - 1][j] is not None:
                    f[i][j] = f[i - 1][j]
            
            while p < len(sorted_events) and mapping_dict[sorted_events[p][1]] == i:
                s = mapping_dict[sorted_events[p][0]]
                for j in range(1, k + 1):
                    if f[s - 1][j - 1] is not None:
                        if f[i][j] is None or f[i][j] < f[s - 1][j - 1] + sorted_events[p][2]:
                            f[i][j] = f[s - 1][j - 1] + sorted_events[p][2]
                
                p += 1
        
        return max(f[-1])
```
