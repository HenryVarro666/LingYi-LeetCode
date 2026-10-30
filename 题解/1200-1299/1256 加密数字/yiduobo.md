---
title: "1256. 加密数字"
aliases: ["yiduobo的每日leetcode 1256.加密数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614874951"
zhihu_id: "614874951"
zhihu_title: "yiduobo的每日leetcode 1256.加密数字"
question_id: "1256"
question: "加密数字"
problem_url: "https://leetcode.cn/problems/encode-number/"
created: "2023-03-17T19:32:08+08:00"
updated: "2023-03-17T19:32:08+08:00"
upvotes: 0
comments: 0
---

# 1256. 加密数字

> **[yiduobo的每日leetcode 1256.加密数字](https://zhuanlan.zhihu.com/p/614874951) · 知乎 · 2023-03-17 · 赞同 0**
> 力扣：[1256. 加密数字](https://leetcode.cn/problems/encode-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1256.加密数字

[力扣](https://leetcode.cn/problems/encode-number/)

找规律的题目，具体的规律是num + 1的二进制表示然后去掉最高位的1。

最后附上python代码：

```python
class Solution(object):
    def encode(self, num):
        """
        :type num: int
        :rtype: str
        """

        num += 1
        digit_list = []
        while num:
            digit_list.append(num % 2)
            num /= 2
        
        digit_list.pop()
        digit_list.reverse()
        
        return ''.join([str(x) for x in digit_list])
```
