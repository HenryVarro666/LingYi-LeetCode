---
title: "2068. 检查两个字符串是否几乎相等"
aliases: ["yiduobo的每日leetcode 2068.检查两个字符串是否几乎相等"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/515345530"
zhihu_id: "515345530"
zhihu_title: "yiduobo的每日leetcode 2068.检查两个字符串是否几乎相等"
question_id: "2068"
question: "检查两个字符串是否几乎相等"
problem_url: "https://leetcode.cn/problems/check-whether-two-strings-are-almost-equivalent/"
difficulty: "Easy"
created: "2022-05-16T19:52:31+08:00"
updated: "2022-05-16T19:52:31+08:00"
upvotes: 0
comments: 0
---

# 2068. 检查两个字符串是否几乎相等

> **[yiduobo的每日leetcode 2068.检查两个字符串是否几乎相等](https://zhuanlan.zhihu.com/p/515345530) · 知乎 · 2022-05-16 · 赞同 0**
> 力扣：[2068. 检查两个字符串是否几乎相等](https://leetcode.cn/problems/check-whether-two-strings-are-almost-equivalent/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2068.检查两个字符串是否几乎相等

[力扣](https://leetcode.cn/problems/check-whether-two-strings-are-almost-equivalent/)

比较基础的题目，使用哈希表记录每个字符在word1中出现次数与word2中出现次数之差，接下来遍历每种字符出现次数之差，如果有差值大于3次的字符，那么答案就是false，否则答案就是true。

最后附上python代码：

```python
class Solution(object):
    def checkAlmostEquivalent(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: bool
        """

        char_diff = {}
        for char in word1:
            char_diff[char] = char_diff.get(char, 0) + 1
        
        for char in word2:
            char_diff[char] = char_diff.get(char, 0) - 1

        for diff in char_diff.values():
            if abs(diff) > 3:
                return False

        return True
```
