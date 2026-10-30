---
title: "2557. 从一个范围内选择最多整数II"
aliases: ["yiduobo的每日leetcode 2557.从一个范围内选择最多整数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638960044"
zhihu_id: "638960044"
zhihu_title: "yiduobo的每日leetcode 2557.从一个范围内选择最多整数II"
question_id: "2557"
question: "从一个范围内选择最多整数II"
problem_url: "https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-ii/"
created: "2023-06-27T20:59:51+08:00"
updated: "2023-06-27T20:59:51+08:00"
upvotes: 0
comments: 0
---

# 2557. 从一个范围内选择最多整数II

> **[yiduobo的每日leetcode 2557.从一个范围内选择最多整数II](https://zhuanlan.zhihu.com/p/638960044) · 知乎 · 2023-06-27 · 赞同 0**
> 力扣：[2557. 从一个范围内选择最多整数II](https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2557.从一个范围内选择最多整数II

[力扣](https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-ii/)

之前的2554题的升级版

[yiduobo：yiduobo的每日leetcode 2554.从一个范围内选择最多整数I](https://zhuanlan.zhihu.com/p/638958222)

由于数据规模的变大了，因此不能再继续使用暴力算法，但是贪心的思路还是一样的，从1开始尽量选择小的且没有被ban的数字。另一方面，如果最终答案越大，其包含的数字和也就越大，因此在这里可以二分答案。

对于当前二分到的mid，选择的数字就应该是处于1到mid之间，且没有被ban的所有数字。这些数字的和则可以通过求和公式(1 + mid) \* mid / 2，再减去1到mid中被ban掉的数字之和得到。

而对于被ban掉的数字之和，则可以先将被ban掉的数字去重后排序得到有序的被ban数组，然后在其中二分mid，找出被ban数组中小于等于mid的最大值的下标p，那么需要减去的数就是被ban数组的一个前缀，只需预处理出这个数组的前缀和，就可以高效地得知1到mid中被ban数字之和是多少了。

最后附上python代码：

```python
class Solution(object):
    def maxCount(self, banned, n, maxSum):
        """
        :type banned: List[int]
        :type n: int
        :type maxSum: int
        :rtype: int
        """

        banned = sorted(set(banned))
        pre_s = [0]
        for v in banned:
            pre_s.append(pre_s[-1] + v)

        def get_ban(v):
            if v < banned[0]:
                return 0

            left = 0
            right = len(banned) - 1
            while left < right:
                mid = (left + right + 1) / 2
                if v >= banned[mid]:
                    left = mid
                else:
                    right = mid - 1
            
            return left + 1

        left = 0
        right = n
        while left < right:
            mid = (left + right + 1) / 2
            s = (1 + mid) * mid / 2 - pre_s[get_ban(mid)]

            if s <= maxSum:
                left = mid
            else:
                right = mid - 1
        
        return left - get_ban(left)
```
