---
title: "409. 最长回文串"
aliases: ["yiduobo的每日leetcode 409.最长回文串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/186229859"
zhihu_id: "186229859"
zhihu_title: "yiduobo的每日leetcode 409.最长回文串"
question_id: "409"
question: "最长回文串"
problem_url: "https://leetcode.cn/problems/longest-palindrome/"
created: "2020-08-16T18:44:04+08:00"
updated: "2020-08-16T18:44:04+08:00"
upvotes: 1
comments: 0
---

# 409. 最长回文串

> **[yiduobo的每日leetcode 409.最长回文串](https://zhuanlan.zhihu.com/p/186229859) · 知乎 · 2020-08-16 · 赞同 1**
> 力扣：[409. 最长回文串](https://leetcode.cn/problems/longest-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

409.最长回文串<https://leetcode-cn.com/problems/longest-palindrome/>

比较基础的题目。统计出串中每个字符出现的次数，那么可以将所有字符两个两个加入到答案的两侧。处理完之后，如果还剩下落单的字符，那么可以选取某一个作为答案的正中字符。

最后附上python代码：

```python
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: int
        """

        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        single = 0
        res = 0
        for cnt in char_dict.values():
            if cnt % 2 == 1:
                single = 1
                res += cnt - 1
            else:
                res += cnt

        return res + single
```
