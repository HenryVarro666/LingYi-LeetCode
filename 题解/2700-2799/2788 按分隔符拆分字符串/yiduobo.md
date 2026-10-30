---
title: "2788. 按分隔符拆分字符串"
aliases: ["yiduobo的每日leetcode 2788.按分隔符拆分字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656715087"
zhihu_id: "656715087"
zhihu_title: "yiduobo的每日leetcode 2788.按分隔符拆分字符串"
question_id: "2788"
question: "按分隔符拆分字符串"
problem_url: "https://leetcode.cn/problems/split-strings-by-separator/"
created: "2023-09-17T05:09:14+08:00"
updated: "2023-09-17T05:09:14+08:00"
upvotes: 0
comments: 0
---

# 2788. 按分隔符拆分字符串

> **[yiduobo的每日leetcode 2788.按分隔符拆分字符串](https://zhuanlan.zhihu.com/p/656715087) · 知乎 · 2023-09-17 · 赞同 0**
> 力扣：[2788. 按分隔符拆分字符串](https://leetcode.cn/problems/split-strings-by-separator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2788.按分隔符拆分字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/split-strings-by-separator/description/)

有原生split函数的语言可以直接通过split分割每个单词，然后将不为空的部分依次加入到答案数组中即可。没有的话则需要遍历每个单词，每次从起始位置p开始，使用一个指针q不断向后移动，直到来到单词末尾或者分隔符，那么p到q - 1的这一段子串就是拆分的一个部分，将其加入到答案中，然后将p移动到q并重复此过程。

最后附上python代码：

```python
class Solution(object):
    def splitWordsBySeparator(self, words, separator):
        """
        :type words: List[str]
        :type separator: str
        :rtype: List[str]
        """

        res = []
        for w in words:
            for part in w.split(separator):
                if part:
                    res.append(part)
        
        return res
```
