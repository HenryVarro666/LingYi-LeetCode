---
title: "476. 数字的补数"
aliases: ["yiduobo的每日leetcode 476.数字的补数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/240791959"
zhihu_id: "240791959"
zhihu_title: "yiduobo的每日leetcode 476.数字的补数"
question_id: "476"
question: "数字的补数"
problem_url: "https://leetcode.cn/problems/number-complement/"
difficulty: "Easy"
created: "2020-09-13T22:06:02+08:00"
updated: "2020-09-13T22:06:02+08:00"
upvotes: 0
comments: 0
---

# 476. 数字的补数

> **[yiduobo的每日leetcode 476.数字的补数](https://zhuanlan.zhihu.com/p/240791959) · 知乎 · 2020-09-13 · 赞同 0**
> 力扣：[476. 数字的补数](https://leetcode.cn/problems/number-complement/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

476.数字的补数<https://leetcode-cn.com/problems/number-complement/>

比较基础的题目。题目描述的补数为num的二进制取反，那么将num转化为二进制之后逐位取反，然后再转换回十进制即可。

我在这里用了一种比较取巧的做法。由于补数是num二进制下逐位取反得到的，那么补数加上num必然是1111..111这种形式，而这里的1111..111 \= 2^k - 1，这里的k则可以通过num的长度获取到。这个做法在python里面可行，但是在c里面可能会出现越界的情况。

最后附上python代码：

```python
class Solution(object):
    def findComplement(self, num):
        """
        :type num: int
        :rtype: int
        """

        pow2 = 1
        while pow2 <= num:
            pow2 <<= 1
        
        return pow2 - 1 - num
```
