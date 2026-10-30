---
title: "2338. 统计理想数组的数目"
aliases: ["yiduobo的每日leetcode 2338.统计理想数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/559661052"
zhihu_id: "559661052"
zhihu_title: "yiduobo的每日leetcode 2338.统计理想数组的数目"
question_id: "2338"
question: "统计理想数组的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-ideal-arrays/"
difficulty: "Hard"
rating: 2615
created: "2022-08-31T02:08:55+08:00"
updated: "2022-08-31T02:08:55+08:00"
upvotes: 1
comments: 0
---

# 2338. 统计理想数组的数目

> **[yiduobo的每日leetcode 2338.统计理想数组的数目](https://zhuanlan.zhihu.com/p/559661052) · 知乎 · 2022-08-31 · 赞同 1**
> 力扣：[2338. 统计理想数组的数目](https://leetcode.cn/problems/count-the-number-of-ideal-arrays/) · Hard · 灵茶山艾府：[【图解】转化成放球问题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2338.统计理想数组的数目

[力扣](https://leetcode.cn/problems/count-the-number-of-ideal-arrays/)

拿到题目的第一想法就是令d[i][j]表示长度为i，且以数字j结尾的合法数组数目，但是n和maxValue的规模都不小，再加上状态转移的复杂度，使用最朴素的动态规划无论时间还是空间都不允许，需要想办法高效求解d[i][j]。

题目涉及到整除，那么一个自然的想法就是从质因数入手。

首先考虑特殊情况。当j等于1时，d[i][j]必然为1，即数组中全都是1。

接下来是一般情况。对于大于等于2的任意自然数j，都可以写成

j\= (p[0]^k[0]) \* (p[1]^k[1]) \* ... \* (p[m] ^ k[m])

这里数组p中都是质数，而数组k中则都是正整数

不妨设一个长度为i，以j结尾的合法数组为num[0]、num[1]、...、num[i - 1]，那么首先就有num[i - 1] \= j。

在这里将num[i - 1]写成

num[i - 1] \= (p[0]^k[i - 1][0]) \* (p[1]^k[i - 1][1]) \* ... \* (p[m] ^ k[i - 1][m])

接下来，num[i - 2]则必须满足

num[i - 2] \= (p[0]^k[i - 2][0]) \* (p[1]^k[i - 2][1]) \* ... \* (p[m] ^ k[i - 2][m])

这里的k[i - 2]中的数都是自然数，且都必须满足k[i - 2][index] \<\= k[i - 1][index]

类似的，对于num[i - 3]，写成上面的形式之后则有k[i - 3][index] \<\= k[i - 2][index]，以此类推

可以发现，问题实际上就转化成了有多少个长度为i，且最后一个元素为多元组(k[i - 1][0]、k[i - 1][1]、k[i - 1][index])的递增数组的数目。

以i \= 3，j \= 6为例。

最后一个数6 \= 2^1 \* 3^1，那么在这里数组中的最后一个元素就是二元组(1, 1)，满足条件的数组就有

[(0, 0)，(0, 0)，(1, 1)]，对应到数值数组[1, 1, 6]

[(0, 0)，(0, 1)，(1, 1)]，对应到数值数组[1, 3, 6]

[(0, 0)，(1, 0)，(1, 1)]，对应到数值数组[1, 2, 6]

[(0, 0)，(1, 1)，(1, 1)]，对应到数值数组[1, 6, 6]

[(0, 1)，(0, 1)，(1, 1)]，对应到数值数组[3, 3, 6]

[(0, 1)，(1, 1)，(1, 1)]，对应到数值数组[3, 6, 6]

[(1, 0)，(1, 0)，(1, 1)]，对应到数值数组[2, 2, 6]

[(1, 0)，(1, 1)，(1, 1)]，对应到数值数组[2, 6, 6]

[(1, 1)，(1, 1)，(1, 1)]，对应到数值数组[6, 6, 6]

一共是d[i][j] \= 9种

可以发现，不同质因子的指数是互不影响的，那么可以令c\[k\]表示以数字k为结尾的长度为i的递增数组的数目，接下来就只需要分别求解c\[k\[i - 1\]\[0\]\]、c\[k\[i - 1\]\[1\]\]、...、c\[k\[i - 1\]\[index\]\]，然后根据乘法原理将这些值相乘，就是一开始需要求解的d\[i\]\[j\]了。

还是上面i \= 3, maxValue \=6的例子。在这里分别考虑两个长度为3，且最后一个数为1的递增子数组，那么一共就有

[0, 0, 1]

[0, 1, 1]

[1, 1, 1]

共3种情况，因此最终的d[i][j] \= 3 \* 3 \= 9

当然，在这里求解以数字k结尾，长度为i的递增数组的数目这个问题肯定是不能靠逐个枚举的。常规的做法是通过组合数学中的插板法来进行求解。

不妨考虑有一排共i个球，在这里实际上就相当于要在0的左侧、0和1之间、1和2之间、...、i - 2和i - 1之间这一共i - 1个空位中插入k个板子，将这i个球分成k + 1段。然后从左到右将每一段依次按0、1、...、k来进行填充就得到了一个合法的子数组。

需要注意的是，在这里第i - 1个球的右侧是不允许插板的，因为在这里必须要保证数组是以k结尾，也就意味着最后一段中至少有一个数存在，因此在最后一个求的右侧不允许插板。

接下来，更进一步的转化就是将这k个板子也视为k个球，那么问题就变成了从i - 1 + k个球中选择k个球作为板子。到了这里答案就很明显了，就是C(i + k - 1, k)。

到了这里，就有了大致的算法。对于d[i][j]，先将j分解质因数，得到

j\= (p[0]^k[0]) \* (p[1]^k[1]) \* ... \* (p[m] ^ k[m])

接下来对于p[index]，可以构成的合法子数组就是C(i + k[index] - 1, k[index])，因此就有

d[i][j] \= C(i + k[0] - 1, k[0]) \* C(i + k[1] - 1, k[1]) \* ... \* C(i + k[1] - 1, k[1])

为了高效求解，那么还需要先预处理出所有需要用到的C。由于题目中的maxValue \<\= 10000，那么在这里面，幂次最大的就是2^13 \= 8192，也就意味着上面的k数组中的最大值为13，于是只需要预处理出这一部分的C值即可。值得一提的是，由于题目中需要进行取模运算，因此按常规的乘除法来计算的话还需要额外用到逆元，所以在这里使用递推法，也就是C(m, n) \= C(m - 1, n - 1) + C(m - 1, n)来求解是更好的选择。

预处理出C之后，还有一个需要预处理的问题就是如何高效分解质因数

j\= (p[0]^k[0]) \* (p[1]^k[1]) \* ... \* (p[m] ^ k[m])

在这里我才用的是先执行一次筛法，同时在这个过程中更新f[i]为i的最小质因数。那么对于一个数num，不断用num除以f[num]直到num等于1位置，过程中的f[num]就是num所有质因数了。

最后附上python代码：

```python
class Solution(object):
    def idealArrays(self, n, maxValue):
        """
        :type n: int
        :type maxValue: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7

        f = [0] * 14
        c = [1]
        for i in range(1, n + 13):
            g = f[:]
            f = []
            for j in range(min(i + 1, 14)):
                if j == 0 or j == i:
                    f.append(1)
                else:
                    f.append(g[j - 1] + g[j])
                    if f[-1] >= mod:
                        f[-1] -= mod

            if i >= n:
                c.append(f[i - n + 1])

        f = range(maxValue + 1)
        now = 2
        while now * now <= maxValue:
            if f[now] == now:
                for index in range(now + now, maxValue + 1, now):
                    if f[index] == index:
                        f[index] = now
            now += 1

        res = 1
        for num in range(2, maxValue + 1):
            now = num
            prime_cnt = []
            last_prime = None

            while now != 1:
                if f[now] == last_prime:
                    prime_cnt[-1] += 1
                else:
                    prime_cnt.append(1)
                    last_prime = f[now]
                
                now /= f[now]
            
            delta = 1
            for cnt in prime_cnt:
                delta = delta * c[cnt] % mod
            
            res = (res + delta) % mod
        
        return res
```
