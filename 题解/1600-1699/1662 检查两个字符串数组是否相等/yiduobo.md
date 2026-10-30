---
title: "1662. 检查两个字符串数组是否相等"
aliases: ["yiduobo的每日leetcode 1662.检查两个字符串数组是否相等"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/442055405"
zhihu_id: "442055405"
zhihu_title: "yiduobo的每日leetcode 1662.检查两个字符串数组是否相等"
question_id: "1662"
question: "检查两个字符串数组是否相等"
problem_url: "https://leetcode.cn/problems/check-if-two-string-arrays-are-equivalent/"
created: "2021-12-07T00:48:31+08:00"
updated: "2021-12-07T00:48:31+08:00"
upvotes: 0
comments: 0
---

# 1662. 检查两个字符串数组是否相等

> **[yiduobo的每日leetcode 1662.检查两个字符串数组是否相等](https://zhuanlan.zhihu.com/p/442055405) · 知乎 · 2021-12-07 · 赞同 0**
> 力扣：[1662. 检查两个字符串数组是否相等](https://leetcode.cn/problems/check-if-two-string-arrays-are-equivalent/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1662.检查两个字符串数组是否相等

[力扣](https://leetcode-cn.com/problems/check-if-two-string-arrays-are-equivalent/)

比较基础的题目，最容易想的做法是直接将所有部分拼起来然后检测是否相等，我在这里采用的是使用两组指针分别指向两个字符串数组当前处理到的字符，然后同时向后推进并进行比较，若某一方率先到达当前字符串数组的末尾，或者期间指向的字符不一样，那么就返回false，否则返回true。

最后附上python代码：

```python
class Solution(object):
    def arrayStringsAreEqual(self, word1, word2):
        """
        :type word1: List[str]
        :type word2: List[str]
        :rtype: bool
        """

        p1 = p2 = index1 = index2 = 0
        while p1 < len(word1) and p2 < len(word2):
            if p1 == len(word1) or p2 == len(word2):
                return False
            if word1[p1][index1] != word2[p2][index2]:
                return False
            
            index1 += 1
            if index1 == len(word1[p1]):
                p1 += 1
                index1 = 0
            
            index2 += 1
            if index2 == len(word2[p2]):
                p2 += 1
                index2 = 0

        return p1 == len(word1) and p2 == len(word2)
```
