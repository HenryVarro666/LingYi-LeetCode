---
title: "2309. 兼具大小写的最好英文字母"
aliases: ["yiduobo的每日leetcode 2309.兼具大小写的最好英文字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/string", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/555767418"
zhihu_id: "555767418"
zhihu_title: "yiduobo的每日leetcode 2309.兼具大小写的最好英文字母"
question_id: "2309"
question: "兼具大小写的最好英文字母"
problem_url: "https://leetcode.cn/problems/greatest-english-letter-in-upper-and-lower-case/"
difficulty: "Easy"
created: "2022-08-19T22:57:34+08:00"
updated: "2022-08-19T22:57:34+08:00"
upvotes: 1
comments: 0
---

# 2309. 兼具大小写的最好英文字母

> **[yiduobo的每日leetcode 2309.兼具大小写的最好英文字母](https://zhuanlan.zhihu.com/p/555767418) · 知乎 · 2022-08-19 · 赞同 1**
> 力扣：[2309. 兼具大小写的最好英文字母](https://leetcode.cn/problems/greatest-english-letter-in-upper-and-lower-case/) · Easy · 灵茶山艾府：[统计 + 倒序枚举（附位运算做法）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2309.兼具大小写的最好英文字母

[力扣](https://leetcode.cn/problems/greatest-english-letter-in-upper-and-lower-case/)

将s中的所有字符加入到哈希表中，然后从Z到A进行反向的遍历，若当前字符以及其小写形式都出现在哈希表中，那么该字符就是答案。

若遍历完都没有找到合法的答案，那么就返回空。

最后附上python代码：

```python
class Solution(object):
    def greatestLetter(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_set = set(s)
        
        for index in range(25, -1, -1):
            upper_char = chr(index + 65)
            lower_char = chr(index + 97)
            if upper_char in char_set and lower_char in char_set:
                return upper_char

        return ''
```
