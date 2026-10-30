---
title: "2529. 正整数和负整数的最大计数"
aliases: ["yiduobo的每日leetcode 2529.正整数和负整数的最大计数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "leetcode/bian-li", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636898139"
zhihu_id: "636898139"
zhihu_title: "yiduobo的每日leetcode 2529.正整数和负整数的最大计数"
question_id: "2529"
question: "正整数和负整数的最大计数"
problem_url: "https://leetcode.cn/problems/maximum-count-of-positive-integer-and-negative-integer/"
difficulty: "Easy"
created: "2023-06-14T00:17:40+08:00"
updated: "2023-06-14T00:17:40+08:00"
upvotes: 0
comments: 2
---

# 2529. 正整数和负整数的最大计数

> **[yiduobo的每日leetcode 2529.正整数和负整数的最大计数](https://zhuanlan.zhihu.com/p/636898139) · 知乎 · 2023-06-14 · 赞同 0**
> 力扣：[2529. 正整数和负整数的最大计数](https://leetcode.cn/problems/maximum-count-of-positive-integer-and-negative-integer/) · Easy · 灵茶山艾府：[两种方法：遍历 / 二分查找（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2529.正整数和负整数的最大计数

[力扣](https://leetcode.cn/problems/maximum-count-of-positive-integer-and-negative-integer/)

O(n)的做法是很容易想到的，直接一趟遍历统计数组中正数和负数的数量就行了。题目希望得到一个O(log(n))的做法，注意到给出的数组有序，那么很自然联想到使用二分来求解。

首先考虑边界情况。若数组第一个元素为正数，那么说明数组中所有元素都是正数；同样的，若数组最后一个元素为负数，那么说明数组中所有元素都是负数。对于这两种情况，答案都是数组长度。

接下来对于一般情况，则可以通过二分法找到数组中最小的非负数下标，不妨记为p，那么下标在0到p - 1之间的数就都是负数；同样的，也可以通过二分法找到数组中最大的非正数下标，不妨记为q，那么下标在q + 1到n - 1之间的数就都是正数。此时只需取二者的较大值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumCount(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        if nums[0] > 0 or nums[-1] < 0:
            return n
        
        left, right = 0, n - 1
        while left < right:
            mid = (left + right) >> 1
            if nums[mid] >= 0:
                right = mid
            else:
                left = mid + 1
        
        neg = left

        left, right = 0, n - 1
        while left < right:
            mid = (left + right + 1) >> 1
            if nums[mid] <= 0:
                left = mid
            else:
                right = mid - 1
        
        pos = n - 1 - left

        return max(neg, pos)
```
