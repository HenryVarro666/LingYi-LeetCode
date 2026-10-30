---
title: "1984. 学生分数的最小差值"
aliases: ["yiduobo的每日leetcode 1984.学生分数的最小差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/498735359"
zhihu_id: "498735359"
zhihu_title: "yiduobo的每日leetcode 1984.学生分数的最小差值"
question_id: "1984"
question: "学生分数的最小差值"
problem_url: "https://leetcode.cn/problems/minimum-difference-between-highest-and-lowest-of-k-scores/"
difficulty: "Easy"
rating: 1306
created: "2022-04-14T22:03:30+08:00"
updated: "2022-04-14T22:03:30+08:00"
upvotes: 0
comments: 0
---

# 1984. 学生分数的最小差值

> **[yiduobo的每日leetcode 1984.学生分数的最小差值](https://zhuanlan.zhihu.com/p/498735359) · 知乎 · 2022-04-14 · 赞同 0**
> 力扣：[1984. 学生分数的最小差值](https://leetcode.cn/problems/minimum-difference-between-highest-and-lowest-of-k-scores/) · Easy · 灵茶山艾府：[贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1984.学生分数的最小差值

[力扣](https://leetcode-cn.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/)

为了使得这个差值最小，那么答案必然出现在分数连续的k个学生中，于是可以将数组从小到大进行排序，然后使用一个大小为k的滑动窗口从头开始向后移动，并根据窗口头尾两个分数的差值来更新答案。

最后附上python代码：

```python
class Solution(object):
    def minimumDifference(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = sorted(nums)
        res = nums[k - 1] - nums[0]
        for index in range(k, len(nums)):
            res = min(res, nums[index] - nums[index - k + 1])
        
        return res
```
