---
title: "3024. 三角形类型"
aliases: ["yiduobo的每日leetcode 3024.三角形类型"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694929139"
zhihu_id: "694929139"
zhihu_title: "yiduobo的每日leetcode 3024.三角形类型"
question_id: "3024"
question: "三角形类型"
problem_url: "https://leetcode.cn/problems/type-of-triangle/"
difficulty: "Easy"
created: "2024-04-28T00:49:50+08:00"
updated: "2024-04-28T00:49:50+08:00"
upvotes: 1
comments: 0
---

# 3024. 三角形类型

> **[yiduobo的每日leetcode 3024.三角形类型](https://zhuanlan.zhihu.com/p/694929139) · 知乎 · 2024-04-28 · 赞同 1**
> 力扣：[3024. 三角形类型](https://leetcode.cn/problems/type-of-triangle/) · Easy · 灵茶山艾府：[用排序简化代码逻辑（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3024.三角形类型

[. - 力扣（LeetCode）](https://leetcode.cn/problems/type-of-triangle/description/)

先通过两短边之和是否大于第三边判断能否形成三角形，如果不是，返回none

接下来，判断是否为等边三角形，如果是，返回equilateral

最后，判断是否为等腰三角形，如果是，返回isosceles

如果都不满足，就返回scalene

最后附上python代码：

```python
class Solution(object):
    def triangleType(self, nums):
        """
        :type nums: List[int]
        :rtype: str
        """

        nums.sort()
        if nums[0] + nums[1] <= nums[2]:
            return "none"
        
        if nums[0] == nums[1]:
            if nums[0] == nums[2]:
                return "equilateral"
            else:
                return "isosceles"
        elif nums[0] == nums[2] or nums[1] == nums[2]:
            return "isosceles"
        else:
            return "scalene"
```
