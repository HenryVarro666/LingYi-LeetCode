---
title: "1897. 重新分配字符使所有字符串都相等"
aliases: ["yiduobo的每日leetcode 1897.重新分配字符使所有字符串都相等"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479839962"
zhihu_id: "479839962"
zhihu_title: "yiduobo的每日leetcode 1897.重新分配字符使所有字符串都相等"
question_id: "1897"
question: "重新分配字符使所有字符串都相等"
problem_url: "https://leetcode.cn/problems/redistribute-characters-to-make-all-strings-equal/"
difficulty: "Easy"
created: "2022-03-12T20:05:42+08:00"
updated: "2022-03-12T20:05:42+08:00"
upvotes: 0
comments: 0
---

# 1897. 重新分配字符使所有字符串都相等

> **[yiduobo的每日leetcode 1897.重新分配字符使所有字符串都相等](https://zhuanlan.zhihu.com/p/479839962) · 知乎 · 2022-03-12 · 赞同 0**
> 力扣：[1897. 重新分配字符使所有字符串都相等](https://leetcode.cn/problems/redistribute-characters-to-make-all-strings-equal/) · Easy · 灵茶山艾府：[计算每个字母个数的平均数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1897.重新分配字符使所有字符串相等

[力扣](https://leetcode-cn.com/problems/redistribute-characters-to-make-all-strings-equal/)

由于题目可以任意调整字符串的构成，那么只需要每种字符出现的次数都是n的倍数，就可以将当前字符平均分配到各个字符串上的同一位置，从而使得所有字符串都相等。这里的n是字符串的总数。

最后附上python代码：

```python
class Solution(object):
    def makeEqual(self, words):
        """
        :type words: List[str]
        :rtype: bool
        """

        cnt_dict = {}
        for word in words:
            for char in word:
                cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        for cnt in cnt_dict.values():
            if cnt % len(words) != 0:
                return False
        
        return True
```
