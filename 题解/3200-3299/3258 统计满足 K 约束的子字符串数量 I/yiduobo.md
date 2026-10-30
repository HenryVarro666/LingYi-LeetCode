---
title: "3258. 统计满足K约束的子字符串数量I"
aliases: ["yiduobo的每日leetcode 3258.统计满足K约束的子字符串数量I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/722192899"
zhihu_id: "722192899"
zhihu_title: "yiduobo的每日leetcode 3258.统计满足K约束的子字符串数量I"
question_id: "3258"
question: "统计满足 K 约束的子字符串数量 I"
problem_url: "https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-i/"
difficulty: "Easy"
created: "2024-09-26T02:14:28+08:00"
updated: "2024-09-26T02:14:28+08:00"
upvotes: 1
comments: 0
---

# 3258. 统计满足K约束的子字符串数量I

> **[yiduobo的每日leetcode 3258.统计满足K约束的子字符串数量I](https://zhuanlan.zhihu.com/p/722192899) · 知乎 · 2024-09-26 · 赞同 1**
> 力扣：[3258. 统计满足 K 约束的子字符串数量 I](https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-i/) · Easy · 灵茶山艾府：[「越短越合法」型滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3258.统计满足K约束的字符串数量I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-i/)

题目给出一个二进制字符串s以及一个整数k，若某个二进制字符串中0的数量不超过k，或者1的数量不超过k，那么这个字符串就是一个k约束字符串。现在要求计算s中所有k约束字符串的数量。

使用变长滑动窗口从左向右移动，随着右边界的向右移动，窗口内0和1的数量可能同时超过k，此时就需要不断向后移动左边界，直到窗口内0的数量不超过k个，或者1的数量不超过k个。不妨设当前窗口的左右边界分别为p和index，那么所有起点在p、p + 1、p + 2、...、index，终点在index的子串都是满足k约束的，一共有index - p + 1个子串，将其累加到答案然后继续向后移动窗口右边界即可。

最后附上python代码：

```python
class Solution(object):
    def countKConstraintSubstrings(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        zero = 0
        one = 0
        res = 0

        p = 0
        for index, char in enumerate(s):            
            if char == '1':
                one += 1
            else:
                zero += 1
        
            while one > k and zero > k:
                if s[p] == '0':
                    zero -= 1
                else:
                    one -= 1
                p += 1
            
            res += (index - p + 1)
        
        return res
```
