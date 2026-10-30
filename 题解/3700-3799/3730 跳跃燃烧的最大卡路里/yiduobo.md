---
title: "3730. 跳跃燃烧的最大卡路里"
aliases: ["yiduobo的每日leetcode 3730.跳跃燃烧的最大卡路里"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968465587219990171"
zhihu_id: "1968465587219990171"
zhihu_title: "yiduobo的每日leetcode 3730.跳跃燃烧的最大卡路里"
question_id: "3730"
question: "跳跃燃烧的最大卡路里"
problem_url: "https://leetcode.cn/problems/maximum-calories-burnt-from-jumps/"
created: "2025-11-03T02:32:08+08:00"
updated: "2025-11-03T02:32:09+08:00"
upvotes: 2
comments: 0
---

# 3730. 跳跃燃烧的最大卡路里

> **[yiduobo的每日leetcode 3730.跳跃燃烧的最大卡路里](https://zhuanlan.zhihu.com/p/1968465587219990171) · 知乎 · 2025-11-03 · 赞同 2**
> 力扣：[3730. 跳跃燃烧的最大卡路里](https://leetcode.cn/problems/maximum-calories-burnt-from-jumps/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3730.跳跃燃烧的最大卡路里

[3730. 跳跃燃烧的最大卡路里 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-calories-burnt-from-jumps/description/)

题目给出一个长度为n的整数数组heights，其中heights[index]表示训练计划中第index个块的高度。现在要求从地面开始，按任意顺序跳到每个方块上。每个方块只能跳一次，且一旦开始，就不能再跳回到地面上。

从一个高度为a的方块起跳到另一个高度为b的方块，所消耗的卡路里为(a - b)^2，最开始的这次跳跃所消耗的卡路里则为x^2，其中x是首次跳跃的目标方块。

问选择最优的跳跃顺序可以燃烧的最大总卡路里。

为了让最终答案最大，直观感觉上就应该让每一步的跨度都尽可能大，所以应该将这些方块按照最大-最小-最大-最小的顺序排布。虽然不知道怎么给出严谨的证明，但是也没有找到反例。于是只需按照高度从小到大进行排序，然后两个指针left和right分别从两侧向中间扫，每一轮先跳到right对应的方块，然后令right向左移动，再跳到left对应的方块，再令left向左移动，直到使用完所有方块为止。

最后附上python代码：

```python
class Solution(object):
    def maxCaloriesBurnt(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        
        heights.sort()
        left, right = 0, len(heights) - 1
        res = 0
        pre = 0
        while left <= right:
            res += (heights[right] - pre) ** 2
            pre = heights[right]
            right -= 1
            if left <= right:
                res += (heights[left] - pre) ** 2
                pre = heights[left]
                left += 1
        
        return res
```
