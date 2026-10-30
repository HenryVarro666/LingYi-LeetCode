---
title: "2496. 数组中字符串的最大值"
aliases: ["yiduobo的每日leetcode 2496.数组中字符串的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633213410"
zhihu_id: "633213410"
zhihu_title: "yiduobo的每日leetcode 2496.数组中字符串的最大值"
question_id: "2496"
question: "数组中字符串的最大值"
problem_url: "https://leetcode.cn/problems/maximum-value-of-a-string-in-an-array/"
difficulty: "Easy"
created: "2023-05-30T03:30:25+08:00"
updated: "2023-05-30T03:30:25+08:00"
upvotes: 0
comments: 0
---

# 2496. 数组中字符串的最大值

> **[yiduobo的每日leetcode 2496.数组中字符串的最大值](https://zhuanlan.zhihu.com/p/633213410) · 知乎 · 2023-05-30 · 赞同 0**
> 力扣：[2496. 数组中字符串的最大值](https://leetcode.cn/problems/maximum-value-of-a-string-in-an-array/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2496.数组中字符串的最大值

[力扣](https://leetcode.cn/problems/maximum-value-of-a-string-in-an-array/)

直接按照题目意思一趟遍历，检测当前遍历的字符串中是否出现了小写字符。如果出现了，那么就使用其长度来更新答案，否则使用其数值来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumValue(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        res = 0
        for s in strs:
            flag = True
            for char in s:
                if 'a' <= char <= 'z':
                    flag = False
                    break
            
            if flag:
                v = int(s)
            else:
                v = len(s)
            
            res = max(res, v)

        return res
```
