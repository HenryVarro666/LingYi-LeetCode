---
title: "318. 最大单词长度乘积"
aliases: ["yiduobo的每日leetcode 318.最大单词长度乘积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/159217513"
zhihu_id: "159217513"
zhihu_title: "yiduobo的每日leetcode 318.最大单词长度乘积"
question_id: "318"
question: "最大单词长度乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-word-lengths/"
created: "2020-07-13T22:06:00+08:00"
updated: "2020-07-13T22:06:00+08:00"
upvotes: 0
comments: 0
---

# 318. 最大单词长度乘积

> **[yiduobo的每日leetcode 318.最大单词长度乘积](https://zhuanlan.zhihu.com/p/159217513) · 知乎 · 2020-07-13 · 赞同 0**
> 力扣：[318. 最大单词长度乘积](https://leetcode.cn/problems/maximum-product-of-word-lengths/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

318.最大单词长度乘积<https://leetcode-cn.com/problems/maximum-product-of-word-lengths/>

题目要求找到两个不含重复字符的字符串，那么对于一个字符串，我们实际上只关心某个字符是否出现过，而不关心其出现的次数，又由于题目保证了所有的字符都是小写的，因此可以利用一个长度为26的二进制串来表示每个单词中字母出现的情况。

例如样例二中的["a","ab","abc","d","cd","bcd","abcd"]，分别可以表示为

a: 000...0001

ab: 000...0011

abc: 000...0111

d: 000...1000

cd: 000...1100

bcd: 000...1110

abcd: 000...1111

由于2^26 \< 2^31 - 1，因此每个字符串都可以通过一个整数来表示，而判断两个字符串中是否有相同的字符，只需要判断两个整数按位与是否为零即可。

于是将所有字符串转化为整数表示，同时记录下字符串长度之后，再通过两重循环枚举所有可能性即可。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        len_list = []
        for word in words:
            tmp = 0
            for char in word:
                tmp |= 1 << (ord(char) - 97)
            len_list.append([tmp, len(word)])

        res = 0
        for i in range(len(len_list) - 1):
            for j in range(i + 1, len(len_list)):
                if len_list[i][0] & len_list[j][0] == 0 and len_list[i][1] * len_list[j][1] > res:
                    res = len_list[i][1] * len_list[j][1]

        return res
```
