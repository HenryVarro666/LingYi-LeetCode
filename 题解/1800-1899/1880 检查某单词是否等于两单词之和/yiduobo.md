---
title: "1880. 检查某单词是否等于两单词之和"
aliases: ["yiduobo的每日leetcode 1880.检查某单词是否等于两单词之和"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476349884"
zhihu_id: "476349884"
zhihu_title: "yiduobo的每日leetcode 1880.检查某单词是否等于两单词之和"
question_id: "1880"
question: "检查某单词是否等于两单词之和"
problem_url: "https://leetcode.cn/problems/check-if-word-equals-summation-of-two-words/"
difficulty: "Easy"
created: "2022-03-05T18:56:20+08:00"
updated: "2022-03-05T18:56:20+08:00"
upvotes: 0
comments: 0
---

# 1880. 检查某单词是否等于两单词之和

> **[yiduobo的每日leetcode 1880.检查某单词是否等于两单词之和](https://zhuanlan.zhihu.com/p/476349884) · 知乎 · 2022-03-05 · 赞同 0**
> 力扣：[1880. 检查某单词是否等于两单词之和](https://leetcode.cn/problems/check-if-word-equals-summation-of-two-words/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1880.检查某单词是否等于两单词之和

[力扣](https://leetcode-cn.com/problems/check-if-word-equals-summation-of-two-words/)

直接按照题目中字符与数字的对应关系计算出三个单词对应的数值，然后判断是否满足两数之和等于目标数。

最后附上python代码：

```python
class Solution(object):
    def isSumEqual(self, firstWord, secondWord, targetWord):
        """
        :type firstWord: str
        :type secondWord: str
        :type targetWord: str
        :rtype: bool
        """

        return self.word_sum(firstWord) + self.word_sum(secondWord) == self.word_sum(targetWord)
    
    def word_sum(self, s):
        res = 0
        for char in s:
            res = res * 10 + ord(char) - 97
        
        return res
```
