---
title: "2828. 判别首字母缩略词"
aliases: ["yiduobo的每日leetcode 2828.判别首字母缩略词"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659174492"
zhihu_id: "659174492"
zhihu_title: "yiduobo的每日leetcode 2828.判别首字母缩略词"
question_id: "2828"
question: "判别首字母缩略词"
problem_url: "https://leetcode.cn/problems/check-if-a-string-is-an-acronym-of-words/"
difficulty: "Easy"
created: "2023-09-30T22:10:46+08:00"
updated: "2023-09-30T22:10:46+08:00"
upvotes: 0
comments: 0
---

# 2828. 判别首字母缩略词

> **[yiduobo的每日leetcode 2828.判别首字母缩略词](https://zhuanlan.zhihu.com/p/659174492) · 知乎 · 2023-09-30 · 赞同 0**
> 力扣：[2828. 判别首字母缩略词](https://leetcode.cn/problems/check-if-a-string-is-an-acronym-of-words/) · Easy · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2828.判别首字母缩略词

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-a-string-is-an-acronym-of-words/)

遍历words中的所有单词，将首字母拼接起来之后判断是否与s即可。

最后附上python代码：

```python
class Solution(object):
    def isAcronym(self, words, s):
        """
        :type words: List[str]
        :type s: str
        :rtype: bool
        """

        return ''.join([w[0] for w in words]) == s
```
