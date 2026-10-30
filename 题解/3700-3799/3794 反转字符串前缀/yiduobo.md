---
title: "3794. 反转字符串前缀"
aliases: ["yiduobo的每日leetcode 3794.反转字符串前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1991711359973467168"
zhihu_id: "1991711359973467168"
zhihu_title: "yiduobo的每日leetcode 3794.反转字符串前缀"
question_id: "3794"
question: "反转字符串前缀"
problem_url: "https://leetcode.cn/problems/reverse-string-prefix/"
difficulty: "Easy"
created: "2026-01-06T03:26:25+08:00"
updated: "2026-01-06T03:26:26+08:00"
upvotes: 1
comments: 0
---

# 3794. 反转字符串前缀

> **[yiduobo的每日leetcode 3794.反转字符串前缀](https://zhuanlan.zhihu.com/p/1991711359973467168) · 知乎 · 2026-01-06 · 赞同 1**
> 力扣：[3794. 反转字符串前缀](https://leetcode.cn/problems/reverse-string-prefix/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3794.反转字符串前缀

[3794. 反转字符串前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/reverse-string-prefix/description/)

题目给出一个字符串s以及一个整数k，要求反转s的前k个字符，并返回结果字符串。

比较基础的题目，直接按照题目要求执行就可以了。具体实现上，使用python可以通过s[:k]和s[k:]的写法分离出s中的前k个字符以及剩下的字符。更进一步的，可以通过s[:k][::-1]得到前k个字符反转后的结果，然后与s[k:]拼接起来即为最终答案。

```python
class Solution(object):
    def reversePrefix(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        
        return s[:k][::-1] + s[k:]
```
