---
title: "3296. 移山所需的最少秒数"
aliases: ["yiduobo的每日leetcode 3296.移山所需的最少秒数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "leetcode/simulation", "leetcode/heap-priority-queue", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/919294736"
zhihu_id: "919294736"
zhihu_title: "yiduobo的每日leetcode 3296.移山所需的最少秒数"
question_id: "3296"
question: "移山所需的最少秒数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-seconds-to-make-mountain-height-zero/"
difficulty: "Medium"
rating: 1850
created: "2024-10-11T00:08:07+08:00"
updated: "2024-10-11T00:08:07+08:00"
upvotes: 1
comments: 0
---

# 3296. 移山所需的最少秒数

> **[yiduobo的每日leetcode 3296.移山所需的最少秒数](https://zhuanlan.zhihu.com/p/919294736) · 知乎 · 2024-10-11 · 赞同 1**
> 力扣：[3296. 移山所需的最少秒数](https://leetcode.cn/problems/minimum-number-of-seconds-to-make-mountain-height-zero/) · Medium · 灵茶山艾府：[两种方法：最小堆模拟/二分答案（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3296.移山所需的最少秒数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-seconds-to-make-mountain-height-zero/description/)

题目给出一个整数mountainHeight表示山的高度，同时给出一个整数数组workerTimes，表示工人们的工作时间，以秒为单位。工人们需要同时工作来降低山的高度，对于工人i，如果想让山的高度降低x，需要花费的时间为workerTimes[i] + workerTimes[i] \* 2 + ... + workerTimes[i] \* x秒。

问将山的高度降低到0最少需要花费多少秒。

时间过去越久，工人们可以降低的山的总高度就越多，符合二分的性质，因此在这里可以二分将山的高度降低到0所需的时间。

二分的下界自然是1，而上界可以取得保守一点，就取效率最高的工人单干所需的时间。对于工人i，其单干所需的时间就是

workerTimes[i] + workerTimes[i] \* 2 + ... + workerTimes[i] \* mountainHeight

求和后为

workerTimes[i] \* (1 + mountainHeight) \* mountainHeight // 2

因此二分的上界就可以定为

min(workerTimes) \* (1 + mountainHeight) \* mountainHeight // 2

接下来开始进行二分。对于当前二分到的时间mid，遍历每个工人。对于当前遍历到的workerTimes[i]，不妨设其可以降低山的高度为x，那么就有

workerTimes[i] \* (1 + x) \* x // 2 \<\= mid

即

x^2 + x \<\= mid \* 2 // workerTimes[i]

解这个不等式可以得到

x \<\= sqrt(mid \* 2.0 / workerTimes[i] + 0.25) - 0.5)

对右侧部分向下取整即可得到x。

累加所有工人可以降低的山的高度，得到总的高度h，若h \< mountainHeight，说明时间不够，需要调整二分下界为mid + 1，否则调整二分上界为mid。

最后附上python代码：

```python
class Solution(object):
    def minNumberOfSeconds(self, mountainHeight, workerTimes):
        """
        :type mountainHeight: int
        :type workerTimes: List[int]
        :rtype: int
        """

        left = 1
        right = min(workerTimes) * (1 + mountainHeight) * mountainHeight // 2

        while left < right:
            mid = (left + right) // 2
            h = 0
            for t in workerTimes:
                h += int(sqrt(mid * 2.0 / t + 0.25) - 0.5)
            
            if h < mountainHeight:
                left = mid + 1
            else:
                right = mid

        return left
```
