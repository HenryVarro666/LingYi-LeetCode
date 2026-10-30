---
title: "3744. 在展开字符串中查找第K个字符"
aliases: ["yiduobo的每日leetcode 3744.在展开字符串中查找第K个字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1971712849173787102"
zhihu_id: "1971712849173787102"
zhihu_title: "yiduobo的每日leetcode 3744.在展开字符串中查找第K个字符"
question_id: "3744"
question: "在展开字符串中查找第K个字符"
problem_url: "https://leetcode.cn/problems/find-kth-character-in-expanded-string/"
created: "2025-11-11T23:06:27+08:00"
updated: "2025-11-11T23:07:09+08:00"
upvotes: 2
comments: 0
---

# 3744. 在展开字符串中查找第K个字符

> **[yiduobo的每日leetcode 3744.在展开字符串中查找第K个字符](https://zhuanlan.zhihu.com/p/1971712849173787102) · 知乎 · 2025-11-11 · 赞同 2**
> 力扣：[3744. 在展开字符串中查找第K个字符](https://leetcode.cn/problems/find-kth-character-in-expanded-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3744.在展开字符串中查找第K个字符

[3744. 在展开字符串中查找第 K 个字符 - 力扣（LeetCode）](https://leetcode.cn/problems/find-kth-character-in-expanded-string/description/)

题目给出一个字符串s，其长度不超过10^5。s由一个或多个单词组成，这些单词都由小写英文字母组成，单词之间由单个空格分隔，且s不包含前导或者后缀空格。

现在要求将s展开得到字符串t：对s中的每个单词，重复一次这个单词的第一个字符，然后重复两次第二个字符，以此类推。例如s \= "hello world"，那么t \= "heelllllllooooo woorrrllllddddd"。

给出一个整数k，k的大小在0到len(t) - 1之间，问t中下标为k的字符是什么。

为了方便计算，可以先将k加上1，将问题变成t中第k个字符是什么，在理解上会更加直观。

对于一个长度为length的单词，其扩展后的长度就是1 + 2 + ... + length \= (length + 1) \* lenght // 2。基于这一点，就可以将s按空格切分，接下来一趟遍历。对于当前单词，可以先计算其扩展后的长度exp_length，若k大于exp_length，说明答案在后续的单词中，否则说明答案就在当前单词中。

对于前面这种情况，需要让k减去exp_length，若此时的k为1，那么最终答案就是空格，否则需要将k减去1，然后继续考虑下一个单词。

对于后面这种情况，则只需遍历当前这个单词，对于处于下标index的字符c，若k小于等于index + 1，则说明答案就是c，否则需要将k减去index + 1，然后考虑下一个字符，直到找到答案为止。

最后附上python代码：

```python
class Solution(object):
    def kthCharacter(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        k += 1
        for w in s.split():
            word_length = len(w)
            exp_length = (word_length + 1) * word_length // 2
            if k <= exp_length:
                for index, c in enumerate(w):
                    if k <= index + 1:
                        return c
                    k -= index + 1
            else:
                k -= exp_length
                if k == 1:
                    return " "
                k -= 1
```
