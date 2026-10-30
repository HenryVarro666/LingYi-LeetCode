---
title: "2042. 检查句子中的数字是否递增"
aliases: ["yiduobo的每日leetcode 2042.检查句子中的数字是否递增"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/510385884"
zhihu_id: "510385884"
zhihu_title: "yiduobo的每日leetcode 2042.检查句子中的数字是否递增"
question_id: "2042"
question: "检查句子中的数字是否递增"
problem_url: "https://leetcode.cn/problems/check-if-numbers-are-ascending-in-a-sentence/"
difficulty: "Easy"
created: "2022-05-06T21:10:51+08:00"
updated: "2022-05-06T21:10:51+08:00"
upvotes: 1
comments: 0
---

# 2042. 检查句子中的数字是否递增

> **[yiduobo的每日leetcode 2042.检查句子中的数字是否递增](https://zhuanlan.zhihu.com/p/510385884) · 知乎 · 2022-05-06 · 赞同 1**
> 力扣：[2042. 检查句子中的数字是否递增](https://leetcode.cn/problems/check-if-numbers-are-ascending-in-a-sentence/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2042.检查句子中的数字是否递增

[力扣](https://leetcode-cn.com/problems/check-if-numbers-are-ascending-in-a-sentence/)

题目明确规定了每个token直接由单个空格分隔，那么直接按单个空格split整个字符串，然后逐个遍历每个token。由于单个token要么全是字符，要么是数字，那么检测token的首字符就可以判断当前的token是不是数字。如果是，将其转化后判断其是否大于等于上一个数字即可。

最后附上python代码：

```python
class Solution(object):
    def areNumbersAscending(self, s):
        """
        :type s: str
        :rtype: bool
        """

        last = None
        for word in s.split(' '):
            if word[0] < '0' or word[0] > '9':
                continue
            
            now = int(word)
            
            if last is not None and last >= now:
                return False
            last = now
        
        return True
```
