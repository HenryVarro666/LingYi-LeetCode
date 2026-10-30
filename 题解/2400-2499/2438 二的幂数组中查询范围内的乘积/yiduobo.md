---
title: "2438. 二的幂数组中查询范围内的乘积"
aliases: ["yiduobo的每日leetcode 2438.二的幂数组中查询范围内的乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "leetcode/prefix-sum", "leetcode/bao-li", "题单/位运算", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583792876"
zhihu_id: "583792876"
zhihu_title: "yiduobo的每日leetcode 2438.二的幂数组中查询范围内的乘积"
question_id: "2438"
question: "二的幂数组中查询范围内的乘积"
problem_url: "https://leetcode.cn/problems/range-product-queries-of-powers/"
difficulty: "Medium"
rating: 1610
created: "2022-11-16T01:20:51+08:00"
updated: "2022-11-16T01:20:51+08:00"
upvotes: 0
comments: 0
---

# 2438. 二的幂数组中查询范围内的乘积

> **[yiduobo的每日leetcode 2438.二的幂数组中查询范围内的乘积](https://zhuanlan.zhihu.com/p/583792876) · 知乎 · 2022-11-16 · 赞同 0**
> 力扣：[2438. 二的幂数组中查询范围内的乘积](https://leetcode.cn/problems/range-product-queries-of-powers/) · Medium · 灵茶山艾府：[三种方法：暴力 / 预处理 / 前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2438.二的幂数组中查询范围内的乘积

[力扣](https://leetcode.cn/problems/range-product-queries-of-powers/)

题目的要求分两步。

首先是将n拆成2的幂次组成的数组power，要求power的长度尽量短。这个长度尽量短就意味着数组中不能出现相同的数，否则这两个数之和就可以用更进一位的2的幂次来代替。有了这个前提，就只需将n的二进制表示中所有为1的位给剥离出来就行了。

得到power之和，将有一连串的query，要求计算power中某个区间的乘积。对于区间乘积的计算，一个自然的想法就是将其转化为前缀乘积之间的除法。不过在这里需要对结果进行取模，那么一旦涉及到除法操作就免不了要计算乘法逆元，那么在这里不妨利用2的幂次这一性质，将乘法操作利用对数转化为加法操作。这样一来，区间乘积就转化为了区间和运算，再将其转化为前缀和就能很方便的计算了。

当然，在转化为区间和运算之后，对于最后的和还需要计算其2的幂次。注意到这里n不超过10的9次方，那么其二进制表示上的最大值就是2^29，因此在这里区间和最大也就是(1 + 29) \* 29 / 2，很明显是不超过500的一个值，那么完全可以先将2的幂次都算出来，就可以利用前缀和以及这个幂次表在O(1)的时间内处理单个询问了。

最后附上python代码：

```python
class Solution(object):
    def productQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        power = []
        now = 0
        while n:
            if n & (1 << now):
                n ^= (1 << now)
                power.append(now)
            now += 1

        s = [power[0]]
        for p in power[1:]:
            s.append(s[-1] + p)
        
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(500):
            pow2.append(pow2[-1] + pow2[-1])
            if pow2[-1] >= mod:
                pow2[-1] -= mod

        res = []
        for x, y in queries:
            p = s[y]
            if x > 0:
                p -= s[x - 1]
            res.append(pow2[p])
            
        
        return res
```
