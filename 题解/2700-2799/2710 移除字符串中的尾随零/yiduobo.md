---
title: "2710. 移除字符串中的尾随零"
aliases: ["yiduobo的每日leetcode 2710.移除字符串中的尾随零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/api"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651071303"
zhihu_id: "651071303"
zhihu_title: "yiduobo的每日leetcode 2710.移除字符串中的尾随零"
question_id: "2710"
question: "移除字符串中的尾随零"
problem_url: "https://leetcode.cn/problems/remove-trailing-zeros-from-a-string/"
difficulty: "Easy"
created: "2023-08-19T18:04:04+08:00"
updated: "2023-08-19T18:04:04+08:00"
upvotes: 0
comments: 0
---

# 2710. 移除字符串中的尾随零

> **[yiduobo的每日leetcode 2710.移除字符串中的尾随零](https://zhuanlan.zhihu.com/p/651071303) · 知乎 · 2023-08-19 · 赞同 0**
> 力扣：[2710. 移除字符串中的尾随零](https://leetcode.cn/problems/remove-trailing-zeros-from-a-string/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2710.移除字符串中的尾随零

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/remove-trailing-zeros-from-a-string/)

由于题目保证num是正数，那么数字中必然存在一个非零的数位。只需从最后一位开始，向前找到位置最后的那个非零位，然后将这个非零位后面的部分截取掉就行了。

最后附上python代码：

```python
class Solution(object):
    def removeTrailingZeros(self, num):
        """
        :type num: str
        :rtype: str
        """

        p = len(num) - 1
        while num[p] == '0':
            p -= 1
        
        return num[:p + 1]
```
