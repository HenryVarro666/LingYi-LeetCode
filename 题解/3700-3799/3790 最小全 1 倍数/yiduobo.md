---
title: "3790. 最小全1的倍数"
aliases: ["yiduobo的每日leetcode 3790.最小全1的倍数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/一-链表", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1988664004302893191"
zhihu_id: "1988664004302893191"
zhihu_title: "yiduobo的每日leetcode 3790.最小全1的倍数"
question_id: "3790"
question: "最小全 1 倍数"
problem_url: "https://leetcode.cn/problems/smallest-all-ones-multiple/"
difficulty: "Medium"
rating: 1015
created: "2025-12-29T22:32:12+08:00"
updated: "2025-12-29T22:32:13+08:00"
upvotes: 1
comments: 0
---

# 3790. 最小全1的倍数

> **[yiduobo的每日leetcode 3790.最小全1的倍数](https://zhuanlan.zhihu.com/p/1988664004302893191) · 知乎 · 2025-12-29 · 赞同 1**
> 力扣：[3790. 最小全 1 倍数](https://leetcode.cn/problems/smallest-all-ones-multiple/) · Medium · 灵茶山艾府：[原题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3790.最小全1的倍数

[3790. 最小全 1 倍数 - 力扣（LeetCode）](https://leetcode.cn/problems/smallest-all-ones-multiple/description/)

题目给出一个正整数k，要求找出最小的，由全1构成的整数n，且n可以被k整除。

k的取值范围在2到10^5之间。

要求返回n的位数，若不存在这样的n，则返回-1。

没有什么特别好的思路，那么不妨直接暴力计算。由于k的大小不超过10^5，因此余数最多只有10^5种可能性。接下来需要考虑的是，若出现相同的余数应该怎么办。

设两个由全1组成的数n1以及n2，二者的数位分别为m1以及m2，且m1 > m2，这两个数模k都余r，即

111...11 ≡ r (mod k)，一共是m1个1

111...11 ≡ r (mod k)，一共是m2个1

那么就有(n1 - n2) ≡ 0 (mod k)，也就是

111...11000...00 ≡ 0 (mod k)

即m1 - m2个1后面接了m2个0

更进一步的，就有

111...11 \* (2^m2) \* (5^m2) ≡ 0 (mod k)

也就是说，若k既不是2的倍数，也不是5的倍数，那么就可以得到

111...11 ≡ 0 (mod k)

一共是m1 - m2个1。也就是说，在计算到n1之前，就一定会碰到一个长度为m1 - m2个全1整数，其可以被k整除。

这也就意味着若k不是2或者5的倍数，就可以直接暴力计算，在余数出现重复时必然先找出合法的答案，即暴力计算的次数不超过k次。

此时还有一个问题就是若k是2或者5的倍数应该如何处理，答案也很简单，就是无解。

因为2的所有倍数必然是偶数，而5的倍数要么以5结尾，要么以0结尾，而全1整数显然都不满足，因此若k是2或者5的倍数时，可以直接返回-1。

最后附上python代码：

```python
class Solution(object):
    def minAllOneMultiple(self, k):
        """
        :type k: int
        :rtype: int
        """
        
        if k % 2 == 0 or k % 5 == 0:
            return -1
        
        r = 1
        s = 1
        res = 1
        while s != 0:
            r = r * 10 % k
            s = (s + r) % k
            res += 1
        
        return res
```
