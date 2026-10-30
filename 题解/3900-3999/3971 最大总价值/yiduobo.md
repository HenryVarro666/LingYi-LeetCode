---
title: "3971. 最大总价值"
aliases: ["yiduobo的每日leetcode 3971.最大总价值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2054000636321178404"
zhihu_id: "2054000636321178404"
zhihu_title: "yiduobo的每日leetcode 3971.最大总价值"
question_id: "3971"
question: "最大总价值"
problem_url: "https://leetcode.cn/problems/maximum-total-value/"
difficulty: "Hard"
rating: 2195
created: "2026-06-27T00:47:41+08:00"
updated: "2026-06-27T00:47:42+08:00"
upvotes: 1
comments: 0
---

# 3971. 最大总价值

> **[yiduobo的每日leetcode 3971.最大总价值](https://zhuanlan.zhihu.com/p/2054000636321178404) · 知乎 · 2026-06-27 · 赞同 1**
> 力扣：[3971. 最大总价值](https://leetcode.cn/problems/maximum-total-value/) · Hard · 灵茶山艾府：[二分第 m 大价值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3971.最大总价值

<https://leetcode.cn/problems/maximum-total-value/description/>

题目给出两个正整数数组value和decay，以及一个正整数m。数组的长度不超过10^5，其中元素的大小以及m都不超过10^9。

现在要求执行至多m次操作，每次操作中，需要选择一个下标index，将当前的value[index]累加到总价值中，然后将value[index]减去decay[index]。

问最大可能获得的总价值是多少，答案对10^9 + 7取模。

首先可以明确的是，每次操作都应该选择当前剩余的最大的正整数，不过本题的数据规模很大，直接模拟是行不通的，必须想办法进行优化。

在这里不妨考虑最后一次添加到总价值中的元素值，这个值越小，可能执行的操作次数就越多，反之若这个值越大，可能执行的操作次数就越少。换言之，在这里可以直接二分这个最小元素值。

二分的下界自然为0，而上界则是value中的最大值。对于当前二分到的值mid，只需遍历原始的value，对于每个value[index]，计算在衰减量为decay[index]的前提下需要多少次操作才会让value[index]小于mid，并统计操作次数之和。若总的操作次数够多，说明需要调整二分的下界，否则需要调整二分的上界。

通过二分确定下这个值之后，就可以通过等差数列求和计算出每个value[index]不断执行操作直到小于这个值时可以得到的价值并累加起来即可。

需要特别注意的是，这样可能导致最终这个最小值被计算多次，因此还需要统计一共执行的操作次数，将超出m的次数带来的价值和从最终答案中减去。

最后附上python代码：

```python
class Solution(object):
    def maxTotalValue(self, value, decay, m):
        """
        :type value: List[int]
        :type decay: List[int]
        :type m: int
        :rtype: int
        """
        
        left = 0
        right = max(value)

        while left < right:
            mid = (left + right + 1) // 2
            cnt = 0
            for v, d in zip(value, decay):
                if v >= mid:
                    delta = v - mid
                    cnt += delta // d + 1
                    if cnt >= m:
                        break

            if cnt >= m:
                left = mid
            else:
                right = mid - 1
        
        mod = 10 ** 9 + 7
        res = 0
        cnt = 0
        for v, d in zip(value, decay):
            if v >= left:
                delta = v - left
                x = delta // d + 1
                cnt += x
                res = (res + (v + v - d * (x - 1)) * x // 2) % mod

        res = (res - (cnt - m) * left % mod + mod) % mod
        return res
```
