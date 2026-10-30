---
title: "1915. 最美子字符串的数目"
aliases: ["yiduobo的每日leetcode 1915.最美子字符串的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/bitmask", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/483740145"
zhihu_id: "483740145"
zhihu_title: "yiduobo的每日leetcode 1915.最美子字符串的数目"
question_id: "1915"
question: "最美子字符串的数目"
problem_url: "https://leetcode.cn/problems/number-of-wonderful-substrings/"
difficulty: "Medium"
rating: 2235
created: "2022-03-19T15:24:45+08:00"
updated: "2022-03-19T15:24:45+08:00"
upvotes: 1
comments: 0
---

# 1915. 最美子字符串的数目

> **[yiduobo的每日leetcode 1915.最美子字符串的数目](https://zhuanlan.zhihu.com/p/483740145) · 知乎 · 2022-03-19 · 赞同 1**
> 力扣：[1915. 最美子字符串的数目](https://leetcode.cn/problems/number-of-wonderful-substrings/) · Medium · 灵茶山艾府：[前缀和常见技巧（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1915.最美子字符串的数目

[力扣](https://leetcode-cn.com/problems/number-of-wonderful-substrings/)

题目只需要关注子字符串中各个字母的奇偶性，而不关心具体的数值。注意到题目中只有10个字符，那么可以使用2进制状态压缩来表示字符串的奇偶性。

另一方面，对于一个子字符串中各个字符的奇偶性，则可以通过经典的区间转前缀的做法，通过两个前缀字符串中各个字符的奇偶性来得知。这样一来，就得到了一种做法。

一趟遍历，使用一个哈希表cnt_dict来记录每种奇偶状态的前缀字符串出现的次数，并使用一个状态码now来记录到以当前字符结束的前缀字符串的奇偶状态。对于当前字符：

1、首先使用该字符更新now

2、接下来，若当前前缀字符串之前存在另外的前缀字符，其奇偶状态也是now，那么当前前缀字符串多出来的这个子字符串中每个字符出现的次数必然都是偶数，满足题目要求，因此需要使用cnt_dict[now]更新答案

3、另外，题目也允许其中一个字符出现奇数次，那么就可以在now的基础上枚举各个字符，计算出单个字符出现奇数次时的奇偶状态码last，并使用cnt_dict[last]来更新答案

4、最后，需要使用now来更新cnt_dict，然后继续考虑下一个字符

最后附上python代码：

```python
class Solution(object):
    def wonderfulSubstrings(self, word):
        """
        :type word: str
        :rtype: int
        """

        cnt_dict = {0 : 1}
        now = 0
        res = 0
        for char in word:
            now = now ^ (1 << (ord(char) - 97))
            res += cnt_dict.get(now, 0)
            for index in range(10):
                res += cnt_dict.get(now ^ (1 << index), 0)
            
            cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        return res
```
