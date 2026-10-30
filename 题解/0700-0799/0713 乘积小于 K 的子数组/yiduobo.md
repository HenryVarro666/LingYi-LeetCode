---
title: "713. 乘积小于K的子数组"
aliases: ["yiduobo的每日leetcode 713.乘积小于K的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "leetcode/shi-pin", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/329006429"
zhihu_id: "329006429"
zhihu_title: "yiduobo的每日leetcode 713.乘积小于K的子数组"
question_id: "713"
question: "乘积小于 K 的子数组"
problem_url: "https://leetcode.cn/problems/subarray-product-less-than-k/"
difficulty: "Medium"
created: "2020-12-03T23:21:29+08:00"
updated: "2020-12-03T23:21:29+08:00"
upvotes: 0
comments: 0
---

# 713. 乘积小于K的子数组

> **[yiduobo的每日leetcode 713.乘积小于K的子数组](https://zhuanlan.zhihu.com/p/329006429) · 知乎 · 2020-12-03 · 赞同 0**
> 力扣：[713. 乘积小于 K 的子数组](https://leetcode.cn/problems/subarray-product-less-than-k/) · Medium · 灵茶山艾府：[【视频讲解】越短越合法型滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

713.乘积小于K的子数组

[力扣](https://leetcode-cn.com/problems/subarray-product-less-than-k/)

首先，题目给出的数组元素都是正数，因此当k小于等于1时，答案必然是0。

注意到题目要求的是连续子数组，因此可以使用滑动窗口来做。维护两个指针left和right，每次将right往右移动一位，若当前left到right这一段的乘积大于等于k，那么就将left往右移动直到乘积小于k。此时就得到以right结尾的乘积小于k的子数组一共有right - left + 1个，因此将答案加上right - left + 1，然后继续将right往右移动直到末尾。

最后附上python代码：

```python
class Solution(object):
    def numSubarrayProductLessThanK(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        if k <= 1:
            return 0

        n = len(nums)
        now = 1
        p = 0
        res = 0

        for index in range(n):
            now *= nums[index]
            while now >= k:
                now /= nums[p]
                p += 1
            res += index - p + 1

        return res
```
