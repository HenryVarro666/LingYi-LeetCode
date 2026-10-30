---
title: "3138. 同位字符串连接的最小长度"
aliases: ["yiduobo的每日leetcode 3138.同位字符串连接的最小长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702836207"
zhihu_id: "702836207"
zhihu_title: "yiduobo的每日leetcode 3138.同位字符串连接的最小长度"
question_id: "3138"
question: "同位字符串连接的最小长度"
problem_url: "https://leetcode.cn/problems/minimum-length-of-anagram-concatenation/"
difficulty: "Medium"
created: "2024-06-12T00:57:34+08:00"
updated: "2024-06-12T00:57:34+08:00"
upvotes: 1
comments: 0
---

# 3138. 同位字符串连接的最小长度

> **[yiduobo的每日leetcode 3138.同位字符串连接的最小长度](https://zhuanlan.zhihu.com/p/702836207) · 知乎 · 2024-06-12 · 赞同 1**
> 力扣：[3138. 同位字符串连接的最小长度](https://leetcode.cn/problems/minimum-length-of-anagram-concatenation/) · Medium · 灵茶山艾府：[两种方法：枚举因子 / 枚举次数 + GCD 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3138.同位字符串连接的最小长度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-length-of-anagram-concatenation/)

题目给出一个字符串s，其可以由字符串t和t的同位字符串拼接组成，问t的最小长度是多少。同位字符串值的是重新排列一个字符串得到的另一个字符串。

题目中s的长度n比较大，可以达到10^5，但是t的长度必然是s长度的约数，而约数的增长速度其实是非常缓慢的。对于一个正整数n而言，不妨设n \= p[0]^k[0] \* p[1]^k[1] \* ... \* p[m]^k[m]，这里的p都是质数，那么n的约数数目就是(k[0] + 1) \* (k[1] + 1) \* ... \* (k[m] + 1)。

观察这个式子可以发现，如果想让约数的数目增加一倍，那么就需要从n中分离掉一个新的质数，而分离新的质数对n的缩进速度显然是大于两倍的。另一方面，如果从n中分离出之前出现过的质数，不妨设分离出来的质数为p[i]，那么约数的数目将增加p[0]^k[0] \* p[1]^k[1] \* ... \* p[i - 1]^k[i - 1] \* p[i + 1]^k[i + 1] \* ... \* p[m]^k[m]，相比之前增加了1 / k[i]，这个增长速率相比p[i]自身也是很小的，而且会越来越小。

换言之，即使n的规模来到10^5，其中约数数目最多也不会很大。在这里可以先暴力遍历，计算1到10^5中每个数的约数数目，可以发现其中83160 \= 2^3 \* 3^3 \* 5 \* 7 \* 11，一共只有128个约数。

根据上面的结论，就可以从1到n暴力枚举所有的长度length，若length为n的约数，那么就计算s中所有起点为length的倍数，且长度为length的子串中每种字符出现的次数，若次数都相等，那么length即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minAnagramLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        for length in range(1, len(s)):
            if len(s) % length == 0:
                freq = Counter(s[:length])
                flag = True
                for index in range(length, len(s), length):
                    if Counter(s[index : index + length]) != freq:
                        flag = False
                        break
                
                if flag:
                    return length
        
        return len(s)
```
