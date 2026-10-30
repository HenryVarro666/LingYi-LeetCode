---
title: "2839. 判断通过操作能否让字符串相等I"
aliases: ["yiduobo的每日leetcode 2839.判断通过操作能否让字符串相等I"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659687627"
zhihu_id: "659687627"
zhihu_title: "yiduobo的每日leetcode 2839.判断通过操作能否让字符串相等I"
question_id: "2839"
question: "判断通过操作能否让字符串相等 I"
problem_url: "https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-i/"
difficulty: "Easy"
created: "2023-10-06T02:56:51+08:00"
updated: "2023-10-06T02:56:51+08:00"
upvotes: 0
comments: 0
---

# 2839. 判断通过操作能否让字符串相等I

> **[yiduobo的每日leetcode 2839.判断通过操作能否让字符串相等I](https://zhuanlan.zhihu.com/p/659687627) · 知乎 · 2023-10-06 · 赞同 0**
> 力扣：[2839. 判断通过操作能否让字符串相等 I](https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-i/) · Easy · 灵茶山艾府：[O(n) 通用做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2839.判断通过操作能否让字符串相等I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-strings-can-be-made-equal-with-operations-i/)

题目给出的字符串长度为4，且可交换的下标之差为2，那么就意味着两个字符串中的下标0、2可以互相交换，下标1、3可以互相交换。于是只需将两个字符串中下标0、2的分为一组，1、3的分为另一组，然后对比两个字符串中这两组是否都相同就行了。

最后附上python代码：

```python
class Solution(object):
    def canBeEqual(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        if min(s1[0], s1[2]) != min(s2[0], s2[2]):
            return False
        if max(s1[0], s1[2]) != max(s2[0], s2[2]):
            return False
        if min(s1[1], s1[3]) != min(s2[1], s2[3]):
            return False
        if max(s1[1], s1[3]) != max(s2[1], s2[3]):
            return False
        return True
```
