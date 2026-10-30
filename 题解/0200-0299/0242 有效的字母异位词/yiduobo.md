---
title: "242. 有效的字母异位词"
aliases: ["yiduobo的每日leetcode 242.有效的字母异位词"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "题单/面试经典-150-题", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150842353"
zhihu_id: "150842353"
zhihu_title: "yiduobo的每日leetcode 242.有效的字母异位词"
question_id: "242"
question: "有效的字母异位词"
problem_url: "https://leetcode.cn/problems/valid-anagram/"
difficulty: "Easy"
created: "2020-06-26T18:04:46+08:00"
updated: "2020-06-26T18:04:46+08:00"
upvotes: 1
comments: 0
---

# 242. 有效的字母异位词

> **[yiduobo的每日leetcode 242.有效的字母异位词](https://zhuanlan.zhihu.com/p/150842353) · 知乎 · 2020-06-26 · 赞同 1**
> 力扣：[242. 有效的字母异位词](https://leetcode.cn/problems/valid-anagram/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

242.有效的字母异位词<https://leetcode-cn.com/problems/valid-anagram/>

比较基础的题目。首先两个词长度必须要相等，然后使用dict统计其中一个词中各个字母的频率，再逐个判断另一个词中的字母是否出现在dict中且出现次数相等即可。

最后附上python代码：

```python
class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        chars = {}
        for char in s:
            chars[char] = chars.get(char, 0) + 1
        
        for char in t:
            if chars.get(char, 0) == 0:
                return False
            chars[char] -= 1
            
        return len(s) == len(t)
```
