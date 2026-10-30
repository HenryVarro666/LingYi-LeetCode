---
title: "557. 反转字符串中的单词III"
aliases: ["yiduobo的每日leetcode 557.反转字符串中的单词III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/265531034"
zhihu_id: "265531034"
zhihu_title: "yiduobo的每日leetcode 557.反转字符串中的单词III"
question_id: "557"
question: "反转字符串中的单词III"
problem_url: "https://leetcode.cn/problems/reverse-words-in-a-string-iii/"
created: "2020-10-13T22:43:40+08:00"
updated: "2020-10-13T22:43:40+08:00"
upvotes: 0
comments: 0
---

# 557. 反转字符串中的单词III

> **[yiduobo的每日leetcode 557.反转字符串中的单词III](https://zhuanlan.zhihu.com/p/265531034) · 知乎 · 2020-10-13 · 赞同 0**
> 力扣：[557. 反转字符串中的单词III](https://leetcode.cn/problems/reverse-words-in-a-string-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

557.反转字符串中的单词III <https://leetcode-cn.com/problems/reverse-words-in-a-string-iii/>

比较基础的题目，按空格分离单词，逐个反转后再合并起来就行了。

最后附上python代码：

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = s.split(' ')
        return ' '.join([x[::-1] for x in res])
```
