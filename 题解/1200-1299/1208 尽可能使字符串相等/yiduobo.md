---
title: "1208. 尽可能使字符串相等"
aliases: ["yiduobo的每日leetcode 1208.尽可能使字符串相等"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382207298"
zhihu_id: "382207298"
zhihu_title: "yiduobo的每日leetcode 1208.尽可能使字符串相等"
question_id: "1208"
question: "尽可能使字符串相等"
problem_url: "https://leetcode.cn/problems/get-equal-substrings-within-budget/"
created: "2021-06-19T20:13:54+08:00"
updated: "2021-06-19T20:13:54+08:00"
upvotes: 0
comments: 0
---

# 1208. 尽可能使字符串相等

> **[yiduobo的每日leetcode 1208.尽可能使字符串相等](https://zhuanlan.zhihu.com/p/382207298) · 知乎 · 2021-06-19 · 赞同 0**
> 力扣：[1208. 尽可能使字符串相等](https://leetcode.cn/problems/get-equal-substrings-within-budget/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1208.尽可能使字符串相等

[力扣](https://leetcode-cn.com/problems/get-equal-substrings-within-budget/)

题目已经给出了字符串变换需要的代价，那么我们可以先进行一趟扫描，计算出每个位置上变换所需的代价。此时我们就得到了一个代价数组，而目标则是从中间选择出尽可能长的连续的一段，而这一段数组中各个数字之和必须小于等于最大预算。

这是一个典型的滚动数组问题，我们首先设0为答案的起点l，那么我们需要从0开始向后扫描，寻找最大的r。接下来每一轮我们都尝试将r向后移动一个位置，并根据当前开销调整l的位置即可。

最后附上python代码：

```python
class Solution(object):
    def equalSubstring(self, s, t, maxCost):
        """
        :type s: str
        :type t: str
        :type maxCost: int
        :rtype: int
        """

        n = len(s)
        cost_list = [abs(ord(s[index]) - ord(t[index])) for index in range(n)]
        l = 0
        r = 0
        now = 0
        while r < n and cost_list[r] + now <= maxCost:
            now += cost_list[r]
            r += 1
        
        res = r - l
        while r < n:
            now += cost_list[r]
            r += 1
            while l < r and now > maxCost:
                now -= cost_list[l]
                l += 1
            res = max(res, r - l)
        
        return res
```
