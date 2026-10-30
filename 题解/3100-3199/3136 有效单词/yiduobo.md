---
title: "3136. 有效单词"
aliases: ["yiduobo的每日leetcode 3136.有效单词"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702629213"
zhihu_id: "702629213"
zhihu_title: "yiduobo的每日leetcode 3136.有效单词"
question_id: "3136"
question: "有效单词"
problem_url: "https://leetcode.cn/problems/valid-word/"
difficulty: "Easy"
created: "2024-06-11T00:07:37+08:00"
updated: "2024-06-11T00:07:37+08:00"
upvotes: 1
comments: 0
---

# 3136. 有效单词

> **[yiduobo的每日leetcode 3136.有效单词](https://zhuanlan.zhihu.com/p/702629213) · 知乎 · 2024-06-11 · 赞同 1**
> 力扣：[3136. 有效单词](https://leetcode.cn/problems/valid-word/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3136.有效单词

[. - 力扣（LeetCode）](https://leetcode.cn/problems/valid-word/description/)

题目给出一个字符串，要求判断其是否为有效单词。有效单词的定义为长度大于等于3，由大小写字符以及数字组成的字符串，且其中包含至少一个元音字符和一个辅音字符。

首先需要先判断字符串的长度是否大于等于3，接下来，由于元音字符较少，可以先将元音字符记录在集合vowel中，然后对字符串进行一趟遍历，使用两个变量v_flag和c_flag分别表示字符串中是否存在元音字符和辅音字符。对于当前遍历到的字符：

1、若其出现在vowel，那么就将v_flag置为true

2、否则就检测其是否为字符，如果是那么其必然为辅音字符，那么就将c_flag置为true

3、否则检测其是否为数字，如果不是说明出现了其他字符，此时直接返回false

遍历完成后，若v_flag和c_flag都为true，则返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def isValid(self, word):
        """
        :type word: str
        :rtype: bool
        """

        vowel = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])

        v_flag = False
        c_flag = False

        if len(word) < 3:
            return False
        
        for char in word:
            if char in vowel:
                v_flag = True
            elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                c_flag = True
            elif not '0' <= char <= '9':
                return False
        
        return v_flag and c_flag
```
