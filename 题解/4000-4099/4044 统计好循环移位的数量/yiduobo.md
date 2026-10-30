---
title: "4044. 统计好循环移位的数量"
aliases: ["yiduobo的每日leetcode 4044.统计好循环移位的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2079967842800346286"
zhihu_id: "2079967842800346286"
zhihu_title: "yiduobo的每日leetcode 4044.统计好循环移位的数量"
question_id: "4044"
question: "统计好循环移位的数量"
problem_url: "https://leetcode.cn/problems/count-good-cyclic-rotations/"
difficulty: "Medium"
rating: 1418
created: "2026-09-06T16:29:32+08:00"
updated: "2026-09-06T16:29:32+08:00"
upvotes: 0
comments: 0
---

# 4044. 统计好循环移位的数量

> **[yiduobo的每日leetcode 4044.统计好循环移位的数量](https://zhuanlan.zhihu.com/p/2079967842800346286) · 知乎 · 2026-09-06 · 赞同 0**
> 力扣：[4044. 统计好循环移位的数量](https://leetcode.cn/problems/count-good-cyclic-rotations/) · Medium · 灵茶山艾府：[两种方法：前缀和 / 定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4044.统计好循环移位的数量

<https://leetcode.cn/problems/count-good-cyclic-rotations/description/>

题目给出一个长度为偶数n的整数数组nums。

nums的一次循环移位指的是选择一个长度为0到n - 1的前缀，将其移动到数组的末尾，同时保持所有元素的相对顺序不变。

若依次循环移位后的数组中，前n // 2个元素之和严格大于后n // 2个元素之和，那么就称这个循环移位是好循环移位。

问nums中好循环移位的数量。

题目实际上问的是对于起点到0到n - 1，且长度为n // k的循环子数组中元素之和，是否大于数组总和的一半，因此在这里只需使用一个长度为k \= n // 2的滑动窗口从0到n - 1向后滑动即可。注意这里的滑动窗口也是循环的，也就是右边界超出n - 1之后，需要重新从0开始。

具体实现上，可以将nums复制一份贴在后面，也可以在右边界移动时对n取模。

最后附上python代码：

```python
class Solution(object):
    def countGoodRotations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        k = n // 2
        s = 0
        total = sum(nums)
        for index in range(k):
            s += nums[index]
        
        res = 0
        if s * 2 > total:
            res += 1
        
        for index in range(k, n + k - 1):
            s += nums[index % n]
            s -= nums[index - k]
            if s * 2 > total:
                res += 1
        
        return res
```
