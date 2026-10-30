---
title: "414. 第三大的数"
aliases: ["yiduobo的每日leetcode 414.第三大的数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/188735239"
zhihu_id: "188735239"
zhihu_title: "yiduobo的每日leetcode 414.第三大的数"
question_id: "414"
question: "第三大的数"
problem_url: "https://leetcode.cn/problems/third-maximum-number/"
created: "2020-08-18T21:36:41+08:00"
updated: "2020-08-18T21:36:41+08:00"
upvotes: 0
comments: 0
---

# 414. 第三大的数

> **[yiduobo的每日leetcode 414.第三大的数](https://zhuanlan.zhihu.com/p/188735239) · 知乎 · 2020-08-18 · 赞同 0**
> 力扣：[414. 第三大的数](https://leetcode.cn/problems/third-maximum-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

414.第三大的数<https://leetcode-cn.com/problems/third-maximum-number/>

比较基础的题目。一趟扫描，维护住这三个数即可。

最后附上python代码：

```python
class Solution(object):
    def thirdMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        first = nums[0]
        second = third = None
        pos = 1
        while pos < len(nums) and nums[pos] == first:
            pos += 1
        if pos == len(nums):
            return first

        if nums[pos] < first:
            second = nums[pos]
        else:
            second = first
            first = nums[pos]

        for num in nums[pos + 1:]:
            if num == first or num == second:
                continue
            if num > first:
                third = second
                second = first
                first = num
            elif num > second:
                third = second
                second = num
            elif third is None or num > third:
                third = num

        if third is None:
            return first
        
        return third
```
