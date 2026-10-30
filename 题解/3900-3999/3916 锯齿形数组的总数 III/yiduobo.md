---
title: "3916. Number of ZigZag Array III"
aliases: ["yiduobo的每日leetcode 3916.Number of ZigZag Array III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/动态规划", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2034745412062552291"
zhihu_id: "2034745412062552291"
zhihu_title: "yiduobo的每日leetcode 3916.Number of ZigZag Array III"
question_id: "3916"
question: "锯齿形数组的总数 III"
problem_url: "https://leetcode.cn/problems/number-of-zigzag-arrays-iii/"
difficulty: "Hard"
created: "2026-05-04T22:07:28+08:00"
updated: "2026-05-04T22:07:28+08:00"
upvotes: 1
comments: 0
---

# 3916. Number of ZigZag Array III

> **[yiduobo的每日leetcode 3916.Number of ZigZag Array III](https://zhuanlan.zhihu.com/p/2034745412062552291) · 知乎 · 2026-05-04 · 赞同 1**
> 力扣：[3916. 锯齿形数组的总数 III](https://leetcode.cn/problems/number-of-zigzag-arrays-iii/) · Hard · 灵茶山艾府：[拉格朗日插值](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3916.Number of ZigZag Array III

<https://leetcode.cn/problems/number-of-zigzag-arrays-iii/description/>

题目给出三个整数n、l和r，其中n在3到200之间，l和r则满足1 \<\= l \<\= r \<\= 10^9。

现在要求构造长度为n的zigzag数组，满足

- 其中每个元素都在l到r之间
- 任意两个相邻元素都互不相同
- 任意三个连续元素既不单调递增，也不单调递减

问可以构造的合法zigzag数组的数目是多少。答案对10^9 + 7取模。

首先可以进行最初步的转化。题目中的zigzag主要考察的是元素间的大小关系，而元素绝对大小只需要限制在l到r之间就行了，那么可以把问题从使用l到r之间的元素构造zigzag数组，转化为使用0到r - l之间的元素构造zigzag数组。

方便期间，在先这里将r更新为r - l，接下来就基于使用0到r之间的元素构造zigzag数组来进行讨论。

接下来，zigzag数组可以是vvvv..形的，也可以是^^^^..形的，不过可以明确的是，这两类的zigzag数组实际上是一一对应的。具体来说，对于任意一个vvvv..形的zigzag数组，将其中所有元素v都替换成r - v，就形成了一个与之对应的^^^^..形的zigzag数组。换言之，在这里只需要计算其中一种类型的zigzag数组的总数就行了，乘以2之后就是最终答案。

接下来考察如何计算vvvv..形的zigzag数组的数目。如果抛开r巨大的取值范围不看，动态规划是很容易想到的。令f[length][v]表示长度为index，最后一个元素值为v的zigzag数组的数目，那么对于f[length][v]：

1、若length为奇数，说明当前元素是一个谷值，那么就有

f[length][v] \= f[length - 1][r] + f[length - 1][r - 1] + ... + f[length - 1][v + 1]

2、若length为偶数，说明当前元素是一个峰值，那么就有

f[length][v] \= f[length - 1][0] + f[length - 1][1] + ... + f[length - 1][v - 1]

注意到两个转移方程分别是后缀和与前缀和的形式，在这里就可以令s[length][v]表示f[length][0]到f[length][v]之和，那么上面的转移方程就可以写成

1、若length为奇数，f[length][v] \= s[length - 1][r] - s[length - 1][v]

2、若length为偶数，f[length][v] \= s[length - 1][v - 1]

得到所有的f[length]后，再一趟遍历，计算s[length][0]到s[length][r]即可。

最后，基于f和s的更新方式，在这里可以省去length这一维，而vvvv形的zigzag数组的数目就是s[-1]。

最后再考虑如何处理r巨大的情况。在这里显然无法再使用上面带有值域的动态规划，一个常见的想法就是看看小数值的结果，尝试从中寻找规律。

可惜对于本题，由于转移方程与奇偶有关，不是很规整，很难直接观察出规律，不过有一点可以明确的是，每一轮都是前缀和或者后缀和，因此使用0到r之间的元素构成的长度为n的zigzag数组的数量，必然是一个以r为参数n次的多项式g[r]。有由于这里n的取值范围较小，那么就可以先计算出g[0]到g[n]，相当于使用n + 1个点来唯一确定一条n次的曲线。这样一来，就可以考虑把所有系数都解出来，然后把r带进去，就可以计算得到g[r]了。

然而，想直接把系数解出来也是非常困难的，在这里需要使用拉格朗日插值法，利用g[0]到g[n]的结果，在不计算出系数的前提下直接计算出g[r]。拉格朗日插值法相关的东西这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def zigZagArrays(self, n, l, r):
        """
        :type n: int
        :type l: int
        :type r: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7

        def calc(r):
            f = []
            s = []
            for v in range(r + 1):
                f.append(v)
                if not s:
                    s.append(f[-1])
                else:
                    s.append(s[-1] + f[-1])

            for length in range(3, n + 1):
                for v in range(r + 1):
                    if length % 2 == 0:
                        if v == 0:
                            f[v] = 0
                        else:
                            f[v] = s[v - 1]
                    else:
                        f[v] = s[-1] - s[v]
                        if f[v] < 0:
                            f[v] += mod
            
                s = []
                for v in range(r + 1):
                    if not s:
                        s.append(f[v])
                    else:
                        s.append(s[-1] + f[v])
                        if s[-1] >= mod:
                            s[-1] -= mod

            res = s[-1] + s[-1]
            if res >= mod:
                res -= mod
            return res

        def quick_pow(base, p):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            res = quick_pow(base, p // 2)
            res = res * res % mod
            if p % 2 == 1:
                res = res * base % mod
            return res

        r -= l
        if r <= n:
            return calc(r)
        
        x = []
        y = []
        for v in range(n + 1):
            x.append(v)
            y.append(calc(v))

        res = 0
        for p in range(n + 1):
            a, b = 1, 1
            for index in range(n + 1):
                if p == index:
                    continue

                a = a * (r - x[index]) % mod
                b = b * (x[p] - x[index]) % mod
            
            a = a * y[p] % mod

            res = (res + a * quick_pow(b, mod - 2) % mod) % mod
        
        return res
```
