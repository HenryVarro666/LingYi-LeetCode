---
title: "1170. 比较字符串中最小字母出现频次"
aliases: ["yiduobo的每日leetcode 1170.比较字符串中最小字母出现频次"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379359257"
zhihu_id: "379359257"
zhihu_title: "yiduobo的每日leetcode 1170.比较字符串中最小字母出现频次"
question_id: "1170"
question: "比较字符串中最小字母出现频次"
problem_url: "https://leetcode.cn/problems/compare-strings-by-frequency-of-the-smallest-character/"
created: "2021-06-09T23:31:28+08:00"
updated: "2021-06-09T23:31:28+08:00"
upvotes: 0
comments: 0
---

# 1170. 比较字符串中最小字母出现频次

> **[yiduobo的每日leetcode 1170.比较字符串中最小字母出现频次](https://zhuanlan.zhihu.com/p/379359257) · 知乎 · 2021-06-09 · 赞同 0**
> 力扣：[1170. 比较字符串中最小字母出现频次](https://leetcode.cn/problems/compare-strings-by-frequency-of-the-smallest-character/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1170.比较字符串中最小字母出现频次

[力扣](https://leetcode-cn.com/problems/compare-strings-by-frequency-of-the-smallest-character/)

首先，我们可以根据题目意思找出每个word中最小字母出现的频次，由于word的长度不超过两千，那么我们在这里就得到了一个数组a，a中的值都不超过两千。

接下来我们对于每个query，按同样的方法求出其最小字母出现的频次，设为k，那么此时我们就需要找出t中有多少个值大于k。

由于a中的值都不超过两千，因此很自然想到使用哈希表来处理。对于a中的值a[index]，我们将哈希表对应下标为a[index]的位置加上1，那么最终得到的哈希表t中，t[index]就表示a中有多少个值为index的数。

此时我们要求a中要多少个值大于k的数，那么就等于res \= t[k + 1] + t[k + 2] + ... + t[-1]。这是一个子段和问题，那么可以再进一步转化成前缀和的问题来解决了，即res \= (t[0] + t[1] + ... + t[-1]) - (t[0] + t[1] + ... + t[k]) \= s[-1] - s[k]

最后附上python代码：

```python
class Solution(object):
    def numSmallerByFrequency(self, queries, words):
        """
        :type queries: List[str]
        :type words: List[str]
        :rtype: List[int]
        """

        t = [0] * 2001
        for word in words:
            cnt = 0
            now = None
            for char in word:
                if now is None or now > char:
                    now = char
                    cnt = 1
                elif now == char:
                    cnt += 1
            t[cnt] += 1

        s = t[:]
        for index in range(1, 2001):
            s[index] += s[index - 1]
        
        res = []
        for word in queries:
            cnt = 0
            now = None
            for char in word:
                if now is None or now > char:
                    now = char
                    cnt = 1
                elif now == char:
                    cnt += 1
            
            res.append(s[-1] - s[cnt])

        return res
```
