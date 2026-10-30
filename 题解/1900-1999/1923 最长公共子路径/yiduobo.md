---
title: "1923. 最长公共子路径"
aliases: ["yiduobo的每日leetcode 1923.最长公共子路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/suffix-array", "题单/字符串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/485432793"
zhihu_id: "485432793"
zhihu_title: "yiduobo的每日leetcode 1923.最长公共子路径"
question_id: "1923"
question: "最长公共子路径"
problem_url: "https://leetcode.cn/problems/longest-common-subpath/"
difficulty: "Hard"
rating: 2661
created: "2022-03-22T15:50:18+08:00"
updated: "2022-03-22T15:50:19+08:00"
upvotes: 0
comments: 0
---

# 1923. 最长公共子路径

> **[yiduobo的每日leetcode 1923.最长公共子路径](https://zhuanlan.zhihu.com/p/485432793) · 知乎 · 2022-03-22 · 赞同 0**
> 力扣：[1923. 最长公共子路径](https://leetcode.cn/problems/longest-common-subpath/) · Hard · 灵茶山艾府：[后缀数组+二分答案](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1923.最长公共子路径

[力扣](https://leetcode-cn.com/problems/longest-common-subpath/)

多个字符串的最长公共子串问题。由于字符串的数量上限和长度上限都比较大，那么在这里常规的动态规划做法肯定是不行的。

对于这类与字符串相等相关的问题，大多可以使用后缀数组来解决。可以明确的一点是，字符串的任何一个子串都是其某个后缀字符串的前缀，那么对后缀排序后就可以通过后缀间的公共前缀来得知某些子串是相等的。对于本题，则只需要将各个字符串拼接在一起，使用分隔符隔开，然后求后缀数组再二分答案即可。

不过有一说一，后缀数组确实蛮难写的，所以我在这里用的是rk算法。具体来说就是先二分答案，设当前处理的字符串长度为mid，那么就对每个字符串中所有长度为mid的子串按照某个base进制进行编码。当然这个编码可能会非常大，因此需要对这个编码进行哈希。若两个子串的哈希值一样，那么二者就可能相同。

一般来说，选择一个质数编码，然后对一个质数取模做哈希就能满足了。本题的数据好像还蛮强的，最后被迫用了两个质数分别做哈希。

而求所有长度为mid的子串的编码，则可以利用之前的结果。例如对于字符串中[l, r]这一段的编码，其形式应该是

c[r] \= (base^(r - l) \* s[l] + base^(r - l - 1) \* s[l + 1] + ... + base \* s[r - 1] + s[r]) % mod

而对于[l + 1, r + 1]这一段，则为

c[r + 1] \= (base^(r - l) \* s[l + 1] + base^(r - l - 1) \* s[l + 2] + ... + base \* s[r] + s[r + 1]) % mod

可以发现，下面这个式子可以认为是上面式子乘以base，然后去掉s[l]这一项，再加上s[r + 1]这一项得到的，于是可以先预处理出base的所有幂次，就有

c[r + 1] \= (c[r] \* base + s[r] - pow_base[r - l +1] \* s[l]) % mod

这样一来，就可以在均摊O(1)的时间复杂度内求出来一个字符串所有长度为mid的子字符串的编码。使用一个集合记录各个字符串拥有的公共编码，若最终集合不为空，说明存在某个子字符串出现在所有字符串中，那么更新二分下界l \= mid，否则更新二分上界r \= mid - 1。这里需要注意的是，这种二分的更新方式需要在计算mid时使用mid \= (l + r + 1) / 2来计算，而不能使用mid \= (l + r) / 2，从而避免mid一直等于l的情况出现。

最后附上python代码：

```python
class Solution(object):
    def longestCommonSubpath(self, n, paths):
        """
        :type n: int
        :type paths: List[List[int]]
        :rtype: int
        """

        base = 100003
        mod1 = 10 ** 9 + 7
        mod2 = 2147483647

        l = 0
        r = 100000
        for path in paths:
            r = min(r, len(path))
        
        remove_base1 = [1]
        remove_base2 = [1]
        for _ in range(r + 1):
            remove_base1.append(remove_base1[-1] * base % mod1)
            remove_base2.append(remove_base2[-1] * base % mod2)

        while l < r:
            mid = (l + r + 1) >> 1

            common1 = set()
            common2 = set()
            flag = True
            first_flag = True
            for path in paths:
                now1 = 0
                now2 = 0
                for index in range(mid):
                    now1 = now1 * base + path[index]
                    now1 %= mod1
                    now2 = now2 * base + path[index]
                    now2 %= mod2
                
                h = set([(now1, now2)])
                for index in range(mid, len(path)):
                    now1 = now1 * base + path[index] - (remove_base1[mid] * path[index - mid] % mod1)
                    if now1 < 0:
                        now1 += mod1
                    now1 %= mod1

                    now2 = now2 * base + path[index] - (remove_base2[mid] * path[index - mid] % mod2)
                    if now2 < 0:
                        now2 += mod2
                    now2 %= mod2
                    
                    h.add((now1, now2))

                if first_flag:
                    common = h.copy()
                    first_flag = False
                else:
                    tuple_list = list(common)
                    for t in tuple_list:
                        if t not in h:
                            common.remove(t)

                if not common:
                    flag = False
                    break
            
            if flag:
                l = mid
            else:
                r = mid - 1
        
        return l
```
