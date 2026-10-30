---
title: "2743. 计算没有重复字符的子字符串数量"
aliases: ["yiduobo的每日leetcode 2743.计算没有重复字符的子字符串数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653627252"
zhihu_id: "653627252"
zhihu_title: "yiduobo的每日leetcode 2743.计算没有重复字符的子字符串数量"
question_id: "2743"
question: "计算没有重复字符的子字符串数量"
problem_url: "https://leetcode.cn/problems/count-substrings-without-repeating-character/"
created: "2023-09-01T01:15:23+08:00"
updated: "2023-09-01T01:15:23+08:00"
upvotes: 0
comments: 0
---

# 2743. 计算没有重复字符的子字符串数量

> **[yiduobo的每日leetcode 2743.计算没有重复字符的子字符串数量](https://zhuanlan.zhihu.com/p/653627252) · 知乎 · 2023-09-01 · 赞同 0**
> 力扣：[2743. 计算没有重复字符的子字符串数量](https://leetcode.cn/problems/count-substrings-without-repeating-character/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2743.计算没有重复字符的子字符串数量

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-substrings-without-repeating-character/)

经典的边长滑动窗口问题。对于每个位置left，找出以left为左边界，且不包含任何重复字符的子串的最大右边界right，那么以left为左边界的没有重复字符的子字符串数量就有right - left个。接下来对于以left + 1为左边界的子字符串，可以明确的是left + 1到right - 1之间是没有任何重复字符的，因此left + 1对应的right'必然大于等于right，也就是说可以在上一轮right的基础上向右扩展。

最后附上python代码：

```python
class Solution(object):
    def numberOfSpecialSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        left = 0
        right = left + 1
        res = 0
        char_set = set([s[0]])
        while left < n:
            while right < n and s[right] not in char_set:
                char_set.add(s[right])
                right += 1
            
            res += right - left

            char_set.remove(s[left])
            left += 1
        
        return res
```
