---
title: "1805. 字符串中不同整数的数目"
aliases: ["yiduobo的每日leetcode 1805.字符串中不同整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464210134"
zhihu_id: "464210134"
zhihu_title: "yiduobo的每日leetcode 1805.字符串中不同整数的数目"
question_id: "1805"
question: "字符串中不同整数的数目"
problem_url: "https://leetcode.cn/problems/number-of-different-integers-in-a-string/"
difficulty: "Easy"
created: "2022-02-05T23:38:34+08:00"
updated: "2022-02-05T23:38:34+08:00"
upvotes: 0
comments: 0
---

# 1805. 字符串中不同整数的数目

> **[yiduobo的每日leetcode 1805.字符串中不同整数的数目](https://zhuanlan.zhihu.com/p/464210134) · 知乎 · 2022-02-05 · 赞同 0**
> 力扣：[1805. 字符串中不同整数的数目](https://leetcode.cn/problems/number-of-different-integers-in-a-string/) · Easy · 灵茶山艾府：[Go 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1805.字符串中不同整数的数目

[力扣](https://leetcode-cn.com/problems/number-of-different-integers-in-a-string/)

比较基础的题目，一趟遍历将word中的数分离出来并加入到哈希表中。最后哈希表的大小就是最终答案。

需要注意的是，这里的字符串长度可达1000，那么对于部分语言来说是不适合将字符串转为整数储存的，而使用字符串储存的话则需要注意处理前导0的情况。

最后附上python代码：

```python
class Solution(object):
    def numDifferentIntegers(self, word):
        """
        :type word: str
        :rtype: int
        """

        num_set = set()
        start = None
        for index, char in enumerate(word):
            if char >= '0' and char <= '9':
                if start is None:
                    start = index
            else:
                if start is not None:
                    while start < index - 1 and word[start] == '0':
                        start += 1
                    num_set.add(word[start:index])
                start = None
        
        if start is not None:
            while start < len(word) - 1 and word[start] == '0':
                start += 1
            num_set.add(word[start:])
        
        return len(num_set)
```
