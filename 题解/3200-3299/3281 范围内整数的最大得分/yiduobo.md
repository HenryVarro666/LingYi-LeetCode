---
title: "3281. 范围内整数的最大得分"
aliases: ["yiduobo的每日leetcode 3281.范围内整数的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/821911424"
zhihu_id: "821911424"
zhihu_title: "yiduobo的每日leetcode 3281.范围内整数的最大得分"
question_id: "3281"
question: "范围内整数的最大得分"
problem_url: "https://leetcode.cn/problems/maximize-score-of-numbers-in-ranges/"
difficulty: "Medium"
rating: 1768
created: "2024-10-04T23:42:50+08:00"
updated: "2024-10-04T23:42:50+08:00"
upvotes: 0
comments: 0
---

# 3281. 范围内整数的最大得分

> **[yiduobo的每日leetcode 3281.范围内整数的最大得分](https://zhuanlan.zhihu.com/p/821911424) · 知乎 · 2024-10-04 · 赞同 0**
> 力扣：[3281. 范围内整数的最大得分](https://leetcode.cn/problems/maximize-score-of-numbers-in-ranges/) · Medium · 灵茶山艾府：[二分答案：最大化最小值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3281.范围内整数的最大得分

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-score-of-numbers-in-ranges/description/)

题目给出一个整数数组start以及一个整数d，代表n个区间[start[i], start[i] + d]。

现在需要从这n个区间中各选择一个整数，是的这些整数两两之间差的绝对值的最小值最大。

首先可以明确的是，对于一系列整数而言，最小的差的绝对值一定是出现在大小相邻的整数对之间，那么在这里就可以先将区间按起点从小到大排序，然后按顺序依次从区间中取数。需要注意的是这里还是需要手动保证这些数是从小到大排布的。

直观上来看运用贪心来处理应该是没问题的，但是贪心的标准不好确定，因为当前区间的取值如果太小，那么与上一个区间取值之差可能太小使得答案不够优，而如果取值太大，则将会压缩后续可用的取数空间。

一种可行的处理方法是二分这个最小差值的最大值，在确定了mid之后，贪心的标准就确定下来了，即在满足相邻数对差大于等于mid的前提下，让当前区间的取数尽量靠前。

更具体的，对于当前二分到的mid，第一个数必然取start[0]，留给后续的选择空间最大。接下来对于第i个数，这里的i > 0，若上一轮的取值x + mid \<\= start[i]，那么这一轮可以直接取start[i]；若x + mid \<\= start[i] + d，那么这一轮就应该取x + mid；若x + mid > start[i] + d，说明本轮没法取值，也就是说无法让最小的差值都大于等于mid。

若存在可行的取数方案，就更新二分的下界为mid，否则更新二分的上界的mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maxPossibleScore(self, start, d):
        """
        :type start: List[int]
        :type d: int
        :rtype: int
        """

        start.sort()

        left = 0
        right = start[-1] + d - start[0]

        while left < right:
            mid = (left + right + 1) // 2
            now = start[0]
            flag = True
            for v in start[1:]:
                if now + mid <= v:
                    now = v
                elif now + mid <= v + d:
                    now += mid
                else:
                    flag = False
                    break
            
            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
```
