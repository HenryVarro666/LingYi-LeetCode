---
title: "3280. 将日期转换为二进制表示"
aliases: ["yiduobo的每日leetcode 3280.将日期转换为二进制表示"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/821891061"
zhihu_id: "821891061"
zhihu_title: "yiduobo的每日leetcode 3280.将日期转换为二进制表示"
question_id: "3280"
question: "将日期转换为二进制表示"
problem_url: "https://leetcode.cn/problems/convert-date-to-binary/"
difficulty: "Easy"
created: "2024-10-04T23:24:10+08:00"
updated: "2024-10-04T23:24:10+08:00"
upvotes: 2
comments: 0
---

# 3280. 将日期转换为二进制表示

> **[yiduobo的每日leetcode 3280.将日期转换为二进制表示](https://zhuanlan.zhihu.com/p/821891061) · 知乎 · 2024-10-04 · 赞同 2**
> 力扣：[3280. 将日期转换为二进制表示](https://leetcode.cn/problems/convert-date-to-binary/) · Easy · 灵茶山艾府：[库函数简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3280.将日期转换为二进制表示

[. - 力扣（LeetCode）](https://leetcode.cn/problems/convert-date-to-binary/description/)

题目给出一个字符串date，形式为yyyy-mm-dd，表示一个日期。现在要求将date中的每个字段都转换为二进制表示。

按照题目要求，将年、月、日分离出来，逐项转换成二进制表示，然后拼接在一起就行了。

最后附上python代码：

```python
class Solution(object):
    def convertDateToBinary(self, date):
        """
        :type date: str
        :rtype: str
        """

        res = []
        for part in date.split('-'):
            v = int(part)
            digits = []
            while v:
                digits.append(str(v % 2))
                v //= 2
            digits.reverse()
            res.append(''.join(digits))
        
        return '-'.join(res)
```
