---
title: "804. 唯一的摩尔斯密码词"
aliases: ["yiduobo的每日leetcode 804.唯一的摩尔斯密码词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343112487"
zhihu_id: "343112487"
zhihu_title: "yiduobo的每日leetcode 804.唯一的摩尔斯密码词"
question_id: "804"
question: "唯一的摩尔斯密码词"
problem_url: "https://leetcode.cn/problems/unique-morse-code-words/"
created: "2021-01-09T20:54:18+08:00"
updated: "2021-01-09T20:54:18+08:00"
upvotes: 0
comments: 0
---

# 804. 唯一的摩尔斯密码词

> **[yiduobo的每日leetcode 804.唯一的摩尔斯密码词](https://zhuanlan.zhihu.com/p/343112487) · 知乎 · 2021-01-09 · 赞同 0**
> 力扣：[804. 唯一的摩尔斯密码词](https://leetcode.cn/problems/unique-morse-code-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

804.唯一的摩尔斯密码词

[力扣](https://leetcode-cn.com/problems/unique-morse-code-words/)

由于单词的数量不超过100，长度也在12之内，因此可以直接将所有单词转化为摩尔斯密码，然后使用set来去重。

最后附上python代码：

```python
class Solution(object):
    def uniqueMorseRepresentations(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        morse = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--.."]
        word_set = set()
        for word in words:
            word_set.add(''.join([morse[ord(char) - 97] for char in word]))
        
        return len(word_set)
```
