---
title: "3925. 连接逆序数组"
aliases: ["yiduobo的每日leetcode 3925.连接逆序数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2038052816187611029"
zhihu_id: "2038052816187611029"
zhihu_title: "yiduobo的每日leetcode 3925.连接逆序数组"
question_id: "3925"
question: "连接逆序数组"
problem_url: "https://leetcode.cn/problems/concatenate-array-with-reverse/"
difficulty: "Easy"
created: "2026-05-14T00:29:36+08:00"
updated: "2026-05-14T00:29:37+08:00"
upvotes: 2
comments: 0
---

# 3925. 连接逆序数组

> **[yiduobo的每日leetcode 3925.连接逆序数组](https://zhuanlan.zhihu.com/p/2038052816187611029) · 知乎 · 2026-05-14 · 赞同 2**
> 力扣：[3925. 连接逆序数组](https://leetcode.cn/problems/concatenate-array-with-reverse/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3925.连接逆序数组

<https://leetcode.cn/problems/concatenate-array-with-reverse/description/>

题目给出一个长度为n的整数数组nums。现在要求构造一个长度为2 \* n的数组ans，其中前n个元素与nums相同，后n个元素为nums的逆序。

直接按照题目要求，将nums反转后拼接在nums后方就行了。

最后附上python代码：

```python
class Solution(object):
    def concatWithReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        return nums + nums[::-1]
```
