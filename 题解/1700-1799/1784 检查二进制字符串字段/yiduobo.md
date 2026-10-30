---
title: "1784. 检查二进制字符串字段"
aliases: ["yiduobo的每日leetcode 1784.检查二进制字符串字段"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462852735"
zhihu_id: "462852735"
zhihu_title: "yiduobo的每日leetcode 1784.检查二进制字符串字段"
question_id: "1784"
question: "检查二进制字符串字段"
problem_url: "https://leetcode.cn/problems/check-if-binary-string-has-at-most-one-segment-of-ones/"
difficulty: "Easy"
created: "2022-01-28T23:33:32+08:00"
updated: "2022-01-28T23:33:32+08:00"
upvotes: 0
comments: 0
---

# 1784. 检查二进制字符串字段

> **[yiduobo的每日leetcode 1784.检查二进制字符串字段](https://zhuanlan.zhihu.com/p/462852735) · 知乎 · 2022-01-28 · 赞同 0**
> 力扣：[1784. 检查二进制字符串字段](https://leetcode.cn/problems/check-if-binary-string-has-at-most-one-segment-of-ones/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1784.检查二进制字符串字段

[力扣](https://leetcode-cn.com/problems/check-if-binary-string-has-at-most-one-segment-of-ones/)

题目需要找出字符串中是否有非连续的1，由于字符串默认是从1开始的，那么只需要找到0第一次出现的位置，然后判断这个位置后面是否有1出现即可。

最后附上python代码：

```python
class Solution(object):
    def checkOnesSegment(self, s):
        """
        :type s: str
        :rtype: bool
        """

        n = len(s)
        p = 0
        while p < n and s[p] == '1':
            p += 1
        
        while p < n and s[p] == '0':
            p += 1
        
        return p == n
```
