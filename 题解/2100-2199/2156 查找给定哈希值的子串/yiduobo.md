---
title: "2156. 查找给定哈希值的子串"
aliases: ["yiduobo的每日leetcode 2156.查找给定哈希值的子串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sliding-window", "leetcode/rolling-hash", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/531523744"
zhihu_id: "531523744"
zhihu_title: "yiduobo的每日leetcode 2156.查找给定哈希值的子串"
question_id: "2156"
question: "查找给定哈希值的子串"
problem_url: "https://leetcode.cn/problems/find-substring-with-given-hash-value/"
difficulty: "Hard"
rating: 2063
created: "2022-06-20T23:57:22+08:00"
updated: "2022-06-20T23:57:22+08:00"
upvotes: 0
comments: 0
---

# 2156. 查找给定哈希值的子串

> **[yiduobo的每日leetcode 2156.查找给定哈希值的子串](https://zhuanlan.zhihu.com/p/531523744) · 知乎 · 2022-06-20 · 赞同 0**
> 力扣：[2156. 查找给定哈希值的子串](https://leetcode.cn/problems/find-substring-with-given-hash-value/) · Hard · 灵茶山艾府：[倒序滑动窗口 + O(1) 额外空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2156.查找给定哈希值的子串

[力扣](https://leetcode.cn/problems/find-substring-with-given-hash-value/)

题目描述的是经典的字符串哈希算法rk算法的反向计算版。

对于字符串中i到i + k - 1这一段，其哈希值为

h1 \= (val(s[i]) \* p^0 + val(s[i + 1]) \* p + ... + val(s[i + k - 1] \* p^(k - 1)) % m

而对于i + 1到i + k这一段，其哈希值则为

h2 \= (val(s[i + 1]) \* p^0 + val(s[i + 2]) \* p + ... + val(s[i + k - 1] \* p^(k - 2) + val(s[i + k]) \* p^(k - 1)) % m

可以发现，将h2乘以p，去除掉最后一项val(s[i + k]) \* p^k，然后再额外添加一项val(s[i])，就得到了h1，即

h1 \= (h2 \* p - val(s[i + k]) \* p^k + val(s[i])) % m

根据这个式子，就可以从后往前一趟遍历，在O(n)的时间内计算出s中每个长度为k的子串对应的哈希值。取其中位置最靠前且哈希值等于目标值的子串作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def subStrHash(self, s, power, modulo, k, hashValue):
        """
        :type s: str
        :type power: int
        :type modulo: int
        :type k: int
        :type hashValue: int
        :rtype: str
        """

        n = len(s)
        p = n - k
        now = 0
        pow_k = 1

        for index in range(n - 1, p - 1, -1):
            now = (now * power + ord(s[index]) - 96) % modulo
            pow_k = pow_k * power % modulo

        res = n - 1
        if now == hashValue:
            res = p
        
        for index in range(p - 1, -1, -1):
            now = (now * power - (ord(s[index + k]) - 96) * pow_k % modulo + modulo + ord(s[index]) - 96) % modulo
            if now == hashValue:
                res = index
        
        return s[res : res + k]
```
