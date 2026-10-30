---
title: "2226. 每个小孩最多能分到多少糖果"
aliases: ["yiduobo的每日leetcode 2226.每个小孩最多能分到多少糖果"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/543264736"
zhihu_id: "543264736"
zhihu_title: "yiduobo的每日leetcode 2226.每个小孩最多能分到多少糖果"
question_id: "2226"
question: "每个小孩最多能分到多少糖果"
problem_url: "https://leetcode.cn/problems/maximum-candies-allocated-to-k-children/"
difficulty: "Medium"
rating: 1646
created: "2022-07-19T00:14:47+08:00"
updated: "2022-07-19T00:14:47+08:00"
upvotes: 0
comments: 0
---

# 2226. 每个小孩最多能分到多少糖果

> **[yiduobo的每日leetcode 2226.每个小孩最多能分到多少糖果](https://zhuanlan.zhihu.com/p/543264736) · 知乎 · 2022-07-19 · 赞同 0**
> 力扣：[2226. 每个小孩最多能分到多少糖果](https://leetcode.cn/problems/maximum-candies-allocated-to-k-children/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2226.每个小孩最多能分到多少糖果

[力扣](https://leetcode.cn/problems/maximum-candies-allocated-to-k-children/)

本题的各种变形在leetcode已经见过不下三次了，做法还是老样子，直接二分答案。

虽然每个小孩分的糖果数变多，可以分的份数必然是变少的，反过来也一样，因此满足使用二分的条件。二分的下界自然是0，而上界则是candies中的最大值。接下来执行二分，计算每堆糖果可以分给几个小朋友，并判断按当前的分法是否能够满足k个小朋友，从而调整二分的上下界。

最后附上python代码：

```python
class Solution(object):
    def maximumCandies(self, candies, k):
        """
        :type candies: List[int]
        :type k: int
        :rtype: int
        """

        l = 0
        r = max(candies)

        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 0
            for candy in candies:
                cnt += candy / mid
            
            if cnt >= k:
                l = mid
            else:
                r = mid - 1
        
        return l
```
