---
title: "3145. 大数组元素的乘积"
aliases: ["yiduobo的每日leetcode 3145.大数组元素的乘积"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703494443"
zhihu_id: "703494443"
zhihu_title: "yiduobo的每日leetcode 3145.大数组元素的乘积"
question_id: "3145"
question: "大数组元素的乘积"
problem_url: "https://leetcode.cn/problems/find-products-of-elements-of-big-array/"
difficulty: "Hard"
rating: 2859
created: "2024-06-15T03:00:41+08:00"
updated: "2024-06-15T03:00:41+08:00"
upvotes: 0
comments: 0
---

# 3145. 大数组元素的乘积

> **[yiduobo的每日leetcode 3145.大数组元素的乘积](https://zhuanlan.zhihu.com/p/703494443) · 知乎 · 2024-06-15 · 赞同 0**
> 力扣：[3145. 大数组元素的乘积](https://leetcode.cn/problems/find-products-of-elements-of-big-array/) · Hard · 灵茶山艾府：[O(log) 试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3145.大数组元素的乘积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-products-of-elements-of-big-array/)

题目定义一个整数的强数组为满足和为x的二的幂的最短有序数组。例如11的强数组为[1, 2, 8]。换言之，一个整数的强数组就是其二进制表示下，从低位到高位值为1的位对应的2的幂次。

将正整数的强数组连接起来，得到数组big_nums，big_nums的开头部分为[1, 2, 1, 2, 4, 1, 4, 2, 4, 1, 2, 4, 8, ...]。其中1到8的强数组分别为[1]，[2]，[1, 2]，[4]，[1, 4]，[2, 4]，[1, 2, 4]，[8]，拼接得到省略号前面的部分。

最后给出一个二维数组queries，其中queris\[i\] \= \[from\[i\], to\[i\], mod\[i\]\]，要求计算(big_nums\[from\[i\]\] \* big_nums\[from\[i\] + 1\] \* ... \* big_nums\[to\[i\]\]) % mod\[i\]。

其中from[i]和to[i]的取值范围可以到10^15。

由于from[i]和to[i]的取值范围非常大，暴力求解显然是不行的，需要想办法找规律。

首先，对于题目中要计算的big_nums\[from\[i\]\] \* big_nums\[from\[i\] + 1\] \* ... \* big_nums\[to\[i\]\]这个式子，这是一个连乘的式子，但是其中的项都是2的幂次，那么如果对big_nums中的项都对2取对数，那么题目这个连成的式子就可以写成2^(arr\[from\[i\]\] + arr\[from\[i\] + 1\] + ... + arr\[to\[i\]\])，其中arr\[i\] \= log2(big_nums\[i\])。对于2的幂次这个问题，可以使用快速幂来处理，这样一来，问题就转化成了arr数组的区间和问题，而对于区间和问题，则可以转化为前缀和求解，于是实际上问题就变成了给出一个整数v，问arr数组到v的前缀和是多少。

接下来观察arr数组的构成，注意arr为big_nums的log2形式。

arr数组的前若干项为

0, 1, 0, 1, 2, 0, 2, 1, 2, 0, 1, 2, 3, 0, 3, 1, 3, 0, 1, 3, 2, 3, 0, 2, 3, 1, 2, 3, 0, 1, 2, 3, 4, ...

这样看很难发现规律，不妨按整数第一次出现的位置分节，那么就可以得到

| 0 |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |
| 0 | 1 |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 0 | 2 |  |  |  |  |  |  |
| 1 |  | 2 |  |  |  |  |  |
| 0 | 1 |  | 2 |  |  |  |  |
|  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 0 | 3 |  |  |  |  |  |  |
| 1 |  | 3 |  |  |  |  |  |
| 0 | 1 |  | 3 |  |  |  |  |
| 2 |  |  |  | 3 |  |  |  |
| 0 | 2 |  |  |  | 3 |  |  |
| 1 |  | 2 |  |  |  | 3 |  |
| 0 | 1 |  | 2 |  |  |  | 3 |

可以发现，当1首次出现时，可以写成一个斜盖，盖住之前出现的1；当2首次出现时，可以写成一个斜盖盖住上面出现过的0和1；当3首次出现时，可以写成一个斜盖，盖住之前出现过的0、1、2；以此类推。

其中数值index对应的斜盖长度恰好为2^index，那么这样一来就很容易写出每个三角形内数的数目以及数值之和。由于题目要计算的是前缀和，那么在这里将其写成前缀的形式。

令f[index]表示以index首次出现的斜盖为结尾的前缀数值之和，g[index]表示以index首次出现的斜盖为结尾的前缀数目之和，那么对于f[index]和g[index]，就有

f[index] \= f[index - 1] \* 2 + index \* 2^index

g[index] \= g[index - 1] \* 2 + 2^index

得到f和g数组之后，接下来就需要想办法通过f和g计算arr的前缀和。

对于某个位置v，需要通过g来确定v位于哪个斜盖之下，即通过v与g[index - 1]的大小关系判断v是否位于index所在的斜盖之下。当v小于等于g[index - 1]时，其位于上半部分，即不处于index的斜盖下，否则就需要将v减去g[index - 1]，并将前缀和res加上上半部分的数值之和f[index - 1]，表示v位于index的斜盖下。

但是需要特别注意的是，仅通过g[index - 1]来判断并累加f[index - 1]是不够的，例如上面表格中最后一行的2，第一轮可以判断其位于3所在的斜盖之下，但是在第二轮计算时，此时需要判断的是v是否位于2的斜盖之下，此时应该对比的就是v与下表中的前四行的数的数目。可以发现，此时除了g[1]之外，外面还附带着3的斜盖，一共是4个3。换言之，在之前的轮次对v进行定位时，每次处于下半区都将额外添加进来一个斜盖，那么对于后续的定位，需要计算斜盖中数的数目，以及数值之和。

那么在这里就需要使用一个数组pos储存当前的v处于那些数的斜盖之下，此时与v对比的就应该是g[index - 1] + len(pos) \* 2^index，后面这一项就是外部斜盖带来的数的数目，一共是2^index行，每一行都有len(pos)项。同样的，此时上部的和就是f[index - 1] + sum(pos) \* 2^index。另外，由于sum计算是O(n)的，所以在这里需要使用另一个变量s来维护pos数组的数值之和。

| 3 |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 |  |  |  |  |  |  |
| 1 |  | 3 |  |  |  |  |  |
| 0 | 1 |  | 3 |  |  |  |  |
| 2 |  |  |  | 3 |  |  |  |
| 0 | 2 |  |  |  | 3 |  |  |
| 1 |  | 2 |  |  |  | 3 |  |
| 0 | 1 |  | 2 |  |  |  | 3 |

另外需要注意的是，由于外部斜盖的存在，那么对v的定位进行到最后，其可能恰好落在斜盖上。

例如定位到上表中倒数第三行的0，此时v的取值范围可以在1到5之间，分别对应的是2、3、0、2、3。可以发现，若此时的v大于pos的长度，那么其位于0所在的这一行，也就是倒数第三行，否则其应该位于倒数第四行。因此当v > len(pos)时，需要再累加一次pos之和，也就是将s累加到答案中，然后将v减去len(pos) + 1，表示跳过了上一行以及当前行的0。最后，若v > 0，其对应的就应该是外部斜盖的第v项，那么还需要将斜盖的前v项之和，也就是pos数组的后v项之和累加到res中。

到了这里，就得到了一种算法。

令f[0] \= 0，g[0] \= 1，接下来按照

f[index] \= f[index - 1] \* 2 + index \* 2^index

g[index] \= g[index - 1] \* 2 + 2^index

计算f和g。计算到g[45]就足够了，因为g[45]已经大于10^15。

接下来从45开始到1向下遍历，对于当前遍历到的index，此时上半部分中数的数目就是

low_cnt \= g[index - 1] + len(pos) \* 2^index

而上半部分的数值之和则为

low_s \= f[index - 1] + s \* 2^index

若此时的v > low_cnt，那么说明v位于index的斜盖之下，此时就应该将low_s累加到答案中，然后将v减去low_cnt，同时将index添加到pos数组末尾并将index累加到s中。

重复上面的过程直到遍历完成，然后判断此时剩下的v是否大于len(pos)，若大于，那么就将s再次累加到答案中，并将v减去len(pos) + 1。最后，若v > 0，还需要将pos的最后v项累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def findProductsOfElements(self, queries):
        """
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        f = [0]
        g = [1]
        for index in range(1, 46):
            f.append(f[-1] * 2 + (index << index))
            g.append(g[-1] * 2 + (1 << index))
        
        def calc(v):
            pos = []
            s = 0
            res = 0
            for index in range(45, 0, -1):
                low_cnt = (len(pos) << index) + g[index - 1]
                low_s = (s << index) + f[index - 1]
                if low_cnt < v:
                    res += low_s
                    v -= low_cnt
                    pos.append(index)
                    s += index

            if v > len(pos):
                res += s
                v -= len(pos) + 1
            if v > 0:
                res += sum(pos[-v:])

            return res

        def quick_pow(p, mod):
            if p == 0:
                return 1 % mod
            if p == 1:
                return 2 % mod
            
            x = quick_pow(p // 2, mod)
            x = x * x % mod
            if p & 1:
                x = x * 2 % mod
            return x

        return [quick_pow(calc(y + 1) - calc(x), mod) for x, y, mod in queries]
```
