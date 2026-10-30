---
title: "3107. 使数组中位数等于K的最少操作数"
aliases: ["yiduobo的每日leetcode 3107.使数组中位数等于K的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700395522"
zhihu_id: "700395522"
zhihu_title: "yiduobo的每日leetcode 3107.使数组中位数等于K的最少操作数"
question_id: "3107"
question: "使数组中位数等于 K 的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-median-of-array-equal-to-k/"
difficulty: "Medium"
rating: 1605
created: "2024-05-29T00:26:10+08:00"
updated: "2024-05-29T00:26:10+08:00"
upvotes: 0
comments: 0
---

# 3107. 使数组中位数等于K的最少操作数

> **[yiduobo的每日leetcode 3107.使数组中位数等于K的最少操作数](https://zhuanlan.zhihu.com/p/700395522) · 知乎 · 2024-05-29 · 赞同 0**
> 力扣：[3107. 使数组中位数等于 K 的最少操作数](https://leetcode.cn/problems/minimum-operations-to-make-median-of-array-equal-to-k/) · Medium · 灵茶山艾府：[排序（附思考题）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3107.使数组中位数等于K的最少操作数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-median-of-array-equal-to-k/description/)

题目给出一个数组nums以及一个整数k，每次操作可以将数组中的任意数加上1或者减去1，要求以最小的代价使得数组的中位数变为k。

由于要满足的是中位数等于k，因此可以先将数组从小到大进行排序，此时的中位数就是nums[n // 2]。接下来：

1、若nums[n // 2]小于k：

此时nums[n // 2]左侧的所有整数都小于k，而为了使得数组的中位数变为k，就必须通过操作从中得到一个k，而最小的代价就是直接将nums[n // 2]变为k。另一方面，nums[n // 2]后方的整数也可能小于k，因此还需要将后面所有小于k整数都变为k，因此只需遍历数组的后半部分，计算将其中所有小于k的整数变为k的代价并累加即可。

2、若nums[n // 2]大于k：

与情况1对称，此时只需遍历数组的前半部分，计算将其中所有大于k的整数变为k的代价并累加即可。

3、若nums[n // 2]等于k：

此时无需操作，答案为0。

最后附上python代码：

```python
class Solution(object):
    def minOperationsToMakeMedianK(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums.sort()
        n = len(nums)
        
        res = 0

        if nums[n // 2] < k:
            for v in nums[n // 2:]:
                res += max(k - v, 0)
        elif nums[n // 2] > k:
            for v in nums[:n // 2 + 1]:
                res += max(v - k, 0)
        
        return res
```
