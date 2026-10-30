---
title: "1796. 字符串中第二大的数字"
aliases: ["yiduobo的每日leetcode 1796.字符串中第二大的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463543729"
zhihu_id: "463543729"
zhihu_title: "yiduobo的每日leetcode 1796.字符串中第二大的数字"
question_id: "1796"
question: "字符串中第二大的数字"
problem_url: "https://leetcode.cn/problems/second-largest-digit-in-a-string/"
created: "2022-02-01T23:05:11+08:00"
updated: "2022-02-01T23:05:11+08:00"
upvotes: 0
comments: 0
---

# 1796. 字符串中第二大的数字

> **[yiduobo的每日leetcode 1796.字符串中第二大的数字](https://zhuanlan.zhihu.com/p/463543729) · 知乎 · 2022-02-01 · 赞同 0**
> 力扣：[1796. 字符串中第二大的数字](https://leetcode.cn/problems/second-largest-digit-in-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1796.字符串中第二大的数字

[力扣](https://leetcode-cn.com/problems/second-largest-digit-in-a-string/)

比较基础的题目，一趟扫描，只针对数字选出其中第二大的即可。

最后附上python代码：

```python
class Solution(object):
    def secondHighest(self, s):
        """
        :type s: str
        :rtype: int
        """

        first = second = None
        for char in s:
            if char >= '0' and char <= '9':
                if first is None or first < char:
                    first, second = char, first
                elif first != char and (second is None or second < char):
                    second = char
        
        if second is None:
            return -1
        
        return int(second)
```
