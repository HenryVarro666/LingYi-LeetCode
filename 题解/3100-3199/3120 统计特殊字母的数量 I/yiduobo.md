---
title: "3120. 统计特殊字母的数量I"
aliases: ["yiduobo的每日leetcode 3120.统计特殊字母的数量I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701439105"
zhihu_id: "701439105"
zhihu_title: "yiduobo的每日leetcode 3120.统计特殊字母的数量I"
question_id: "3120"
question: "统计特殊字母的数量 I"
problem_url: "https://leetcode.cn/problems/count-the-number-of-special-characters-i/"
difficulty: "Easy"
created: "2024-06-03T20:37:09+08:00"
updated: "2024-06-03T20:37:09+08:00"
upvotes: 0
comments: 0
---

# 3120. 统计特殊字母的数量I

> **[yiduobo的每日leetcode 3120.统计特殊字母的数量I](https://zhuanlan.zhihu.com/p/701439105) · 知乎 · 2024-06-03 · 赞同 0**
> 力扣：[3120. 统计特殊字母的数量 I](https://leetcode.cn/problems/count-the-number-of-special-characters-i/) · Easy · 灵茶山艾府：[计算集合交集，位运算做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3120.统计特殊字母的数量I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-special-characters-i/description/)

一趟遍历，使用两个集合upper和lower分别记录字符串中出现的大写字符和小写字符。接下来遍历lower中的小写字符，若其的大写版本出现在upper中，那么就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def numberOfSpecialChars(self, word):
        """
        :type word: str
        :rtype: int
        """

        upper = set()
        lower = set()
        for char in word:
            if 'a' <= char <= 'z':
                lower.add(char)
            else:
                upper.add(char)
        
        res = 0
        for char in lower:
            if chr(ord(char) - 32) in upper:
                res += 1
        
        return res
```
