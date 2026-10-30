---
title: "434. 字符串中的单词数"
aliases: ["yiduobo的每日leetcode 434.字符串中的单词数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/198200809"
zhihu_id: "198200809"
zhihu_title: "yiduobo的每日leetcode 434.字符串中的单词数"
question_id: "434"
question: "字符串中的单词数"
problem_url: "https://leetcode.cn/problems/number-of-segments-in-a-string/"
created: "2020-08-25T23:35:48+08:00"
updated: "2020-08-25T23:35:48+08:00"
upvotes: 0
comments: 0
---

# 434. 字符串中的单词数

> **[yiduobo的每日leetcode 434.字符串中的单词数](https://zhuanlan.zhihu.com/p/198200809) · 知乎 · 2020-08-25 · 赞同 0**
> 力扣：[434. 字符串中的单词数](https://leetcode.cn/problems/number-of-segments-in-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

434.字符串中的单词数<https://leetcode-cn.com/problems/number-of-segments-in-a-string/>

比较基础的题目，直接split即可。各种高级语言现在应该都支持这个操作了。

最后附上python代码：

```python
class Solution(object):
    def countSegments(self, s):
        """
        :type s: str
        :rtype: int
        """

        return len(s.split())
```
