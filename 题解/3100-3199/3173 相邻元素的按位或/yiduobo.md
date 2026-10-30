---
title: "3173. 相邻元素的按位或"
aliases: ["yiduobo的每日leetcode 3173.相邻元素的按位或"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705432227"
zhihu_id: "705432227"
zhihu_title: "yiduobo的每日leetcode 3173.相邻元素的按位或"
question_id: "3173"
question: "相邻元素的按位或"
problem_url: "https://leetcode.cn/problems/bitwise-or-of-adjacent-elements/"
created: "2024-06-26T00:00:51+08:00"
updated: "2024-06-26T00:00:51+08:00"
upvotes: 0
comments: 0
---

# 3173. 相邻元素的按位或

> **[yiduobo的每日leetcode 3173.相邻元素的按位或](https://zhuanlan.zhihu.com/p/705432227) · 知乎 · 2024-06-26 · 赞同 0**
> 力扣：[3173. 相邻元素的按位或](https://leetcode.cn/problems/bitwise-or-of-adjacent-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3173.相邻元素的按位或

[. - 力扣（LeetCode）](https://leetcode.cn/problems/bitwise-or-of-adjacent-elements/description/)

题目给出一个数组nums，要求计算其中下标相邻元素间按位或的结果。

按照题目要求从下标1开始向后遍历，将当前元素与上一个元素按位或的结果加入到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def orArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        return [nums[index] | nums[index - 1] for index in range(1, len(nums))]
```
