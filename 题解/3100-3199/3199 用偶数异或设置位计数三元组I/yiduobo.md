---
title: "3199. 用偶数异或设置位计数三元组I"
aliases: ["yiduobo的每日leetcode 3199.用偶数异或设置位计数三元组I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707323153"
zhihu_id: "707323153"
zhihu_title: "yiduobo的每日leetcode 3199.用偶数异或设置位计数三元组I"
question_id: "3199"
question: "用偶数异或设置位计数三元组I"
problem_url: "https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-i/"
created: "2024-07-06T02:44:09+08:00"
updated: "2024-07-06T02:44:09+08:00"
upvotes: 0
comments: 0
---

# 3199. 用偶数异或设置位计数三元组I

> **[yiduobo的每日leetcode 3199.用偶数异或设置位计数三元组I](https://zhuanlan.zhihu.com/p/707323153) · 知乎 · 2024-07-06 · 赞同 0**
> 力扣：[3199. 用偶数异或设置位计数三元组I](https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3199.用偶数异或设置位计数三元组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-i/description/)

题目给出三个整数数组a、b、c，要求找出其中满足a[i]、b[j]、c[k]三者异或结果的二进制表示中1的数量为偶数的三元组(i, j, k)的数量。

题目个数据规模很小，直接暴力枚举所有的三元组(i, j, k)，计算异或结果然后统计其二进制表示中1的数量是完全可行的。

我在这里使用是利用异或的性质来计算。对于两个整数x和y而言，不妨设x的二进制表示中1的数量为s[x]，y的二进制表示中1的数量为s[y]，那么x^y的二进制表示中1的数量就是s[x] + s[y] - t[(x, y)] \* 2，这里的t[(x, y)]表示x和y的二进制表示中值都为1的二进制位的数量，这些位在异或运算中将出现1^1 \= 0的情况，也就是这一位上的两个1最终将变为0。

可以发现，s[x] + s[y] - t[(x, y)] \* 2与s[x] + s[y]是同奇偶的，也就是说，x^y的二进制表示中如果有偶数个1，那么s[x] + s[y]也必须为偶数，即s[x]和s[y]同奇偶。

更进一步的，对于三元组a[i]、b[j]、c[k]，三者异或的结果可以认为是a[i]与b[j]异或的结果再与c[k]进行异或操作，为了使得最终异或结果的二进制表示中有偶数个1，那么a[i]^b[j]与c[k]的二进制表示中1的数量必须同奇偶。

接下来分情况讨论：

1、若c[k]的二进制表示中有奇数个1：

此时a[i]^b[j]的结果的二进制表示中也必须有奇数个1，对应到a[i]、b[j]这二者的二进制表示中1的数量必须是一奇一偶，即a[i]的二进制表示中有奇数个1且b[j]的二进制表示中有偶数个1，或者a[i]的二进制表示中有偶数个1且b[j]的二进制表示中有奇数个1

2、若c[k]的二进制表示中偶偶数个1：

此时a[i]^b[j]的结果的二进制表示中也必须有偶数个1，对应到a[i]、b[j]这二者的二进制表示中1的数量必须是同奇偶的，即a[i]和b[j]的二进制表示中都有奇数个1，或者都有偶数个1

综合起来，就有以下几种可行的组合

a[i]奇数、b[j]奇数、c[k]偶数

a[i]奇数、b[j]偶数、c[k]奇数

a[i]偶数、b[j]奇数、c[k]奇数

a[i]偶数、b[j]偶数、c[k]偶数

于是只需分别遍历三个数组，计算每个数组中二进制位上1的数量为奇数以及偶数的数有多少个，不妨记为(odd_a，even_a)、(odd_b，even_b)、(odd_c，even_c)，那么最终可行的组合数量就是下面四个式子之和

odd_a \* odd_b \* even_c

odd_a \* even_b \* odd_c

even_a \* odd_b \* odd_c

even_a \* even_b \* even_c

最后附上python代码：

```python
class Solution(object):
    def tripletCount(self, a, b, c):
        """
        :type a: List[int]
        :type b: List[int]
        :type c: List[int]
        :rtype: int
        """

        def cnt(arr):
            odd = even = 0
            for v in arr:
                one = 0
                while v:
                    if v & 1:
                        one += 1
                    v >>= 1
            
                if one & 1:
                    odd += 1
                else:
                    even += 1
            
            return odd, even

        odd_a, even_a = cnt(a)
        odd_b, even_b = cnt(b)
        odd_c, even_c = cnt(c)

        return odd_a * odd_b * even_c + odd_a * even_b * odd_c + even_a * odd_b * odd_c + even_a * even_b * even_c
```
