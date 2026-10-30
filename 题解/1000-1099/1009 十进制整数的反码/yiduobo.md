---
title: "1009. 十进制整数的反码"
aliases: ["yiduobo的每日leetcode 1009.十进制整数的反码"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367063026"
zhihu_id: "367063026"
zhihu_title: "yiduobo的每日leetcode 1009.十进制整数的反码"
question_id: "1009"
question: "十进制整数的反码"
problem_url: "https://leetcode.cn/problems/complement-of-base-10-integer/"
difficulty: "Easy"
created: "2021-04-22T22:29:45+08:00"
updated: "2021-04-22T22:29:45+08:00"
upvotes: 0
comments: 0
---

# 1009. 十进制整数的反码

> **[yiduobo的每日leetcode 1009.十进制整数的反码](https://zhuanlan.zhihu.com/p/367063026) · 知乎 · 2021-04-22 · 赞同 0**
> 力扣：[1009. 十进制整数的反码](https://leetcode.cn/problems/complement-of-base-10-integer/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1009.十进制整数的反码

[力扣](https://leetcode-cn.com/problems/complement-of-base-10-integer/)

设N的二进制表示有K位，那么答案应该是11...1 - N(2)，其中一共有K个1，而11...1又等于100...0 - 1，这里有K个0。

于是我们可以先求出这个2的幂次pow2 \= 100...0，然后使用pow2 - 1 - N就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def bitwiseComplement(self, N):
        """
        :type N: int
        :rtype: int
        """

        pow2 = 2
        while pow2 <= N:
            pow2 <<= 1
        
        return pow2 - N - 1
```
