---
title: "1235. 规划兼职工作"
aliases: ["yiduobo的每日leetcode 1235.规划兼职工作"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/五-堆-优先队列", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384429437"
zhihu_id: "384429437"
zhihu_title: "yiduobo的每日leetcode 1235.规划兼职工作"
question_id: "1235"
question: "规划兼职工作"
problem_url: "https://leetcode.cn/problems/maximum-profit-in-job-scheduling/"
difficulty: "Hard"
rating: 2023
created: "2021-06-27T14:54:28+08:00"
updated: "2021-06-27T14:54:28+08:00"
upvotes: 0
comments: 0
---

# 1235. 规划兼职工作

> **[yiduobo的每日leetcode 1235.规划兼职工作](https://zhuanlan.zhihu.com/p/384429437) · 知乎 · 2021-06-27 · 赞同 0**
> 力扣：[1235. 规划兼职工作](https://leetcode.cn/problems/maximum-profit-in-job-scheduling/) · Hard · 灵茶山艾府：[动态规划 + 二分查找优化（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1235.规划兼职工作

[力扣](https://leetcode-cn.com/problems/maximum-profit-in-job-scheduling/)

对于这些兼职工作，我们希望能够尽快完结，同时收入最高，于是一个自然的想法就是将这些兼职工作按结束时间从小到大进行排序，然后执行动态规划。令f[i][j]表示从前i件工作选择若干件，最后一件工作完结时刻为j的最大收益。

那么若存在某个f[i][p] \<\= f[i][q]，同时有p >\= q，那么这里的f[i][p]就没有存在的必要的。因此我们在执行过程中不需要所有的时间点，而只需要保留可能成为答案的那些时间点。这样一来，整个f数组是随着j的增大单调递增的。由于这个原因，我们也无需用下标来表示j这一维，而只需要维护单调序列就行了。

于是现在的状态就可以改为f[i][j][0]和f[i][j][1]，分别表示前i件工作，选择若干件，得到的有必要保留的单调序列中第j件工作的结束时间以及收入。

对于当前的兼职工作，我们只需要在f中找到最大的j，其中j需要满足f[i - 1][j][0] \<\= start，那么我们就可以执行当前的工作，完成时间end必然是大于f中所有的完成时间，那么此时就应该将f[i - 1][j][1] + profit加入到f末尾。查找最大的j则可以利用时间的单调性，在f[i - 1]中进行二分。

由于这的状态只与上一轮有关，因此也可以省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def jobScheduling(self, startTime, endTime, profit):
        """
        :type startTime: List[int]
        :type endTime: List[int]
        :type profit: List[int]
        :rtype: int
        """

        info = sorted(zip(startTime, endTime, profit), key=lambda d:d[1])
        f = [[0, 0]]
        for s, e, p in info:
            if s >= f[-1][0]:
                f.append([e, f[-1][1] + p])
            else:
                l = 0
                r = len(f) - 1
                while l < r:
                    mid = (l + r + 1) >> 1
                    if f[mid][0] <= s:
                        l = mid
                    else:
                        r = mid - 1
                
                if f[r][1] + p > f[-1][1]:
                    f.append([e, f[r][1] + p])
        
        return f[-1][1]
```
