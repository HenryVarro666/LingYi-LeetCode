---
title: "387. 字符串中的第一个唯一字符"
aliases: ["yiduobo的每日leetcode 387.字符串中的第一个唯一字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/170582853"
zhihu_id: "170582853"
zhihu_title: "yiduobo的每日leetcode 387.字符串中的第一个唯一字符"
question_id: "387"
question: "字符串中的第一个唯一字符"
problem_url: "https://leetcode.cn/problems/first-unique-character-in-a-string/"
created: "2020-08-06T20:54:15+08:00"
updated: "2020-08-06T20:54:15+08:00"
upvotes: 0
comments: 0
---

# 387. 字符串中的第一个唯一字符

> **[yiduobo的每日leetcode 387.字符串中的第一个唯一字符](https://zhuanlan.zhihu.com/p/170582853) · 知乎 · 2020-08-06 · 赞同 0**
> 力扣：[387. 字符串中的第一个唯一字符](https://leetcode.cn/problems/first-unique-character-in-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

387.字符串中的第一个唯一字符<https://leetcode-cn.com/problems/first-unique-character-in-a-string/>

比较基础的题目，一边扫描统计即可。

最后附上python代码：

```python
class Solution(object):
    def firstUniqChar(self, s):
        """
        :type s: str
        :rtype: int
        """

        if not s:
            return -1

        char_dict = {}
        for index, char in enumerate(s):
            if char not in char_dict:
                char_dict[char] = index
            else:
                char_dict[char] = len(s)

        res = min(char_dict.values())
        if len(s) == res:
            return -1
        return res
```
