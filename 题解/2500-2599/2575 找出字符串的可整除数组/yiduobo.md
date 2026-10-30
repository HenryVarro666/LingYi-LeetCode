---
title: "2575. 找出字符串的可整除数组"
aliases: ["yiduobo的每日leetcode 2575.找出字符串的可整除数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642010167"
zhihu_id: "642010167"
zhihu_title: "yiduobo的每日leetcode 2575.找出字符串的可整除数组"
question_id: "2575"
question: "找出字符串的可整除数组"
problem_url: "https://leetcode.cn/problems/find-the-divisibility-array-of-a-string/"
difficulty: "Medium"
created: "2023-07-07T01:11:26+08:00"
updated: "2023-07-07T01:11:26+08:00"
upvotes: 0
comments: 0
---

# 2575. 找出字符串的可整除数组

> **[yiduobo的每日leetcode 2575.找出字符串的可整除数组](https://zhuanlan.zhihu.com/p/642010167) · 知乎 · 2023-07-07 · 赞同 0**
> 力扣：[2575. 找出字符串的可整除数组](https://leetcode.cn/problems/find-the-divisibility-array-of-a-string/) · Medium · 灵茶山艾府：[模运算的性质+从左到右计算（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2575.找出字符串的可整除数组

[力扣](https://leetcode.cn/problems/find-the-divisibility-array-of-a-string/)

题目给出一个字符串word和一个正整数m，要求判断字符串的所有前缀是否可以整除m。

对于word中两个相邻的前缀word[:p]以及word[:p + 1]而言，后者就相当于前者乘以10再加上word[p]。根据取模的性质，就可以利用每个前缀左侧相邻前缀对m取模的结果，推算出当前前缀对m取模的结果，也就是初始化r[0] \= word[0] % m，然后对于所有的i > 0都有r[i] \= (r[i - 1] \* 10 + word[i]) % m

根据这个式子，就可以从头开始一趟遍历，计算出每一位对m取模的结果并根据模是否为0填充答案数组了。

最后附上python代码：

```python
class Solution(object):
    def divisibilityArray(self, word, m):
        """
        :type word: str
        :type m: int
        :rtype: List[int]
        """

        now = 0
        res = []
        for char in word:
            now = now * 10 + int(char)
            now %= m
            if now == 0:
                res.append(1)
            else:
                res.append(0)
        
        return res
```
