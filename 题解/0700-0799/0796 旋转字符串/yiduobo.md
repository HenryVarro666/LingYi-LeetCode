---
title: "796. 旋转字符串"
aliases: ["yiduobo的每日leetcode 796.旋转字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string-matching", "leetcode/bao-li", "题单/字符串", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342125536"
zhihu_id: "342125536"
zhihu_title: "yiduobo的每日leetcode 796.旋转字符串"
question_id: "796"
question: "旋转字符串"
problem_url: "https://leetcode.cn/problems/rotate-string/"
difficulty: "Easy"
created: "2021-01-05T21:24:36+08:00"
updated: "2021-01-05T21:24:36+08:00"
upvotes: 0
comments: 0
---

# 796. 旋转字符串

> **[yiduobo的每日leetcode 796.旋转字符串](https://zhuanlan.zhihu.com/p/342125536) · 知乎 · 2021-01-05 · 赞同 0**
> 力扣：[796. 旋转字符串](https://leetcode.cn/problems/rotate-string/) · Easy · 灵茶山艾府：[两种方法：暴力 / KMP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

796.旋转字符串

[力扣](https://leetcode-cn.com/problems/rotate-string/)

首先，两串都为空，那么答案为true，否则其他情况下两串长度若不相同，那么答案为false。

注意到题目中字符串的长度较短，因此直接使用暴力法也是可以的，不过更通用的做法是将A串复制一遍然后接在A后面。设A的长度为n，那么这样一来，

A[0]到A[n - 1]就是原始的A

A[1]到A[n]就是A移动一位

A[2]到A[n + 1]就是A移动两位

...
A[n - 1]到A[n + n - 2]就是A移动n - 1位

可以发现，复制后的串包含了A所有的可能移动，那么此时只需要判断B是否为A + A的子串即可。这里判断的方法多种多样，我在这里采用的是kmp。

最后附上python代码：

```python
class Solution(object):
    def rotateString(self, A, B):
        """
        :type A: str
        :type B: str
        :rtype: bool
        """

        if not A and not B:
            return True

        if len(A) != len(B):
            return False

        f = [0]
        pos = 0
        for index in range(1, len(B)):
            while pos > 0 and B[pos] != B[index]:
                pos = f[pos - 1]
            if B[pos] == B[index]:
                pos += 1
            f.append(pos)
        
        pos = 0
        for char in A + A:
            while pos > 0 and B[pos] != char:
                pos = f[pos - 1]
            if B[pos] == char:
                pos += 1
                if pos == len(B):
                    return True

        return False
```
