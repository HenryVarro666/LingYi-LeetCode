---
title: "3556. 最大质数子字符串之和"
aliases: ["yiduobo的每日leetcode 3556.最大质数子字符串之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/ordered-set", "leetcode/sorting", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909803259239076028"
zhihu_id: "1909803259239076028"
zhihu_title: "yiduobo的每日leetcode 3556.最大质数子字符串之和"
question_id: "3556"
question: "最大质数子字符串之和"
problem_url: "https://leetcode.cn/problems/sum-of-largest-prime-substrings/"
difficulty: "Medium"
rating: 1440
created: "2025-05-26T22:10:37+08:00"
updated: "2025-05-26T22:10:37+08:00"
upvotes: 0
comments: 0
---

# 3556. 最大质数子字符串之和

> **[yiduobo的每日leetcode 3556.最大质数子字符串之和](https://zhuanlan.zhihu.com/p/1909803259239076028) · 知乎 · 2025-05-26 · 赞同 0**
> 力扣：[3556. 最大质数子字符串之和](https://leetcode.cn/problems/sum-of-largest-prime-substrings/) · Medium · 灵茶山艾府：[判断质数 + 预处理质数加速判断（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3556.最大质数子字符串之和

[3556. 最大质数子字符串之和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-largest-prime-substrings/description/)

题目给出一个字符串s，s的长度不超过10。要求找出由其子字符串构成的3个最大的不同质数之和。若不同的质数不足3个，则返回所有不同质数之和。

对于长度n的字符串，其一共有n \* (n - 1) / 2个子字符串。本题中s的长度不超过10，那么就可以直接暴力枚举s的所有子串，然后检测这些子串对应的数是否为质数即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfLargestPrimes(self, s):
        """
        :type s: str
        :rtype: int
        """
        

        primes = [0] * 3
        for length in range(1, len(s) + 1):
            for start in range(len(s) - length + 1):
                v = int(s[start :start + length])
                if v == 0 or v == 1:
                    continue

                flag = True
                x = 2
                while x * x <= v:
                    if v % x == 0:
                        flag = False
                        break
                    x += 1
                
                if flag:
                    if v > primes[0]:
                        primes[0], primes[1], primes[2] = v, primes[0], primes[1]
                    elif v != primes[0] and v > primes[1]:
                        primes[1], primes[2] = v, primes[1]
                    elif v != primes[0] and v != primes[1] and v > primes[2]:
                        primes[2] = v
        
        return sum(primes)
```
