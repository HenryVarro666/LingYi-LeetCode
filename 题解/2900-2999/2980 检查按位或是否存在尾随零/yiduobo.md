---
title: "2980. 检查按位或是否存在尾随零"
aliases: ["yiduobo的每日leetcode 2980.检查按位或是否存在尾随零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692357015"
zhihu_id: "692357015"
zhihu_title: "yiduobo的每日leetcode 2980.检查按位或是否存在尾随零"
question_id: "2980"
question: "检查按位或是否存在尾随零"
problem_url: "https://leetcode.cn/problems/check-if-bitwise-or-has-trailing-zeros/"
difficulty: "Easy"
rating: 1234
created: "2024-04-14T02:02:18+08:00"
updated: "2024-04-14T02:02:18+08:00"
upvotes: 1
comments: 0
---

# 2980. 检查按位或是否存在尾随零

> **[yiduobo的每日leetcode 2980.检查按位或是否存在尾随零](https://zhuanlan.zhihu.com/p/692357015) · 知乎 · 2024-04-14 · 赞同 1**
> 力扣：[2980. 检查按位或是否存在尾随零](https://leetcode.cn/problems/check-if-bitwise-or-has-trailing-zeros/) · Easy · 灵茶山艾府：[判断是否有至少两个偶数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2980.检查按位或是否存在尾随零

[. - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-bitwise-or-has-trailing-zeros/)

由于题目中的是按位或运算，那么只要有一个奇数参与了运算，结果的最后这一位就必然为一。为了让末尾为零，就只能选出若干个偶数来进行计算，也就是说数组中必须存在至少两个偶数。于是只需一趟遍历，检测数组中偶数的数量是否大于等于两个即可。

最后附上python代码：

```python
class Solution(object):
    def hasTrailingZeros(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        even = 0
        for v in nums:
            if v % 2 == 0:
                even += 1
        
        return even >= 2
```
