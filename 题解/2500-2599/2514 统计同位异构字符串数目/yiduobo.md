---
title: "2514. 统计同位异构字符串数目"
aliases: ["yiduobo的每日leetcode 2514.统计同位异构字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634843567"
zhihu_id: "634843567"
zhihu_title: "yiduobo的每日leetcode 2514.统计同位异构字符串数目"
question_id: "2514"
question: "统计同位异构字符串数目"
problem_url: "https://leetcode.cn/problems/count-anagrams/"
difficulty: "Hard"
rating: 2070
created: "2023-06-06T19:22:12+08:00"
updated: "2023-06-06T19:22:12+08:00"
upvotes: 0
comments: 0
---

# 2514. 统计同位异构字符串数目

> **[yiduobo的每日leetcode 2514.统计同位异构字符串数目](https://zhuanlan.zhihu.com/p/634843567) · 知乎 · 2023-06-06 · 赞同 0**
> 力扣：[2514. 统计同位异构字符串数目](https://leetcode.cn/problems/count-anagrams/) · Hard · 灵茶山艾府：[组合计数（视频讲解）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2514.统计同位异构字符串数目

[力扣](https://leetcode.cn/problems/count-anagrams/)

题目中各个单词间的字符不能打乱使用，换言之各个单词之间是互不相关的，因此在这里就可以使用乘法原理，对于每个单词计算出该单词的异构单词数目，然后将这些数目全部相乘得到最后答案。

对于单个单词，不妨设其长度为word_len，那么这些字符的排列方式数目就是word_len的阶乘，不过其中某些字符出现了多次会产生重复计数，需要除以每种字符串出现次数的阶乘。更具体的说明可以参考之前的1830题：

[yiduobo：yiduobo的每日leetcode 1830.使字符串有序的最少操作次数](https://zhuanlan.zhihu.com/p/467924214)

由于本题的数据规模较大，同时涉及到了除法与取模，因此需要使用到乘法逆元。在具体实现上，为了避免重复的计算，可以先将单词长度的阶乘和去重时除以单个字符串出现次数的阶乘分别使用两个变量累乘起来并取模，然后对去重用的这个乘积计算乘法逆元，再与单词长度阶乘的乘积相乘得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def countAnagrams(self, s):
        """
        :type s: str
        :rtype: int
        """

        mod = 10 ** 9 + 7

        def quickPow(base, k):
            if k == 1:
                return base
            
            p = quickPow(base, k / 2)
            p *= p
            if k & 1:
                p *= base
            
            return p % mod

        res = 1
        divide = 1
        fac_len = 1
        fac = [1]
        for word in s.split(' '):
            word_len = len(word)
            cnt = {}
            for char in word:
                cnt[char] = cnt.get(char, 0) + 1
            
            if word_len >= fac_len:
                for index in range(fac_len, word_len + 1):
                    fac.append(fac[-1] * index % mod)
                fac_len = word_len + 1
            
            res *= fac[word_len]
            res %= mod

            for char in cnt:
                divide *= fac[cnt[char]]
                divide %= mod

            
        return res * quickPow(divide, mod - 2) % mod
```
