---
title: "1991. 找到数组的中间位置"
aliases: ["yiduobo的每日leetcode 1991.找到数组的中间位置"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/499687076"
zhihu_id: "499687076"
zhihu_title: "yiduobo的每日leetcode 1991.找到数组的中间位置"
question_id: "1991"
question: "找到数组的中间位置"
problem_url: "https://leetcode.cn/problems/find-the-middle-index-in-array/"
difficulty: "Easy"
created: "2022-04-16T16:54:09+08:00"
updated: "2022-04-16T16:54:09+08:00"
upvotes: 0
comments: 0
---

# 1991. 找到数组的中间位置

> **[yiduobo的每日leetcode 1991.找到数组的中间位置](https://zhuanlan.zhihu.com/p/499687076) · 知乎 · 2022-04-16 · 赞同 0**
> 力扣：[1991. 找到数组的中间位置](https://leetcode.cn/problems/find-the-middle-index-in-array/) · Easy · 灵茶山艾府：[简洁写法，O(1) 额外空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1991.找到数组的中间位置

[力扣](https://leetcode-cn.com/problems/find-the-middle-index-in-array/)

题目要求找到一个位置将数组切分成两半，这两半之和必须相等。

一个自然的想法就是枚举这个分割点，然后判断两半之和是否相等。对于前半部分之和，可以在枚举的过程中不断累加，而对于后半部分之和，则可以通过数组总和，减去前半部分之和以及分割点的值来得到。若在这个过程中找到了前后相等的分割点，那么该点就是最终答案。若一直没能找到，那么答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def findMiddleIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = 0
        s = sum(nums)
        for index in range(len(nums)):
            if now == s - nums[index] - now:
                return index
            
            now += nums[index]
        
        return -1
```
