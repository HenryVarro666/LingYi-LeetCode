---
title: "1408. 数组中的字符串匹配"
aliases: ["yiduobo的每日leetcode 1408.数组中的字符串匹配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405932817"
zhihu_id: "405932817"
zhihu_title: "yiduobo的每日leetcode 1408.数组中的字符串匹配"
question_id: "1408"
question: "数组中的字符串匹配"
problem_url: "https://leetcode.cn/problems/string-matching-in-an-array/"
created: "2021-09-01T23:29:08+08:00"
updated: "2021-09-01T23:29:08+08:00"
upvotes: 0
comments: 0
---

# 1408. 数组中的字符串匹配

> **[yiduobo的每日leetcode 1408.数组中的字符串匹配](https://zhuanlan.zhihu.com/p/405932817) · 知乎 · 2021-09-01 · 赞同 0**
> 力扣：[1408. 数组中的字符串匹配](https://leetcode.cn/problems/string-matching-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1408.数组中的字符串匹配

[力扣](https://leetcode-cn.com/problems/string-matching-in-an-array/)

由于这里的字符串数目很少，且长度也很短，因此直接使用暴力匹配也是可以的。我在这里采用的是之前使用过的类rk算法的前缀哈希算法。

具体来说就是先将字符串按长度从大到小进行排序，然后对于每个字符串，先将其按照29进制编码。由于这个编码很大，因此要将其对10^9 + 7取模。

接下来对于当前字符串s：

1、若其编码之前出现过，说明其是某个字符串的子串，那么将当前字符串加入到答案当中。此时无需计算s的子串的编码，因为若某个字符串t是s的字符，而s又是另一个字符串的子串，因此t也必然是另一个字符串的子串，因此就没有必要计算s的子串的编码值了。

2、若其编码没有出现过，那么就需要计算其每个子串的编码值，并将其加入到哈希表中。

最后附上python代码：

```python
class Solution(object):
    def stringMatching(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """

        mod = 10 ** 9 + 7
        p = [1]
        for index in range(30):
            p.append(p[-1] * 29 % mod)

        hash_list = [set() for _ in range(31)]
        res = []
        for word in sorted(words, key=lambda d:-len(d)):
            v = [ord(word[0]) - 97]
            for char in word[1:]:
                v.append((v[-1] * 29 + ord(char) - 97) % mod)

            n = len(word)
            if v[-1] in hash_list[n]:
                res.append(word)
            else:
                hash_list[n].add(v[-1])
                for l in range(1, n):
                    hash_list[l].add(v[l - 1])
                    for index in range(l, n):
                        hash_list[l].add((v[index] - (v[index - l] * p[l] % mod) + mod) % mod)

        return res
```
