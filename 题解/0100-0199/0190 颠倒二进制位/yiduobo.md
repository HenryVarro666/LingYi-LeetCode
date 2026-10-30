---
title: "190. 颠倒二进制位"
aliases: ["yiduobo的每日leetcode 190.颠倒二进制位"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/divide-and-conquer", "题单/位运算", "题单/面试经典-150-题", "题单/位运算/一-基础题", "题单/面试经典-150-题/位运算"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145681912"
zhihu_id: "145681912"
zhihu_title: "yiduobo的每日leetcode 190.颠倒二进制位"
question_id: "190"
question: "颠倒二进制位"
problem_url: "https://leetcode.cn/problems/reverse-bits/"
difficulty: "Easy"
created: "2020-06-03T21:52:16+08:00"
updated: "2020-06-03T21:52:16+08:00"
upvotes: 0
comments: 0
---

# 190. 颠倒二进制位

> **[yiduobo的每日leetcode 190.颠倒二进制位](https://zhuanlan.zhihu.com/p/145681912) · 知乎 · 2020-06-03 · 赞同 0**
> 力扣：[190. 颠倒二进制位](https://leetcode.cn/problems/reverse-bits/) · Easy · 灵茶山艾府：[O(1) 位运算分治，原理讲解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

190.颠倒二进制位<https://leetcode-cn.com/problems/reverse-bits/>

考察位运算的基础。

n&1表示取n二进制下的最后一位，而n >> 1表示n右移一位，那么可以通过这两种运算的配合从后往前依次取出n的每一位，然后对于最后一位，需要将其左移31位，对于倒数第二位，则是左移30位，以此类推。最后将每一位左移后的结果加起来即为最后的答案。

最后附上python代码：

```python
class Solution:
    # @param n, an integer
    # @return an integer
    def reverseBits(self, n):
        res = 0
        k = 31

        while n:
            res += (n & 1) << k
            n >>= 1
            k -= 1
        
        return res
```
