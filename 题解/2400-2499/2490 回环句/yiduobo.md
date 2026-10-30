---
title: "2490. 回环句"
aliases: ["yiduobo的每日leetcode 2490.回环句"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590110514"
zhihu_id: "590110514"
zhihu_title: "yiduobo的每日leetcode 2490.回环句"
question_id: "2490"
question: "回环句"
problem_url: "https://leetcode.cn/problems/circular-sentence/"
difficulty: "Easy"
created: "2022-12-08T02:04:53+08:00"
updated: "2022-12-08T02:04:53+08:00"
upvotes: 0
comments: 0
---

# 2490. 回环句

> **[yiduobo的每日leetcode 2490.回环句](https://zhuanlan.zhihu.com/p/590110514) · 知乎 · 2022-12-08 · 赞同 0**
> 力扣：[2490. 回环句](https://leetcode.cn/problems/circular-sentence/) · Easy · 灵茶山艾府：[判断空格前后字符是否相同（附 Python 一行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2490.回环句

[力扣](https://leetcode.cn/problems/circular-sentence/)

首先判断句子的首尾是否相同，接下来按空格将句子分离成单词，判断相邻单词间前一个单词的最后一个字符是否与后一个单词的第一个字符相同即可。

最后附上python代码：

```python
class Solution(object):
    def isCircularSentence(self, sentence):
        """
        :type sentence: str
        :rtype: bool
        """

        if sentence[0] != sentence[-1]:
            return False
        
        words = sentence.split(' ')
        for index in range(1, len(words)):
            if words[index][0] != words[index - 1][-1]:
                return False
        
        return True
```
