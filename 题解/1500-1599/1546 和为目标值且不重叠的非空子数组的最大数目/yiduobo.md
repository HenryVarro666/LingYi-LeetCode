---
title: "1546. 和为目标值且不重叠的非空子数组的最大数目"
aliases: ["yiduobo的每日leetcode 1546.和为目标值且不重叠的非空子数组的最大数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424984773"
zhihu_id: "424984773"
zhihu_title: "yiduobo的每日leetcode 1546.和为目标值且不重叠的非空子数组的最大数目"
question_id: "1546"
question: "和为目标值且不重叠的非空子数组的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/"
created: "2021-10-24T11:26:31+08:00"
updated: "2021-10-24T11:26:31+08:00"
upvotes: 0
comments: 0
---

# 1546. 和为目标值且不重叠的非空子数组的最大数目

> **[yiduobo的每日leetcode 1546.和为目标值且不重叠的非空子数组的最大数目](https://zhuanlan.zhihu.com/p/424984773) · 知乎 · 2021-10-24 · 赞同 0**
> 力扣：[1546. 和为目标值且不重叠的非空子数组的最大数目](https://leetcode.cn/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1546.和为目标值且不重叠的非空子数组的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/)

由于在这里对子数组的长度并没有要求，也就是说如果按照从头到尾扫描的做法，那么对于两个存在重叠部分的合法的子数组而言，显然应该保留下靠前的那一个，这样的话就给后续的选择留下了更多的可能性。

而对于数组和匹配目标值的问题，经典做法还是前缀和加上哈希表，那么现在就有了一种做法：从头开始向后一趟扫描，计算当前的前缀和now。

若当前的now - target出现在哈希表中，那么此时应该将答案加上1，然后将now清零，将哈希表清空。这里清零清空的目的是为了避免子数组之间重叠。

若now - target未出现在哈希表中，那么将now加入到哈希表中。

最后附上python代码：

```python
class Solution(object):
    def maxNonOverlapping(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        n = len(nums)
        pos = 0
        res = 0
        while pos < n:
            s = set([0])
            now = 0
            while pos < n:
                now += nums[pos]
                pos += 1
                if now - target in s:
                    res += 1
                    break
                
                s.add(now)
        
        return res
```
