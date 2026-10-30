---
title: "647. 回文子串"
aliases: ["yiduobo的每日leetcode 647.回文子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/string", "leetcode/enumeration", "题单/动态规划", "题单/字符串", "题单/动态规划/八-区间-DP", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/274878472"
zhihu_id: "274878472"
zhihu_title: "yiduobo的每日leetcode 647.回文子串"
question_id: "647"
question: "回文子串"
problem_url: "https://leetcode.cn/problems/palindromic-substrings/"
difficulty: "Medium"
created: "2020-11-05T22:59:59+08:00"
updated: "2020-11-05T22:59:59+08:00"
upvotes: 0
comments: 0
---

# 647. 回文子串

> **[yiduobo的每日leetcode 647.回文子串](https://zhuanlan.zhihu.com/p/274878472) · 知乎 · 2020-11-05 · 赞同 0**
> 力扣：[647. 回文子串](https://leetcode.cn/problems/palindromic-substrings/) · Medium · 灵茶山艾府：[两种方法：中心扩展法 / Manacher 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

647.回文子串

[力扣](https://leetcode-cn.com/problems/palindromic-substrings/)

首先，对于一个长度为奇数回文串，若其回文半径为k，设其回文中心为c，那么以c为回文中心的回文子串就有k个。例如回文串abcdefgfedcba，其回文半径为abcdefg，长度为7，而已字母g为中心的回文子串有

g、fgf、efgfe、defgfed、cdefgfedc、bcdefgfedcb、abcdefgfedcba

恰好也是7个。

有了上面的结论，题目要计算字符串中所有回文子串的个数，那么我们可以将题目转化对于字符串中的每个字符，若该字符为回文中心，那么回文半径是多少。最后答案就是所有的回文半径之和。

但是需要注意的是，对于长度为偶数的回文串是不好标定中心的，因此一个常见的做法就是在每个字符两侧都插入特殊字符，这样就能保证所有的回文串长度都是奇数了。那么对于字符串中的每个字符，设以该字符为中心的回文半径为k，那么就有：

1、若该字符为正常字符：

那么这里形成的回文子串必然是 \#a\#b\#...\#c\#...\#b\#a\# 这种形式，其中\#为我们插入的特殊字符，c为回文中心。

回文半径为 \#a\#b\#...\#c，其长度k必然是偶数，那么正常字符一共就有k/2个，即回文半径为k/2。

2、若该字符为\#：

此时形成的回文子串必然是 \#a\#b\#...\#c\#c\#...\#b\#a\# 这种形式。

回文半径为\#a\#b...\#c\#，其长度k必然是奇数，那么正常字符一共就有(k - 1) / 2个。由于k是奇数，那么可以直接用k整除2，那么此时的回文半径也是k/2。

于是现在的做法就是对于每个字符s[index]求出其回文半径f[index]，那么最终答案就是sum(f[index] / 2)。

对于求出每个字符的回文半径，我们可以直接使用之前第五题的马拉车算法，在O(n)的时间复杂度内求出每个字符的回文半径。

[yiduobo：yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786)

最后附上python代码：

```python
class Solution(object):
    def countSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        s = '#' + '#'.join(list(s)) + '#'
        f = []
        mid = 0
        right = 0
        for index in range(len(s)):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while index >= f[index] and index + f[index] < len(s) and s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        res = 0
        for index in range(len(s)):
            res += f[index] / 2

        return res
```
