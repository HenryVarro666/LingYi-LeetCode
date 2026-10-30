---
title: "3549. 两个多项式相乘"
aliases: ["yiduobo的每日leetcode 3549.两个多项式相乘"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909408038735024521"
zhihu_id: "1909408038735024521"
zhihu_title: "yiduobo的每日leetcode 3549.两个多项式相乘"
question_id: "3549"
question: "两个多项式相乘"
problem_url: "https://leetcode.cn/problems/multiply-two-polynomials/"
difficulty: "Hard"
created: "2025-05-24T02:48:24+08:00"
updated: "2025-05-24T02:48:24+08:00"
upvotes: 1
comments: 0
---

# 3549. 两个多项式相乘

> **[yiduobo的每日leetcode 3549.两个多项式相乘](https://zhuanlan.zhihu.com/p/1909408038735024521) · 知乎 · 2025-05-24 · 赞同 1**
> 力扣：[3549. 两个多项式相乘](https://leetcode.cn/problems/multiply-two-polynomials/) · Hard · 灵茶山艾府：[FFT 模板](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3549.两个多项式相乘

[3549. 两个多项式相乘 - 力扣（LeetCode）](https://leetcode.cn/problems/multiply-two-polynomials/description/)

题目给出两个整数数组ploy1和poly2，其中每个数组中下标index的元素表示多项式中x^index的系数。设A(x)和B(x)分别是poly1和poly2表示的多项式，现在要求返回一个整数数组result，表示乘积多项式R(x) \= A(x) \* B(x)的系数，其中result[index]表示R(x)中x^index的系数。

没想到有一天居然会在leetcode会碰到需要fft的题目，和上次碰到splay的时候一个感想，确实是没题可出了所以下放一点高级货。

言归正传。本题的题目意思很简单，就是给出两个系数数组，表示两个多项式的系数，要求计算这两个多项式相乘后的结果多项式中每一项的系数。对于这个问题，朴素的算法就是逐项相乘计算，时间复杂度为O(n^2)。但是本题中两个多项式的长度都可达10^5，需要进行优化。

题目给出的多项式是由系数表示的，除此之外，还有一种表示方法就是选出若干个点值对来表示。更具体的，对于一个n次多项式f(x) \= a[0] + a[1] \* x + a[2] \* x^2 + ... + a[n] \* x^n，只需选出n + 1个互不相同的x，带入计算得到n个对应的f，就可以用这n + 1个点(x[0], f(x[0])), (x[1], f(x[1])), ..., (x[n], f(x[n]))来表示这个多项式。

如果用矩阵的形式来说明，就是

```python
'''
| 1  x[0]  x[0]^2  ...  x[0]^n |   | A[0] |
| 1  x[1]  x[1]^2  ...  x[1]^n | * | A[1] |  = | f(x[0])  f(x[1])  f(x[2]) ... f(x[n]) |
|     ...     ...  ...     ... |   | ...  |
| 1  x[n]  x[n]^2  ...  x[n]^n |   | A[n] |
'''
```

其中最左边矩阵是x[0]到x[n]这一共n + 1个值以及对应的幂次，中间这个矩阵是原始多项式的系数，矩阵相乘得到的结果就是将x[0]到x[n]分别带入多项式得到的结果矩阵。

左边这个矩阵是一个范德蒙矩阵，其行列式为

(x[1] - x[0]) \* (x[2] - x[0]) \* (x[2] - x[1]) \* ... \* (x[n] - x[0]) \* (x[n] - x[1]) \* (x[n] - x[2]) \* ... \* (x[n] - x[n - 1])

由于x的取值各不相同，因此行列式非0，那么只需在两边都乘以这个矩阵的逆，就可以解出中间的系数矩阵了。

---

接下来对于本题中的ploy1和ploy2，需要将这两个多项式都转化为点值对的形式。在转化之前可以先将这两个多项式的次数补齐，也就是补充一些值为0的系数，使得两个多项式的最高次相同。

令这些点值对为(x[0], p1[0]), (x[1], p1[1])，...，(x[n], p1[n])和(x[0], p2[0]), (x[1], p2[1]), ...，(x[1], p2[n])，那么对于p(x) \= ploy1(x) \* ploy2(x)，如果带入其中某个x[index]，就有

p(x[index]) \= ploy1(x[index]) \* ploy2(x[index]) \= p1[index] \* p2[index]

可以发现，在这个场景下，只需对上面的点值对一趟遍历，就可以计算出将x[0]到x[n]这些点带入到结果多项式p(x)中得到的点值对，即(x[0], p1[0] \* p2[0]), (x[1], p1[1] \* p2[1]), ..., (x[n], p1[n] \* p2[n])。

到了这里，就只需要想办法将这n + 1个点值对还原成系数表示，就得到了本题的结果。

---

到了这里，问题就变成了如何高效地在系数表示和点值表示间进行转换。

直接找n + 1个点暴力计算显然是不行的，这相当于在O(n^2)的时间内计算出了x的矩阵，又花了O(n^2)的时间计算x的矩阵和系数矩阵的乘法，还不如直接用朴素法来的方便。

在这里需要计算的是将

x[0], x[1], ..., x[n]这n + 1个数分别带入多项式A[0] + A[1] \* x + A[2] \* x^2 + ... + A[n] \* x^n的结果

由于x的值是可以选择的，那么就可以考虑选择一些特殊的值来进行计算。对于这个多项式

A[0] + A[1] \* x + A[2] \* x^2 + ... + A[n] \* x^n

将其中的奇数次项和偶数次项都提取出来，就有

(A[0] + A[2] \* x^2 + A[4] \* x^4 + ...) + x \* (A[1] + A[3] \* x^2 + A[5] \* x^4 + ...)

可以发现，左侧括号中和右侧括号中是两个关于x^2的多项式，那么在这里如果选择一组相反数作为某两个x，不妨设为p和n，那么带入的结果就是

(A[0] + A[2] \* p^2 + A[4] \* p^4 + ...) + p \* (A[1] + A[3] \* p^2 + A[5] \* p^4 + ...)

(A[0] + A[2] \* n^2 + A[4] \* n^4 + ...) + n \* (A[1] + A[3] \* n^2 + A[5] \* n^4 + ...)

可以发现，由于p和n互为相反数，那么两个括号中的多项式是分别相等的。在这里不妨记

g(x) \= (A[0] + A[2] \* x + A[4] \* x^2 + ...)

h(x) \= (A[1] + A[3] \* x + A[5] \* x^2 + ...)

那么就有

f(p) \= g(p^2) + p \* h(p^2)

f(n) \= g(n^2) + n \* h(n^2) \= g(p^2) - p \* h(p^2)

也就是说，对于一组p和n，在这里只需要计算p带入到g和h中的结果，就可以同时计算出f(p)和f(n)的结果。

更进一步的，如果选择的x中有四个元素x[0]、x[1]、x[2]、x[3]，满足x[0] \= -x[2], x[1] \= -x[3]，且x[0]^2 \= -x[1]^2，那么将x[0]、x[1]、x[2]、x[3]带入到

f(x) \= A[0] + A[1] \* x + A[2] \* x^2 + ... + A[n] \* x^n

就可以认为是计算将x[0]^2和x[1]^2分别带入到

g(x) \= (A[0] + A[2] \* x + A[4] \* x^2 + ...)和h(x) \= (A[1] + A[3] \* x + A[5] \* x^2 + ...)

而对于将x[0]^2和x[1]^2带入到g(x)，则又可以将g(x)拆分为gg(x) \= (A[0] + A[4] \* x^2 + A[8] \* x^4 + ...)以及x \* gh(x) \= x \* (A[2] + A[6] \* x^2 + A[10] \* x^4)。

由于x[0]^2 \= -x[1]^2，那么又可以如法炮制，将x[0]^4分别带入gg(x)以及gh(x)，就可以计算出x[0]^2和x[1]^2分别带入g的结果。同理，也可以按相同的方法计算出将x[0]^2和x[1]^2分别带入h的结果。

再往回一层，就可以通过g和h的结果计算将x[0]、x[1]、x[2]、x[3]分别带入f的结果了。

为了满足上面这种折半带入的计算，不妨先将多项式的最高次补足到2的幂次减1，也就是将其长度补足到2的幂次m，那么就可以通过不断折半计算，在O(mlogm)的时间内计算出将m个不同的数带入到这个多项式中的结果。

---

接下来的问题就是如何选择这m个数。观察上面的前提条件，像x[0]^2 \= -x[1]^2这种形式显然就已经不是常规选择可以hold住的了，必须有复数参与进来。更具体的，对于m这个规模，可以选择m个单位根，也就是

e^(2πki / m)，其中0 \<\= k \< m

由于e^(πi) \= -1，那么对于一组e^(2πki / m)以及e^(2π(k + m // 2)i / m)，这二者刚好互为相反数，也就是说这m个单位根是由m // 2组相反数组成的。

另一方面，e^(2πki / m)，在平方后的结果是e^(2πki / (m//2))，其与e^(2π(k + (m // 4))i / (m//2))互为相反数，而e^(2π(k + (m // 4))i / (m//2))又刚是e^(2π(k + (m // 4))i / m)的平方，也就是说如果带入这m个单位根进行计算，在执行到只剩计算e^(2π \* 0 \* i / m)，也就是1之前，剩余需要带入计算的单位根的幂次都刚好是若干对相反数。

这样一来，就可以利用递归来进行计算这些多项式的值了。

不妨设目前需要计算的是将n个单位根的幂次数组x，带入到长度为n的多项式p得到的结果数组f：

1、若n \= 1，那么直接将x\[0\] \= 1的结果带入，返回的结果就是f \= \[p\[0\]\]

2、否则将按奇偶划分，得到

even \= \[p\[0\], p\[2\], ..., p\[n - 2\]\]

odd \= \[p\[1\], p\[3\], ..., p\[n - 1\]\]

3、递归计算将x[0]^2、x[1]^2、...、x[n // 2 - 1]^2带入even和odd的结果，分别记为g和h

4、成对遍历g和h，将g[index] + x[index] \* h[index]作为f[index]的结果，将g[index] - x[index] \* h[index]作为f[index + n // 2]的结果

在最外侧调用一次将m个单位根带入到原多项式，得到的结果数组即为所求。

---

到了这一步，已经可以完成多项式到点值对的变换，那么还剩下最后一步，也就是点值对到多项式的转换。这个问题实际上就是对于

```
'''
| 1    ω[0]      ω[0]^2    ...    ω[0]^(m - 1)   |   |   A[0]   |
| 1    ω[1]      ω[1]^2    ...    ω[1]^(m - 1)   | * |   A[1]   |  = | p[0]  p[1] ... p[m - 1] |
| 1    ...           ...     ...        ...         |   |    ...   |
| 1  ω[m - 1]  ω[m - 1]^2  ...  ω[m - 1]^(m - 1) |   | A[m - 1] |
'''
```

需要计算中间矩阵A的值，其中ω[0]到ω[m - 1]分别是m个单位根，矩阵p则是已经计算得到的m个值。

对于这个问题，将两边都乘以左侧矩阵的逆就能得到矩阵A，而对于左侧矩阵的逆，则只需对其中每个元素取共轭，得到的复共轭矩阵与原矩阵相乘是一个对角线上全部都是m的标量矩阵，也就是说只需在右侧矩阵的基础上乘以这个复共轭矩阵，再对其中的元素除以m，就可以得到矩阵A。

而对于单位根e^(2πki / m)，可以写成cos(2πk/m) + isin(2πk/m)，其共轭形式只需将虚数部分的加号改为减号就行了。接下来只需将右侧矩阵视为多项式p，就可以可以直接使用上面的分治法，计算将这些共轭值带入到p中得到的结果，然后再除以m就得到了最终结果A。

最后附上python代码，第一份是递归的写法，但是会超时，还需要做一些常数优化。第二份是非递归的写法，性能比较好：

```
class Solution(object):
    def multiply(self, poly1, poly2):
        """
        :type poly1: List[int]
        :type poly2: List[int]
        :rtype: List[int]
        """
        
        m = 1
        while m < len(poly1) + len(poly2) - 1:
            m += m

        def fft(p, rev=1.0):
            if len(p) == 1:
                return p
            
            odd = []
            even = []
            for index, v in enumerate(p):
                if index % 2 == 0:
                    even.append(p[index])
                else:
                    odd.append(p[index])
            
            x = fft(even, rev)
            y = fft(odd, rev)
            res = [None] * len(p)
            v = complex(1.0)
            for index in range(len(x)):
                res[index] = x[index] + v * y[index]
                res[index + len(x)] = x[index] - v * y[index]
                v = v * complex(cos(2 * pi / len(p)), rev * sin(2 * pi / len(p)))
            
            return res

        p1 = [complex(x) for x in poly1] + [complex(0) for _ in range(m - len(poly1))]
        points1 = fft(p1)
        p2 = [complex(x) for x in poly2] + [complex(0) for _ in range(m - len(poly2))]
        points2 = fft(p2)

        points = []
        for v1, v2 in zip(points1, points2):
            points.append(v1 * v2)

        p = fft(points, -1.0)
        res = []
        for index in range(len(p)):
            res.append(int(round(p[index].real / len(p))))
        
        while len(res) >= len(poly1) + len(poly2):
            res.pop()
        return res
```

```
class Solution(object):
    def multiply(self, poly1, poly2):
        """
        :type poly1: List[int]
        :type poly2: List[int]
        :rtype: List[int]
        """
        
        m = 1
        while m < len(poly1) + len(poly2) - 1:
            m <<= 1

        n = m >> 1
        pos = [0] * m
        rnd = 0
        while n:
            v = 0
            for start in range(0, m, n):
                for index in range(start, start + n):
                    pos[index] |= (v << rnd)
                v ^= 1
            n >>= 1
            rnd += 1

        def fft(p, rev=1):
            p = [p[pos[index]] for index in range(m)]
            n = 2
            while n <= m:
                root_w = complex(cos(2 * pi / n), rev * sin(2 * pi / n))
                for start in range(0, m, n):
                    w = complex(1.0)
                    for index in range(start, start + (n >> 1)):
                        x = p[index]
                        y = w * p[index + (n >> 1)]
                        p[index] = x + y
                        p[index + (n >> 1)] = x - y
                        w *= root_w

                n <<= 1
            
            if rev == -1:
                for index in range(m):
                    p[index] /= m
            
            return p

        p1 = [complex(x) for x in poly1] + [complex(0)] * (m - len(poly1))
        p1 = fft(p1)
        p2 = [complex(x) for x in poly2] + [complex(0)] * (m - len(poly2))
        p2 = fft(p2)
        
        p = [x * y for x, y in zip(p1, p2)]
        p = fft(p, -1)
        
        while len(p) > len(poly1) + len(poly2) - 1:
            p.pop()

        return [int(round(x.real)) for x in p]
```
