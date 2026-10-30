---
title: "1099. 小于K的两数之和"
aliases: ["yiduobo的每日leetcode 1099.小于K的两数之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609267870"
zhihu_id: "609267870"
zhihu_title: "yiduobo的每日leetcode 1099.小于K的两数之和"
question_id: "1099"
question: "小于K的两数之和"
problem_url: "https://leetcode.cn/problems/two-sum-less-than-k/"
created: "2023-02-24T23:42:22+08:00"
updated: "2023-02-24T23:42:22+08:00"
upvotes: 0
comments: 0
---

# 1099. 小于K的两数之和

> **[yiduobo的每日leetcode 1099.小于K的两数之和](https://zhuanlan.zhihu.com/p/609267870) · 知乎 · 2023-02-24 · 赞同 0**
> 力扣：[1099. 小于K的两数之和](https://leetcode.cn/problems/two-sum-less-than-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1099.小于K的两数之和

[力扣](https://leetcode.cn/problems/two-sum-less-than-k/)

又回到了两数之和问题。直接使用第一题中的处理方法，排序后双指针从两侧往中间扫进行了。

最后附上python代码：

```python
class Solution(object):
    def twoSumLessThanK(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums.sort()

        left = 0
        right = len(nums) - 1
        res = -1
        while left < right:
            if nums[left] + nums[right] < k:
                res = max(res, nums[left] + nums[right])
                left += 1
            else:
                right -= 1
        
        return res
```
