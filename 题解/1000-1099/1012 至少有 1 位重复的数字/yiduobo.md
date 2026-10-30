---
title: "1012. 至少有1位重复的数字"
aliases: ["yiduobo的每日leetcode 1012.至少有1位重复的数字"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shi-pin", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367521980"
zhihu_id: "367521980"
zhihu_title: "yiduobo的每日leetcode 1012.至少有1位重复的数字"
question_id: "1012"
question: "至少有 1 位重复的数字"
problem_url: "https://leetcode.cn/problems/numbers-with-repeated-digits/"
difficulty: "Hard"
rating: 2230
created: "2021-04-24T20:02:15+08:00"
updated: "2021-04-24T20:02:15+08:00"
upvotes: 0
comments: 0
---

# 1012. 至少有1位重复的数字

> **[yiduobo的每日leetcode 1012.至少有1位重复的数字](https://zhuanlan.zhihu.com/p/367521980) · 知乎 · 2021-04-24 · 赞同 0**
> 力扣：[1012. 至少有 1 位重复的数字](https://leetcode.cn/problems/numbers-with-repeated-digits/) · Hard · 灵茶山艾府：[数位 DP 通用模板，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1012.至少有1位重复的数字

[力扣](https://leetcode-cn.com/problems/numbers-with-repeated-digits/)

题目要求找出1到N之间至少有1位重复的数字，直接遍历求解的话时间复杂度太高，而找规律的话也比较麻烦，那么不妨逆向思维，先求出1到N中没有重复位的数字，设为res，那么最终答案就是N - res。

对于没有重复数字的问题，我们可以使用简单的组合数学很快求解出来。方便起见，我们先不考虑最高位不能为0的情况。设f[k][l]表示k个不同数字组成长度为l且各个位上不同的整数一共有多少种方法，那么对于第l位，我们一共有k种选择，选择其中任意一种之后问题就转化成了从规模为(k - 1, l - 1)的子问题，即从k - 1个不同数字组成长度为l - 1且各个位上不同的整数的方法，那么就有f[k][l] \= k \* f[k - 1][l - 1]。

边界条件为f[k][0] \= 1。

有了f数组，接下来回到问题本身。设N一共有l位，那么所有长度小于l的数字都是考察的对象。那么对于长度为p的数字，使用10个不同数字来组成就一共有f[10][p]种可能，但是其中还包含着0开头的情况，因此这里还需要减去f[9][p - 1]，即如果最高位定为0，后续有多少种情况。于是长度为p的各个位上不同的数字就一共有f[10][p] - f[9][p - 1]。那么长度小于l，且各个位上不同的数字就一共有

(f[10][1] - f[9][0]) + (f[10][2] - f[9][1]) + ... + (f[10][l - 1] - f[9][l - 2])

例如对于两位数的情况，初始不考虑最高位0时构造的两位数分别为

01、02、...、09

10、12、...、19

...

90、91、...、98

一共为f[10][2] \= 10 \* 9 \= 90种

去除掉最高位为0的情况，那么就是f[9][1] \= 9种

于是最后剩下的合法两位数就是f[10][2] - f[9][1] \= 81种

接下来还需要考察长度为l的数字。此时可以从最高位开始向后遍历，同时使用一个set维护当前已经使用过的数字。

对于当前的N[index]，我们枚举0到N[index] - 1，若当前枚举的数字x未出现在set当中，且此时不是最高位或x不为0，那么就可以将N[index]替换成x之后一定是小于N的。

此时从最高位到第index位之前一共使用了(l - 1 - index)个数字，再去掉index位上当使用的x，那么后面的位上还剩下10 - (l - 1 - index) - 1个数字可用，需要构造长度为index数字，那么这里一共有f[10 - (l - 1 - index) - 1][index]种合法的数字。值得一提的是，这里无需考察最高位为0的情况。

除此之外，若N[index]之前没有被使用过，那么还需要考察N[index]保持不变的情况，此时就需要将N[index]加入set中，并继续考察后续位上的数字，否则就可以直接返回结果了。

例如对于2345中的3而言，我们有必要考察20XX、21XX以及23XX的情况，但是对于3345中的第二个3而言，我们有必要考察30XX、31XX、32XX，但是没有必要继续向后考察33XX了，因为这里的两个3已经产生了重复。

在处理到最后一位时，还需要注意若N[0]没有被使用过，那么N本身也是一个各位上无重复的数字，因此需要将res再加上1。

最后结果就是N - res。

最后附上python代码：

```python
class Solution(object):
    def numDupDigitsAtMostN(self, N):
        """
        :type N: int
        :rtype: int
        """

        f = [[0] * 11 for _ in range(11)]
        for k in range(1, 11):
            f[k][0] = 1
            for l in range(1, k + 1):
                f[k][l] = k * f[k - 1][l - 1]

        a = []
        l = 0
        tmp = N
        while tmp:
            a.append(tmp % 10)
            tmp /= 10
            l += 1
        
        used = set()
        res = 0
        for index in range(l - 1, 0, -1):
            res += f[10][index] - f[9][index - 1]
        for index in range(l - 1, -1, -1):
            for x in range(a[index]):
                if x in used or (index == l - 1 and x == 0):
                    continue
                res += f[10 - (l - 1 - index) - 1][index]

            if a[index] in used:
                break
            used.add(a[index])
            if index == 0:
                res += 1

        return N - res
```
