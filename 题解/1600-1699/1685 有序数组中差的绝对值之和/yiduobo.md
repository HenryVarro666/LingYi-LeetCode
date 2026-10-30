---
title: "1685. 有序数组中差的绝对值之和"
aliases: ["yiduobo的每日leetcode 1685.有序数组中差的绝对值之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/445906805"
zhihu_id: "445906805"
zhihu_title: "yiduobo的每日leetcode 1685.有序数组中差的绝对值之和"
question_id: "1685"
question: "有序数组中差的绝对值之和"
problem_url: "https://leetcode.cn/problems/sum-of-absolute-differences-in-a-sorted-array/"
created: "2021-12-15T23:56:08+08:00"
updated: "2021-12-15T23:56:08+08:00"
upvotes: 0
comments: 0
---

# 1685. 有序数组中差的绝对值之和

> **[yiduobo的每日leetcode 1685.有序数组中差的绝对值之和](https://zhuanlan.zhihu.com/p/445906805) · 知乎 · 2021-12-15 · 赞同 0**
> 力扣：[1685. 有序数组中差的绝对值之和](https://leetcode.cn/problems/sum-of-absolute-differences-in-a-sorted-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1685.有序数组中差的绝对值之和

[力扣](https://leetcode-cn.com/problems/sum-of-absolute-differences-in-a-sorted-array/)

由于题目给出的是排好序的数组，那么可以将计算result的式子中的绝对值符号拆出来，那么result[i]就可以拆分成为两个部分，分别是0到index这一段以及index + 1到n - 1这一段。这两段的值分别为

(nums[i] - nums[0]) + (nums[i] - nums[1]) + ... + (nums[i] - nums[i]) \= nums[i] \* (i + 1) - prefix_s[i]

(nums[i + 1] - nums[i]) + (nums[i + 2] - nums[i]) + ... + (nums[n - 1] - nums[i]) \= suffix_s[i] - nums[i] \* (n - i - 1)

其中prefix_s以及suffix_s分别表示nums的前缀和以及后缀和。由于前缀和与后缀和是可以通过数组的总和互相转化的，因此可以先计算出数组的总和s，然后从头开始一趟扫描，计算当前的前缀和p，并通过p，s以及nums[i]来计算出当前的result[i]。

最后附上python代码：

```python
class Solution(object):
    def getSumAbsoluteDifferences(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        s = sum(nums)
        p = 0
        n = len(nums)
        res = []
        for index, num in enumerate(nums):
            p += num
            res.append(num * (index + 1) - p + (s - p) - num * (n - index - 1))
        
        return res
```
