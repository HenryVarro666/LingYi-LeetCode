---
title: "3010. 将数组分成最小总代价的子数组I"
aliases: ["yiduobo的每日leetcode 3010.将数组分成最小总代价的子数组I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting", "leetcode/bian-li", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693763600"
zhihu_id: "693763600"
zhihu_title: "yiduobo的每日leetcode 3010.将数组分成最小总代价的子数组I"
question_id: "3010"
question: "将数组分成最小总代价的子数组 I"
problem_url: "https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-i/"
difficulty: "Easy"
rating: 1292
created: "2024-04-21T23:42:02+08:00"
updated: "2024-04-21T23:42:02+08:00"
upvotes: 1
comments: 0
---

# 3010. 将数组分成最小总代价的子数组I

> **[yiduobo的每日leetcode 3010.将数组分成最小总代价的子数组I](https://zhuanlan.zhihu.com/p/693763600) · 知乎 · 2024-04-21 · 赞同 1**
> 力扣：[3010. 将数组分成最小总代价的子数组 I](https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-i/) · Easy · 灵茶山艾府：[从 O(nlogn) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3010.将数组分成最小总代价的子数组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-i/description/)

题目对子数组的划分没有任何额外的要求，那么为了让总代价最小，就应该选择最小的两个数作为子数组的起点。于是只需一趟遍历，找出从下标1开始的数中最小的两个，相加后再加上数组的头后返回即可。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        first = second = None
        for v in nums[1:]:
            if first is None or v < first:
                first, second = v, first
            elif second is None or v < second:
                second = v
        
        return nums[0] + first + second
```
