---
title: "151. 翻转字符串里的单词"
aliases: ["yiduobo的每日leetcode 151.翻转字符串里的单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143251784"
zhihu_id: "143251784"
zhihu_title: "yiduobo的每日leetcode 151.翻转字符串里的单词"
question_id: "151"
question: "翻转字符串里的单词"
problem_url: "https://leetcode.cn/problems/reverse-words-in-a-string/"
created: "2020-05-24T19:39:35+08:00"
updated: "2020-05-24T19:39:35+08:00"
upvotes: 0
comments: 0
---

# 151. 翻转字符串里的单词

> **[yiduobo的每日leetcode 151.翻转字符串里的单词](https://zhuanlan.zhihu.com/p/143251784) · 知乎 · 2020-05-24 · 赞同 0**
> 力扣：[151. 翻转字符串里的单词](https://leetcode.cn/problems/reverse-words-in-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

151.翻转字符串里的单词<https://leetcode-cn.com/problems/reverse-words-in-a-string/>

这题用python来写非常简单，split加上reverse最后join一下就搞定了。

具体代码如下：

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """

        word_list = s.split()
        word_list.reverse()
        return ' '.join(word_list)
```
