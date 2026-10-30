---
title: "1830. 使字符串有序的最少操作次数"
aliases: ["yiduobo的每日leetcode 1830.使字符串有序的最少操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/467924214"
zhihu_id: "467924214"
zhihu_title: "yiduobo的每日leetcode 1830.使字符串有序的最少操作次数"
question_id: "1830"
question: "使字符串有序的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-string-sorted/"
created: "2022-02-15T23:40:21+08:00"
updated: "2022-02-15T23:40:21+08:00"
upvotes: 0
comments: 0
---

# 1830. 使字符串有序的最少操作次数

> **[yiduobo的每日leetcode 1830.使字符串有序的最少操作次数](https://zhuanlan.zhihu.com/p/467924214) · 知乎 · 2022-02-15 · 赞同 0**
> 力扣：[1830. 使字符串有序的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-string-sorted/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1830.使字符串有序的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-operations-to-make-string-sorted/)

题目中对单次操作的描述感觉在哪里见过，再看看样例1可以发现，题目中的操作不就是找到某个排列的上一个排列的算法吗？

题目问多少次操作可以使得字符串有序，也就是多少次操作可以回到最初的排列。对于这个问题，也可以看做问当前排列在所有排列中是第几小的排列，对于这个问题，可以使用经典的类康托展开算法来进行求解。

具体来说，就是对于一个长度为n，且以s[0]开头的排列s而言，比这个排列小的排列可以分成两个部分：

1、以比s[0]小的字符开头的排列

2、同样以s[0]开头的排列

首先对于第一种情况，若s[1:n]里面有k个小于s[0]的字符，那么以这些字符开头的排列都比s要小。而对于一个长度为n，固定了首位的排列而言，一共有(n - 1)！种可能的排列。不过需要注意的是，由于s中的字符可能重复，因此这里的(n - 1)！里面也可能出现重复的情况，需要去重。

例如排列baa，对于b而言后面的两个a都小于a，那么这里理论上应该有2 \* (3 - 1)！\= 4种排列比baa要小。但是实际上有两种是重复的。如果用a1和a2分别表示两个a，那么这里得到的应该是

a1 a2 b

a1 b a2

a2 a1 b

a2 b a1

实际上这里的1、3这一组和2、4这一组是完全重复了。

对于这个问题，可以换一种思路去看。例如aaaab这种情况，对于里面的四个2，如果将a进行a1、a2、a3、a4这种编号的话，那么将这些a互换一共有4！种可行的互换方式，也就是说aaaab这种形式的排列一共会被计算4！次。根据这个结论，就只需要统计s中各个字符出现的次数，然后使用k \* (n - 1)！/ （cnt['a']！\* cnt['b']！\* ... \* cnt['z']！)就能达到去重的目的了。

另外，由于这里是阶乘取模运算，且这里出现了除法，那么不可避免地这里需要用到乘法逆元。所谓乘法逆元就是指对于某个数b，存在一个inv_b，满足a / b对mod取模恰好就等于a \* inv_b对mod取模的结果。这样做的目的是由于除法在取模意义下是不满足(a / b) % mod \= (a % mod) / (b % mod)，因此在例如上式的阶乘除法然后取模的运算中是很难直接计算的。而如果使用inv_b，那么就有a \* inv_b % mod \= (a % mod) \* (inv_b % mod)，也就是说在这里可以在阶乘过程中边乘边取模。

对于inv_b的计算，比较简单的运用是在mod为质数时，有inv_b \= b^(mod - 2) % mod，证明也很简单，这里就不展开了。对于这里mod - 2次方的计算，由于mod很大，因此也需要用到快速幂来进行计算。

回到题目。由于这里每个字符出现的次数包含了1次到n次所有的可能性，因此需要实现预处理出1！到n！对mod的乘法逆元。

到了这里，情况1中排列的数目就可以计算了。而对于情况2而言，已经确定了s[0]的情况，可以认为是对s[1:n]这个长度为n - 1的排列，求解有多少个排列比这个排列小。这就是原问题在n - 1规模下的版本，那么直接套用规模为n时的做法，不断计算并向下迭代，直到排列的长度等于1为止。

最后附上python代码：

```python
class Solution(object):
    def makeStringSorted(self, s):
        """
        :type s: str
        :rtype: int
        """
        n = len(s)
        fac = [1]
        inv_fac = [1]
        mod = 10 ** 9 + 7
        for index in range(1, n + 1):
            fac.append(fac[-1] * index % mod)
            inv_fac.append(self.quickPow(fac[-1], mod - 2, mod))

        cnt_list = [0] * 26
        res = 0
        for index in range(n - 1, -1, -1):
            num = ord(s[index]) - 97
            cnt = sum(cnt_list[:num])
            tmp = cnt * fac[n - index - 1] % mod

            cnt_list[num] += 1
            for char_num in range(26):
                tmp = tmp * inv_fac[cnt_list[char_num]] % mod
            
            res += tmp
            if res >= mod:
                res -= mod

        return res

    def quickPow(self, base, k, mod):
        if k == 1:
            return base

        res = self.quickPow(base, k / 2, mod)
        res = res ** 2 % mod
        if k % 2 == 1:
            res = res * base % mod
        return res
```
