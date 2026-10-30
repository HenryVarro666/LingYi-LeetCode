---
title: "1935. 可以输入的最大单词数"
aliases: ["yiduobo的每日leetcode 1935.可以输入的最大单词数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/488094645"
zhihu_id: "488094645"
zhihu_title: "yiduobo的每日leetcode 1935.可以输入的最大单词数"
question_id: "1935"
question: "可以输入的最大单词数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-words-you-can-type/"
difficulty: "Easy"
created: "2022-03-26T18:23:27+08:00"
updated: "2022-03-26T18:23:27+08:00"
upvotes: 0
comments: 0
---

# 1935. 可以输入的最大单词数

> **[yiduobo的每日leetcode 1935.可以输入的最大单词数](https://zhuanlan.zhihu.com/p/488094645) · 知乎 · 2022-03-26 · 赞同 0**
> 力扣：[1935. 可以输入的最大单词数](https://leetcode.cn/problems/maximum-number-of-words-you-can-type/) · Easy · 灵茶山艾府：[两种方法：按空格分割 / 位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1935.可以输入的最大单词数

[力扣](https://leetcode-cn.com/problems/maximum-number-of-words-you-can-type/)

使用一个集合统计损坏的按键，然后对于每个单词，遍历其中的每个字母。

对于当前的单词，若某个字母出现在损坏的集合中，那么说明该单词无法被输入，直接考虑下一个单词；若没有字母出现在损坏的集合中，那么就将答案加1。

最后附上python代码：

```python
class Solution(object):
    def canBeTypedWords(self, text, brokenLetters):
        """
        :type text: str
        :type brokenLetters: str
        :rtype: int
        """

        borken_set = set()
        for char in brokenLetters:
            borken_set.add(char)
        
        res = 0
        for word in text.split(' '):
            flag = True
            for char in word:
                if char in borken_set:
                    flag = False
                    break
            
            if flag:
                res += 1
        
        return res
```
