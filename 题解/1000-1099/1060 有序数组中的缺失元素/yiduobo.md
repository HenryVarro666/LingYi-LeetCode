---
title: "1060. 有序数组中的缺失元素"
aliases: ["yiduobo的每日leetcode 1060.有序数组中的缺失元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607483460"
zhihu_id: "607483460"
zhihu_title: "yiduobo的每日leetcode 1060.有序数组中的缺失元素"
question_id: "1060"
question: "有序数组中的缺失元素"
problem_url: "https://leetcode.cn/problems/missing-element-in-sorted-array/"
created: "2023-02-18T20:29:42+08:00"
updated: "2023-02-18T20:29:42+08:00"
upvotes: 1
comments: 0
---

# 1060. 有序数组中的缺失元素

> **[yiduobo的每日leetcode 1060.有序数组中的缺失元素](https://zhuanlan.zhihu.com/p/607483460) · 知乎 · 2023-02-18 · 赞同 1**
> 力扣：[1060. 有序数组中的缺失元素](https://leetcode.cn/problems/missing-element-in-sorted-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1060.有序数组中的缺失元素

[力扣](https://leetcode.cn/problems/missing-element-in-sorted-array/)

首先可以明确的是，一个长度为n的有序数组nums，其中最小值和最大值分别为nums[0]以及nums[n - 1]，那么理想情况下应该有从nums[0]到nums[n - 1]这一共nums[n - 1] - nums[0] + 1个元素，但是实际上一共只有n个元素，因此最终缺失的元素数量就是nums[n - 1] - nums[0] + 1 - n。

有了这个结论，若k > nums[n - 1] - nums[0] + 1 - n，那么缺失的第k个元素是在nums[n - 1]右侧的，具体为nums[n - 1] + (k - (nums[-1] - nums[0] + 1 - n))。

反之，若k \<\= nums[n - 1] - nums[0] + 1 - n，说明最终答案就位于nums[0]到nums[n - 1]之间。接下来的问题就可以转化为找出位置p，满足nums[0]到nums[p]之间的缺失元素数量小于k，且nums[0]到nums[p + 1]之间的缺失元素数量大于等于k。

对于这个问题，则可以利用二分查找来进行处理。具体来说，就是二分这个p，依然是通过最上面的结论计算nums[0]到nums[p]之间有多少个缺失的元素，然后通过这个缺失的数量来调整二分的上下界。得到p之后，最终答案就是nums[p] + (k - (nums[p] - nums[0] + 1 - (p + 1))。

最后附上python代码：

```python
class Solution(object):
    def missingElement(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        if k > (nums[-1] - nums[0] + 1 - n):
            k -= (nums[-1] - nums[0] + 1 - n)
            return nums[-1] + k
        
        left = 0
        right = n - 1
        while left < right:
            mid = (left + right + 1) / 2
            cnt = nums[mid] - nums[0] + 1 - (mid + 1)
            if cnt < k:
                left = mid
            else:
                right = mid - 1

        return nums[left] + k - (nums[left] - nums[0] + 1 - (left + 1))
```
