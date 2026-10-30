---
title: "3163. 压缩字符串III"
aliases: ["yiduobo的每日leetcode 3163.压缩字符串III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704773217"
zhihu_id: "704773217"
zhihu_title: "yiduobo的每日leetcode 3163.压缩字符串III"
question_id: "3163"
question: "压缩字符串 III"
problem_url: "https://leetcode.cn/problems/string-compression-iii/"
difficulty: "Medium"
created: "2024-06-21T23:59:13+08:00"
updated: "2024-06-21T23:59:13+08:00"
upvotes: 0
comments: 0
---

# 3163. 压缩字符串III

> **[yiduobo的每日leetcode 3163.压缩字符串III](https://zhuanlan.zhihu.com/p/704773217) · 知乎 · 2024-06-21 · 赞同 0**
> 力扣：[3163. 压缩字符串 III](https://leetcode.cn/problems/string-compression-iii/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3163.压缩字符串III

[. - 力扣（LeetCode）](https://leetcode.cn/problems/string-compression-iii/description/)

题目给出一个字符串word，要求对其进行压缩。压缩的方法为对于word的某个长度最多为9且由单字符构成的前缀，将其从word中移除，并将其长度以及构成的字符加入到答案中，重复此过程直到word为空。

直接按照题目的压缩方法，使用两个指针p和q将word中所有由同一个字符构成的子串分离出来。具体来说就是对于从下标p开始的字符串，令q等于p，接下来将q向后迭代，找到第一个不等于word[p]的字符或者来到字符串末尾为止，此时word[p: q]这一段就是一个由同一个字符串构成的子串。接下来将p置为q然后重复此过程，直到p来到字符串末尾为止。

而对于对于某个由同一个字符c构成的子串，若其长度为length，那么就可以构成length // 9个"9c"，另外当length不是9的倍数时，令r \= length % 9，此时还需要将剩下的c压缩成r"c"。

最后附上python代码：

```python
class Solution(object):
    def compressedString(self, word):
        """
        :type word: str
        :rtype: str
        """

        res = []
        p = 0
        while p < len(word):
            q = p
            while q < len(word) and word[p] == word[q]:
                q += 1
            
            length = q - p
            for _ in range(length // 9):
                res.append('9')
                res.append(word[p])
            length %= 9
            if length > 0:
                res.append(str(length))
                res.append(word[p])
            
            p = q
        
        return ''.join(res)
```
