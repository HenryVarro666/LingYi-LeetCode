---
title: "1018. 可被5整除的二进制前缀"
aliases: ["yiduobo的每日leetcode 1018.可被5整除的二进制前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368360055"
zhihu_id: "368360055"
zhihu_title: "yiduobo的每日leetcode 1018.可被5整除的二进制前缀"
question_id: "1018"
question: "可被 5 整除的二进制前缀"
problem_url: "https://leetcode.cn/problems/binary-prefix-divisible-by-5/"
difficulty: "Easy"
rating: 1376
created: "2021-04-27T21:33:38+08:00"
updated: "2021-04-27T21:33:38+08:00"
upvotes: 0
comments: 0
---

# 1018. 可被5整除的二进制前缀

> **[yiduobo的每日leetcode 1018.可被5整除的二进制前缀](https://zhuanlan.zhihu.com/p/368360055) · 知乎 · 2021-04-27 · 赞同 0**
> 力扣：[1018. 可被 5 整除的二进制前缀](https://leetcode.cn/problems/binary-prefix-divisible-by-5/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1018.可被5整除的二进制前缀

[力扣](https://leetcode-cn.com/problems/binary-prefix-divisible-by-5/)

首先，可以知道N_i \= 2 \* N_i-1 + A[i]，那么若

N_i-1 % k \= 5

那么就有

N_i % k \= (2 \* k + A[i]) % 5

于是我们可以从头到尾遍历A，然后每次使用当前的A[i]以及N_i-1 % k的结果来求出N_i % k，并使用这个余数来更新答案。

最后附上python代码：

```python
class Solution(object):
    def prefixesDivBy5(self, A):
        """
        :type A: List[int]
        :rtype: List[bool]
        """

        res = []
        now = 0

        for num in A:
            now = (now * 2 + num) % 5
            res.append(now == 0)
        
        return res
```
