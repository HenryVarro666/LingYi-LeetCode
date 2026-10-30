---
title: "273. 整数转换英文表示"
aliases: ["yiduobo的每日leetcode 273.整数转换英文表示"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/编程能力强化训练"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/152239441"
zhihu_id: "152239441"
zhihu_title: "yiduobo的每日leetcode 273.整数转换英文表示"
question_id: "273"
question: "整数转换英文表示"
problem_url: "https://leetcode.cn/problems/integer-to-english-words/"
difficulty: "Hard"
created: "2020-06-30T22:43:53+08:00"
updated: "2020-06-30T22:43:53+08:00"
upvotes: 0
comments: 0
---

# 273. 整数转换英文表示

> **[yiduobo的每日leetcode 273.整数转换英文表示](https://zhuanlan.zhihu.com/p/152239441) · 知乎 · 2020-06-30 · 赞同 0**
> 力扣：[273. 整数转换英文表示](https://leetcode.cn/problems/integer-to-english-words/) · Hard · 灵茶山艾府：[拆分成若干小于 1000 的数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

273.整数转换英文表示<https://leetcode-cn.com/problems/integer-to-english-words/submissions/>

没有什么难度，但是细节很多的题目。

按照英语的表示习惯，数字都是按照千来进行分割的。

对于分割下来的部分，首先将百分离出来，然后对于十位和个位，如果在20以内，那么有特有的单词与之对应，否则就按十位与个位分割即可。

需要注意的是，除了num为0的情况之外，其他时候0都不会表示在结果中。

另外还需要注意单词之间的空格衔接。

最后附上python代码：

```python
class Solution(object):
    def numberToWords(self, num):
        """
        :type num: int
        :rtype: str
        """

        suffix = ['', ' Thousand', ' Million', ' Billion']
        suffix_pos = 0

        single = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 
                  'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        ten = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

        res = ''
        while num:
            tmp = num % 1000
            part_res = ''

            hundred = tmp / 100
            tmp %= 100

            if tmp == 0:
                part_res = ''
            else:
                if tmp < 20:
                    part_res = single[tmp]
                else:
                    part_res = ten[tmp / 10]
                    tmp %= 10
                    if tmp:
                        part_res = part_res + ' ' + single[tmp]
            
            if hundred > 0:
                if part_res:
                    part_res = single[hundred] + ' Hundred ' + part_res
                else:
                    part_res = single[hundred] + ' Hundred'

            if part_res:
                if res:
                    res = part_res + suffix[suffix_pos] + ' ' + res
                else:
                    res = part_res + suffix[suffix_pos]
            
            num /= 1000
            suffix_pos += 1

        if not res:
            return single[0]

        return res
```
