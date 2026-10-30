---
title: "1271. 十六进制魔术数字"
aliases: ["yiduobo的每日leetcode 1271.十六进制魔术数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615302953"
zhihu_id: "615302953"
zhihu_title: "yiduobo的每日leetcode 1271.十六进制魔术数字"
question_id: "1271"
question: "十六进制魔术数字"
problem_url: "https://leetcode.cn/problems/hexspeak/"
created: "2023-03-19T22:31:36+08:00"
updated: "2023-03-19T22:31:36+08:00"
upvotes: 0
comments: 0
---

# 1271. 十六进制魔术数字

> **[yiduobo的每日leetcode 1271.十六进制魔术数字](https://zhuanlan.zhihu.com/p/615302953) · 知乎 · 2023-03-19 · 赞同 0**
> 力扣：[1271. 十六进制魔术数字](https://leetcode.cn/problems/hexspeak/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1271.十六进制魔术数字

[力扣](https://leetcode.cn/problems/hexspeak/)

直接按照不断模16除以16的方式来进行num的进制转换，若过程中出现了2到9，那么直接返回false，否则按照题目要求将0、1以及10到15转化为字符。

最后附上python代码：

```python
class Solution(object):
    def toHexspeak(self, num):
        """
        :type num: str
        :rtype: str
        """

        res = []
        num = int(num)
        while num:
            now = num % 16
            num /= 16
            if 2 <= now <= 9:
                return 'ERROR'
            
            if now == 0:
                res.append('O')
            elif now == 1:
                res.append('I')
            else:
                res.append(chr(now + 55))
        
        res.reverse()
        return ''.join(res)
```
