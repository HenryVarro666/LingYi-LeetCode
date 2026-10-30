---
title: "3414. 不重叠区间的最大得分"
aliases: ["yiduobo的每日leetcode 3414.不重叠区间的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32253348551"
zhihu_id: "32253348551"
zhihu_title: "yiduobo的每日leetcode 3414.不重叠区间的最大得分"
question_id: "3414"
question: "不重叠区间的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-of-non-overlapping-intervals/"
difficulty: "Hard"
rating: 2723
created: "2025-03-24T00:29:50+08:00"
updated: "2025-03-24T00:29:50+08:00"
upvotes: 0
comments: 0
---

# 3414. 不重叠区间的最大得分

> **[yiduobo的每日leetcode 3414.不重叠区间的最大得分](https://zhuanlan.zhihu.com/p/32253348551) · 知乎 · 2025-03-24 · 赞同 0**
> 力扣：[3414. 不重叠区间的最大得分](https://leetcode.cn/problems/maximum-score-of-non-overlapping-intervals/) · Hard · 灵茶山艾府：[动态规划 + 二分查找优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3414.不重叠区间的最大得分

[3414. 不重叠区间的最大得分 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-score-of-non-overlapping-intervals/description/)

题目给出一个二维整数数组intervals，其中intervals\[i\] \= \[l\[i\], r\[i\], weight\[i\]\]，表示有一个起点为l\[i\]，终点为r\[i\]，权重为weight\[i\]的区间。现在要求从中选出最多4个互不重叠的区间，问得分最大，且选出的区间字典序最小的选择方案是什么。

如果不考虑最多只能选择4个区间这个限制，同时也不需要给出具体方案的情况的话，这就是一个经典的动态规划问题。将区间按终点从小到大进行排序，然后令f[index]表示从排序后的前index个区间中选出若干个不重叠区间可以得到的最大收益，那么对于f[index]：

1、放弃最后这个区间：

此时就有f[index] \= f[index - 1]

2、选择最后这个区间：

此时就有f[index] \= max(f[0]、f[1]、...、f[t]) + w[index]，其中t为满足r[t] \<\= l[index]的最大的下标。另一方面，f在这里显然是单调不减的，因此上面的转移方程可以直接写成f[index] \= f[t] + weight[index]。又由于区间是按照终点排序过的，于是可以用l[index]在排序后的区间中进行二分来确定t。

---

回到本题。本题中多了最多选择4个区间，且还需要保存字典序最小的方案这两个限制。

对于4个区间这个限制，可以修改状态表示，令f[p][index]表示从前index个区间中选择p + 1个区间的最大收益，那么对于f[p][index]：

1、首先依然是放弃最后这个区间：

此时就有f[p][index] \= f[p][index - 1]

2、如果要选择最后这个区间：

2-1）若p等于0：

那么只能选择当前区间，也就是f[p][index] \= weight[index]

2-2）若p > 0：

同样是通过二分找出最优的位置t，从f[p - 1][t]得到f[p][index]，即f[p][index] \= f[p - 1][t] + weight[index]

而对于字典序最小的方案这个要求，则可以将f保留的值从最大的收益，改为最大的收益与最小的字典序形成的二元组，在状态转移时先判断收益的大小，若收益相同再判断字典序就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumWeight(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[int]
        """
        
        f = [[[0, []]] for _ in range(4)]
        sorted_intervals = sorted(enumerate(intervals), key=lambda d:d[1][1])

        for index, (original_index, (left, right, weight)) in enumerate(sorted_intervals):
            hi = index
            lo = 0
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if sorted_intervals[mid - 1][1][1] < left:
                    lo = mid
                else:
                    hi = mid - 1

            for p in range(4):
                if p == 0:
                    choose = [-weight, [original_index]]
                else:
                    choose = [f[p - 1][lo][0] - weight, sorted(f[p - 1][lo][1] + [original_index])]

                f[p].append(min(f[p][-1], choose))

        return f[-1][-1][1]
```
