---
title: "4031. 找到所有数组中消失的数字II"
aliases: ["yiduobo的每日leetcode 4031.找到所有数组中消失的数字II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077564683335243201"
zhihu_id: "2077564683335243201"
zhihu_title: "yiduobo的每日leetcode 4031.找到所有数组中消失的数字II"
question_id: "4031"
question: "找到所有数组中消失的数字 II"
problem_url: "https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/"
difficulty: "Medium"
created: "2026-08-31T01:26:13+08:00"
updated: "2026-08-31T01:26:16+08:00"
upvotes: 0
comments: 0
---

# 4031. 找到所有数组中消失的数字II

> **[yiduobo的每日leetcode 4031.找到所有数组中消失的数字II](https://zhuanlan.zhihu.com/p/2077564683335243201) · 知乎 · 2026-08-31 · 赞同 0**
> 力扣：[4031. 找到所有数组中消失的数字 II](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/) · Medium · 灵茶山艾府：[用哨兵简化代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4031.找到所有数组中消失的数字II

<https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array-ii/description/>

题目给出一个整数数组nums，以及两个整数lower和upper。

若某个整数位于区间[lower, upper]内，且没有出现在nums中，则称其为缺失整数。

要求返回一个二维整数数组，其中每个元素的形式为[start, end]，表示一段有连续的缺失整数构成的区间。所有的连续缺失整数必须构成一个大的区间。

要求按照递增的顺序返回这些区间。若没有缺失整数，则返回空数组。

首先处理特殊情况。若nums中的最大值小于lower，或者nums中的最小值大于upper，那么整个[lower, upper]中的所有元素就都不可能在nums中出现，因此对于这两种情况，可以直接返回[lower, upper]。

接下来考虑一般情况。此时可以明确的是，nums[p]中至少存在一个大于等于lower且小于等于upper的元素，也就是说nums中的某些元素将对[lower, upper]进行若干次的切分。那么在这里就可以先将nums从小到大进行排序，然后一趟遍历，找出最小的满足nums[p] >\= lower的下标p。得到p之后，从lower到nums[p] - 1这一段都没有在nums中出现，因此可以将[lower, nums[p] - 1]加入到答案中。需要注意，这里还有一个前提条件，就是这一段的长度必须大于0。

接下来，则可以考虑nums[p]、nums[p + 1]以及upper之间的关系。若nums[p + 1]还没有越过upper，那么nums[p] + 1到nums[p + 1] - 1这一段就依然落在lower到upper之间，且其中的元素不会在nums中出现，因此在这里可以将[nums[p] + 1, nums[p + 1] - 1]加入到答案中。当然，在这里依然需要满足这一段的长度大于0才能加入到答案中。处理完nums[p]到nums[p + 1]这一段之后，可以将p向后移动一位，然后继续考虑新的nums[p]以及nums[p + 1]，直到右边界越过了upper，或者到达nums的末尾为止。

若此时的nums[p]还没有超过upper，则还需要将[nums[p] + 1, upper]这一段加入到答案中。在这里也别忘了检测区间长度是否大于0。

基于以上方法生成的区间天然就是有序的，因此可以直接返回答案数组。

最后附上python代码：

```python
class Solution(object):
    def findDisappearedNumbers(self, nums, lower, upper):
        """
        :type nums: List[int]
        :type lower: int
        :type upper: int
        :rtype: List[List[int]]
        """
        
        nums.sort()
        p = 0
        while p < len(nums) and nums[p] < lower:
            p += 1
        
        if p == len(nums):
            return [[lower, upper]]
        
        if nums[p] > upper:
            return [[lower, upper]]
        
        res = []
        if lower < nums[p]:
            res.append([lower, nums[p] - 1])
        
        while p + 1 < len(nums) and nums[p + 1] <= upper:
            if nums[p + 1] - nums[p] > 1:
                res.append([nums[p] + 1, nums[p + 1] - 1])
            p += 1
        
        if nums[p] < upper:
            res.append([nums[p] + 1, upper])
        
        return res
```
