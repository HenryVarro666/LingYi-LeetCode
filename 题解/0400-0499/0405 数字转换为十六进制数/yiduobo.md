---
title: "405. 数字转换为十六进制数"
aliases: ["yiduobo的每日leetcode 405.数字转换为十六进制数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/184993593"
zhihu_id: "184993593"
zhihu_title: "yiduobo的每日leetcode 405.数字转换为十六进制数"
question_id: "405"
question: "数字转换为十六进制数"
problem_url: "https://leetcode.cn/problems/convert-a-number-to-hexadecimal/"
difficulty: "Easy"
created: "2020-08-15T20:05:51+08:00"
updated: "2020-08-15T20:05:51+08:00"
upvotes: 0
comments: 0
---

# 405. 数字转换为十六进制数

> **[yiduobo的每日leetcode 405.数字转换为十六进制数](https://zhuanlan.zhihu.com/p/184993593) · 知乎 · 2020-08-15 · 赞同 0**
> 力扣：[405. 数字转换为十六进制数](https://leetcode.cn/problems/convert-a-number-to-hexadecimal/) · Easy · 灵茶山艾府：[Go 一行](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

405.数字转换为十六进制数<https://leetcode-cn.com/problems/convert-a-number-to-hexadecimal/>

比较基础的题目，不断模16然后将10到15转化为a到f即可。

对于负数来说，则是先计算正数的十六进制表示，然后取反取补。

最后附上python代码：

```python
class Solution(object):
    def toHex(self, num):
        """
        :type num: int
        :rtype: str
        """
        
        if num == -2147483648:
            return '80000000'
        if num == 0:
            return '0'

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num

        num_list = [0] * 8
        pos = -1
        while num:
            num_list[pos] = num % 16
            num /= 16
            pos -= 1

        if neg_flag:
            num_list = [15 - x for x in num_list]
            num_list[-1] += 1
            pos = -1
            while num_list[pos] == 16:
                num_list[pos] -= 16
                num_list[pos - 1] += 1
                pos -= 1

        zero_flag = True
        char_list = []
        for x in num_list:
            if zero_flag and x == 0:
                continue
            zero_flag = False
            if x < 10:
                char_list.append(str(x))
            else:
                char_list.append(chr(x + 87))
        
        return ''.join(char_list)
```
