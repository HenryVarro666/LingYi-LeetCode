---
title: "LCP 25. 古董键盘"
aliases: ["yiduobo的每日leetcode LCP25.古董键盘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/573406374"
zhihu_id: "573406374"
zhihu_title: "yiduobo的每日leetcode LCP25.古董键盘"
question_id: "LCP 25"
question: "古董键盘"
created: "2022-10-14T00:50:56+08:00"
updated: "2022-10-14T00:50:56+08:00"
upvotes: 0
comments: 0
---

# LCP 25. 古董键盘

> **[yiduobo的每日leetcode LCP25.古董键盘](https://zhuanlan.zhihu.com/p/573406374) · 知乎 · 2022-10-14 · 赞同 0**
> 力扣：LCP 25. 古董键盘

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP25.古董键盘

[力扣](https://leetcode.cn/problems/Uh984O/)

由于题目的k比较小，那么可以先强行枚举出所有的组成情况，然后计算有多少种可能的排列方式。

具体来说，就是设置一个长度为k的数组choose，满足

choose[0] + choose[1] + ... + choose[k - 1] \= 26

choose[0] \* k + choose[1] \* (k - 1) + ... + choose[k - 1] \= n

即最终的排列中，有choose[0]个字母出现了k次，choose[1]个字母出现了k - 1次，以此类推。

由于k不超过5，那么可以直接暴力dfs找出所有可行的choose数组。

接下来对于某个choose数组，需要计算在这种情况下可能的排列方式。

首先是选字母。第一轮，从26个字母中选出choose[0]个出现了k次的字母，一共有C(26, choose[0])种可能。第二轮，从26 - choose[0]个字母中选出choose[1]个出现了k - 1次的字母，一共有C(26, choose[1])中可能。以此类推。那么选字母的环节，每个choose数组对应的可能性就是

C(26, choose[0]) \* C(26 - choose[0], choose[1]) \* ... \* C(26 - choose[0] - ... choose[k - 2], choose[k - 1])

为了提高效率，在这里可以提前预处理出26及以内的组合数

接下来是计算排列方式。一共n个字符的排列，理论上应该有n!种不同的方案，但是由于其中某些字母出现了多次，那么必然会导致一些重复。对于去重问题，可以参考之前做过的1830题，应该是完全相同的场景。除此之外，由于阶乘中的除法操作，也可以采用与1830题相同的做法，通过乘法逆元来解决，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 1830.使字符串有序的最少操作次数](https://zhuanlan.zhihu.com/p/467924214)

得到了选字母方案数与字母排列数之后，二者相乘就是当前的choose数组对应的方案数了。将每种不同的choose数组对应的方案数计算出来然后累加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def keyboard(self, k, n):
        """
        :type k: int
        :type n: int
        :rtype: int
        """

        C = [[0] * 27 for _ in range(27)]
        C[0][0] = C[1][0] = C[1][1] = 1
        mod = 10 ** 9 + 7
        for i in range(2, 27):
            C[i][0] = C[i][i] = 1
            for j in range(1, i):
                C[i][j] = C[i - 1][j] + C[i - 1][j - 1]
                if C[i][j] >= mod:
                    C[i][j] -= mod
        self.res = 0

        def quick_pow(base, p):
            if p == 0:
                return 1
            elif p == 1:
                return base
            else:
                tmp = quick_pow(base, p / 2)
                tmp = tmp * tmp % mod
                if p % 2 == 1:
                    tmp = tmp * base % mod
                return tmp

        rev_fac_pow = [[], [1], [1], [1], [1], [1]]
        fac = 1
        for index in range(1, k + 1):
            fac *= index
            rev_fac_pow[index].append(quick_pow(fac, mod - 2))
            p = 2
            while p * index <= n:
                rev_fac_pow[index].append(rev_fac_pow[index][-1] * rev_fac_pow[index][1] % mod)
                p += 1
        
        def dfs(choose, level, rest_alpha, rest_n):
            if level == k - 1:
                if rest_alpha < rest_n:
                    return
                now = 1
                tot = 26
                choose.append(rest_n)
                for index in range(k):
                    now = now * C[tot][choose[index]] % mod
                    now = now * rev_fac_pow[k - index][choose[index]] % mod
                    tot -= choose[index]

                for index in range(1, n + 1):
                    now = now * index % mod
                
                self.res += now
                choose.pop()
                return
            
            cnt = 0
            while cnt <= rest_alpha and cnt * (k - level) <= rest_n:
                choose.append(cnt)
                dfs(choose, level + 1, rest_alpha - cnt, rest_n - choose[-1] * (k - level))
                cnt += 1
                choose.pop()
        
        choose = []
        dfs(choose, 0, 26, n)
        return self.res % mod
```
