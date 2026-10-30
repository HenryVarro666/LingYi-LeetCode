---
title: "1680. 连接连续二进制数字"
aliases: ["yiduobo的每日leetcode 1680.连接连续二进制数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/数学算法", "题单/位运算/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444958286"
zhihu_id: "444958286"
zhihu_title: "yiduobo的每日leetcode 1680.连接连续二进制数字"
question_id: "1680"
question: "连接连续二进制数字"
problem_url: "https://leetcode.cn/problems/concatenation-of-consecutive-binary-numbers/"
difficulty: "Medium"
rating: 1630
created: "2021-12-14T00:04:15+08:00"
updated: "2021-12-14T00:04:15+08:00"
upvotes: 0
comments: 0
---

# 1680. 连接连续二进制数字

> **[yiduobo的每日leetcode 1680.连接连续二进制数字](https://zhuanlan.zhihu.com/p/444958286) · 知乎 · 2021-12-14 · 赞同 0**
> 力扣：[1680. 连接连续二进制数字](https://leetcode.cn/problems/concatenation-of-consecutive-binary-numbers/) · Medium · 灵茶山艾府：[两种方法：从 O(n) 暴力到 O(log^2 n) 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1680.连接连续二进制数字

[力扣](https://leetcode-cn.com/problems/concatenation-of-consecutive-binary-numbers/)

不妨设s[i]表示1到i的二进制拼接后的十进制的值，那么对于s[i]，可以认为是在s[i - 1]的二进制后面拼接上了i的二进制表示。不妨设i的二进制表示有l[i]位，那么将i拼接在s[i - 1]后面就相当于将s[i - 1]左移了2^l[i]位，然后再加上i本身，于是就有s[i] \= s[i - 1] \* 2^l[i] + i。

初始化s[1] \= 1，然后从2开始到n一趟扫描，求出对应的s即可。

注意到l[i]只与i本身有关，因此可以先预处理出所有的l[i]。实际上，l[i]的分布也存在规律。1位的二进制数只有1，2位的二进制数有2、3一共两个，3位的二进制数有4、5、6、7一共四个。更一般的，k为的二进制数有2^(k - 1)个，根据这个规律可以很快扩展出整个l数组。

另外，这里的s[i]只与s[i - 1]有关，因此完全不需要s数组，只需要维护当前的s就好了。

本题应该也存在数学方法。简单想了一下，如果按数字的位数分组的话，k为二进制数为答案提供的数值和就是

2^(k - 1) \* 2^p + (2^(k - 1) + 1) \* 2^(p - k) + ... + (2^(k - 1) + 2^(k - 1) - 1) \* 2^(p - k \* (k - 1))

首先可以将2^(k - 1)项都提出来，可以的得到一个等比数列

2^(k - 1) \* 2^p + 2^(k - 1) \* 2^(p - k) + ... + 2^(k - 1) \* 2^(p - k \* (k - 1))

提出来之后还剩下

2^(p - k) + 2 \* 2^(p - k \* 2) + 3 \* 2^(p - k \* 3) + ... + (2^(k - 1) - 1) \* 2^(p - k \* (k - 1))

这个式子可以拆开成为

(2^(p - k) + 2^(p - k \* 2) + 2^(p - k \* 3) + ... + 2^(p - k \* (k - 1))) +

(2^(p - k \* 2) + 2^(p - k \* 3) + ... + 2^(p - k \* (k - 1))) +

... +

2^(p - k \* (k - 1))

一共是k - 1个等比数列

注意到这些式子的公比都是2^k，包括最开始提出来的2^(k - 1)的等比数列，因此最终答案一定可以合并成一个幂次相关的求解式子。对于幂次的求解，很自然想到使用快速幂来优化。除此之外，一开始就可以计算出整个式子的长度，也就是说上面式子的p和k是存在某种关系的。那么到了这里，1到n一共分成log(n)组，求解每一组的时间复杂度也是O(logn)，因此最终时间复杂度应该是O(log(n)log(n))。

不过我推导到上面这一步就没有继续往后推导了，因为实在是很麻烦。。所以也就无从谈起具体实现了。

最后附上python代码，我在这里采用的最上面的朴素递推算法：

```python
class Solution(object):
    def concatenatedBinary(self, n):
        """
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        l = [2]
        now = 2
        while now * 2 - 1 <= n:
            l.extend([now + now] * now)
            now += now
        
        l.extend([now + now] * (n - now + 1))
        
        res = 0
        for num in range(n):
            res = (res * l[num] + num + 1) % mod
        
        return res
```
