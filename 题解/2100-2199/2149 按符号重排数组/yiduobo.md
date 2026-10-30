---
title: "2149. 按符号重排数组"
aliases: ["yiduobo的每日leetcode 2149.按符号重排数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530376800"
zhihu_id: "530376800"
zhihu_title: "yiduobo的每日leetcode 2149.按符号重排数组"
question_id: "2149"
question: "按符号重排数组"
problem_url: "https://leetcode.cn/problems/rearrange-array-elements-by-sign/"
difficulty: "Medium"
created: "2022-06-17T21:47:52+08:00"
updated: "2022-06-17T21:47:52+08:00"
upvotes: 0
comments: 0
---

# 2149. 按符号重排数组

> **[yiduobo的每日leetcode 2149.按符号重排数组](https://zhuanlan.zhihu.com/p/530376800) · 知乎 · 2022-06-17 · 赞同 0**
> 力扣：[2149. 按符号重排数组](https://leetcode.cn/problems/rearrange-array-elements-by-sign/) · Medium · 灵茶山艾府：[简洁写法 + 一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2149.按符号重排数组

[力扣](https://leetcode.cn/problems/rearrange-array-elements-by-sign/)

使用两个指针p_pos和n_pos分别指向当前答案中下一个正数放置的下标以及下一个负数放置的下标，然后遍历原数组，若当前数为正数，那么将其填充到答案数组p_pos这个位置，然后将p_pos加上2，否则将其填充到答案数组n_pos这个位置，然后将n_pos加上2。

最后附上python代码：

```python
class Solution(object):
    def rearrangeArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        res = [None] * n
        p_pos = 0
        n_pos = 1
        for num in nums:
            if num > 0:
                res[p_pos] = num
                p_pos += 2
            else:
                res[n_pos] = num
                n_pos += 2
        
        return res
```
