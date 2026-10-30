---
title: "1071. 字符串的最大公因子"
aliases: ["yiduobo的每日leetcode 1071.字符串的最大公因子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372412840"
zhihu_id: "372412840"
zhihu_title: "yiduobo的每日leetcode 1071.字符串的最大公因子"
question_id: "1071"
question: "字符串的最大公因子"
problem_url: "https://leetcode.cn/problems/greatest-common-divisor-of-strings/"
created: "2021-05-14T21:46:41+08:00"
updated: "2021-05-14T21:46:41+08:00"
upvotes: 0
comments: 0
---

# 1071. 字符串的最大公因子

> **[yiduobo的每日leetcode 1071.字符串的最大公因子](https://zhuanlan.zhihu.com/p/372412840) · 知乎 · 2021-05-14 · 赞同 0**
> 力扣：[1071. 字符串的最大公因子](https://leetcode.cn/problems/greatest-common-divisor-of-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1071.字符串的最大公因子

[力扣](https://leetcode-cn.com/problems/greatest-common-divisor-of-strings/)

不妨设这个最大公因子为P，那么str1和str2就分别应该是P \* m以及P \* n构成，其中m和n分别等于len(str1) / len(P)以及len(str2) / len(P)。

若答案存在，那么这里的m和n必然是互质的，证明也很简单。若m和n不互质，可以设二者存在公约数k，就有m \= k \* m'，n \= k \* n'，那么此时的答案就不应该是P，而因该是kP了，与P是最大公因子产生了矛盾。

知道m和n互质之后，那么很明显这里的len(P)就必然是len(str1)和len(str2)的最大公约数，设其为l。求出l之后，还需判断str1[:l] \* m是否等于str1，且str1[:l] \* n是否等于str2即可。若都满足，那么答案就是str1[:l]，否则答案为空。

最后附上python代码：

```python
class Solution(object):
    def gcdOfStrings(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """

        m = len(str1)
        n = len(str2)

        l, o = m, n
        while o:
            l, o = o, l % o
        
        if m < n:
            tmp = str1[:l] * (m / l)
            if tmp != str1:
                return ''
            tmp += str1[:l] * ((n - m) / l)
            if tmp == str2:
                return str1[:l]
            else:
                return ''
        else:
            tmp = str1[:l] * (n / l)
            if tmp != str2:
                return ''
            tmp += str1[:l] * ((m - n) / l)
            if tmp == str1:
                return str1[:l]
            else:
                return ''
```
