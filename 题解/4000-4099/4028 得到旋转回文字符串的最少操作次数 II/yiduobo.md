---
title: "4028. 得到旋转回文的最少操作次数II"
aliases: ["yiduobo的每日leetcode 4028.得到旋转回文的最少操作次数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/numpy", "leetcode/fast-fourier-transform"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077187539513913766"
zhihu_id: "2077187539513913766"
zhihu_title: "yiduobo的每日leetcode 4028.得到旋转回文的最少操作次数II"
question_id: "4028"
question: "得到旋转回文字符串的最少操作次数 II"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-ii/"
difficulty: "Hard"
created: "2026-08-30T01:20:05+08:00"
updated: "2026-08-30T01:20:08+08:00"
upvotes: 1
comments: 1
---

# 4028. 得到旋转回文的最少操作次数II

> **[yiduobo的每日leetcode 4028.得到旋转回文的最少操作次数II](https://zhuanlan.zhihu.com/p/2077187539513913766) · 知乎 · 2026-08-30 · 赞同 1**
> 力扣：[4028. 得到旋转回文字符串的最少操作次数 II](https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-ii/) · Hard · 灵茶山艾府：[循环自卷积](灵茶山艾府.md)

因为家里有事，加上正好碰到了难题，索性鸽了一阵子。题解恢复更新，依然是每天两题，争取不卡题吧。

4028.得到旋转回文的最少操作次数II

<https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-ii/description/>

题目给出一个由小写英文字符组成的字符串s，其长度不超过50000。

现在可以按照任意顺序执行以下操作任意次，包括零次：

- 递增：选择一个下标index，并将s[index]替换为下一个小写字符。'z'之后的字符是'a'。
- 左旋：将字符串的第一个字符移动到末尾。

问使得s成为回文串所需的最少操作次数。

本题与之前的4021题题设相同，不过数据规模增加到了50000，之前O(n^2)的算法不在适用，必须想办法进行优化。

[yiduobo的每日leetcode 4021.得到旋转回文字符串的最少操作次数I](https://zhuanlan.zhihu.com/p/2072837887305978384)

之前O(n^2)的算法，其主要的复杂度来自两个部分，分别是枚举左移的位数，以及计算将左移后的字符串变为回文的代价。直观上来看，枚举位数的操作似乎是无法避免的，也就是说在这里只能想办法去优化计算代价的过程。

不妨设当前左旋的次数为r，那么对于一组处于回文位置上的字符，其下标对就是index与n - index - 1。更进一步的，在左旋之前，这两个字符在原字符串中的位置就是(index + r) % n，以及(n - index - 1 + r) % n。可以发现，这两个下标之和对n取模可以把index消去，得到的项是(r \* 2 - 1) % n。换言之，对于确定下来的旋转次数r，接下来需要计算的就是所有下标和对n取模等于(r \* 2 - 1) % n的下标对。

到了这一步，依然没有取得什么实质性的进展，因为此时依然需要枚举，才能得到所有符合条件的下标对。

既然先枚举r行不通，那么不妨换一种思路，先把所有不同下标的字符对的代价都计算好，然后根据下标之和模n分别收集起来得到代价和数组g，最后再枚举r，取最小的r + g[(r \* 2 - 1) % n]作为最终答案即可。

上面这种方法乍一看依然是O(n^2)的，因为需要两两枚举下标对，不过在这里还有一个条件可以利用，那就是字符串中只有小写字符，也就是说不同的字符对只有26 \* 25 // 2 \= 325种。另一方面， 在确定了字符对之后，将二者变为相同的代价是很容易计算的，设二者ascii码之差为dis，那么代价就是min(dis, 26 - dis)。更进一步的，如果对于每种字符对，能高效地按照下标之和模n分别统计这种字符对出现的数量，那么就可以很容易得到g。

接下来的问题就变成了如何高效地按照下标之和模n统计字符串的数量。

由于需要计算下标之和模n，因此最直观的想法就是先按照字符将出现的下标收集起来，得到二维下标数组p。其中p[c]按顺序记录了字符c出现的所有下标。那么对于一组字符串a和b，最直观的做法就是两两枚举p[a]以及p[b]中的所有下标对，计算下标之后模n，然后更新g。很遗憾，这里的算法依然是O(n^2)的，因为本质上依然还是在逐对枚举下标对。虽然将下标按字符分别收集了起来，但是由于这些下标是不连续的，因此除了枚举似乎没有其他更好的办法来进行处理。

接下来，就需要进行一个漂亮的变形了。

由于此时的瓶颈是出现位置不连续，那么在这里可以进行如下转化：对于每种字符c，建立一个长度为n的01数组f[c]。若原字符串中下标为index的字符s[index]恰好为c，那么令f[c][index]为1，否则令f[c][index]为0。

经过这个变换后，位置就变得连续了起来，而对于一组字符a和b，此时就可以使用f[a][idx_a] \* f[b][idx_b] \* cost(a, b)来更新g[(idx_a + idx_b) % n]，其中cost(a, b)表示将a和b变为相同的代价。这么做的意义是，只有当s[idx_a]恰好为a，s[idx_b]恰好为b时，才将这一组字符对(a, b)的代价更新到g[(idx_a + idx_b) % n]，也代价数组g中下标之和模n对应的位置。

到了这里，看上去依然是两个长度为n的多项式相乘，复杂度还是O(n^2)，但是对于多项式相乘的问题，可以利用fft进行优化。关于fft的内容可以参考之前的3549题，这里就不展开了。

[yiduobo的每日leetcode 3549.两个多项式相乘](https://zhuanlan.zhihu.com/p/1909408038735024521)

不过基于本题01数组相乘的特殊性，在这里改用ntt可以避免实数运算。

ntt的本质和fft类似，都是通过寻找若干个特殊的点位，高效计算出这个多项式在这些点上的值，然后利用C[idx] \= A[idx] \* B[idx]的特性，直接通过点积计算出结果多项式在这些点上的值，在通过逆运算还原出结果多项式。不同的是，fft使用的是单位根，而ntt则是先取一个形如k \* 2^pow + 1的大质数，然后通过这个大质数的原根来进行变换。

具体来说，对于本题结果多项式长度不超过10^6的情况，可以取用p \= 3 \* 2^18 + 1作为这个大质数。实际上基于本题的数据规模而言，取最小的形如k \* 2^17 + 1的质数就行了，不过验算发现这里的k等于，也就是上面这个3 \* 2^18 + 1。

接下来，由于p是素数，因此至少可以找出一个原根g，这个g满足g % p、g^2 % p、...、g^(p - 1) % p恰好可以覆盖住1到p - 1。也就是说，在这里可以利用g^((p - 1) // m)作为变换的单位根ω，其中m为大于等于2n - 1的最小的2的幂。那么ω^0、ω、ω^2、...、ω^(m - 1)对p取模刚好走完一圈，同时也满足ω[idx]^k **≡** ω[idx \* k % m]，因此这一组ω的幂就可以同来充当着m个特殊的点。

对于上面的p，其最小的原根为10，接下来就可以根据s的长度计算出对应的m，然后计算出ω，预处理出ω的幂次并如fft一样执行蝶形算法就行了。需要注意的是，在过程中需要将中间结果对p取模。

另外，在最后执行intt时，使用的单位根应该取ω关于模p的逆元，在这里有一个现成的，也就是ω^(m - 1) % p。而在执行ifft后需要将结果除以m，在这里则同样是乘以m关于模p的逆元，可以使用p - (p - 1) // m。

到了这里，就可以先对每种字符计算出数组f，然后对于每种字符c，先对f[c]做一次ntt，接下来枚举所有的不同字符对，利用做了ntt之后的f数组高效更新g数组，这一步的复杂度就从O(325 \*(n^2))降低到了O(325 \* n)。最后，对g数组做intt，然后枚举r找出最终答案即可。

由于ntt的复杂度为O(nlogn)，因此最终的复杂度就是O(26 \* nlogn + 325 \* n)。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s):
        """
        :type s: str
        :rtype: int
        """

        def quick_power(base, p, mod):
            if p == 0:
                return 1
            if p == 1:
                return base
            
            x = quick_power(base, p >> 1, mod)
            x = x * x % mod
            if p & 1:
                x = x * base % mod
            return x

        n = len(s)
        f = [[0] * n for _ in range(26)]

        for index, c in enumerate(s):
            f[ord(c) - 97][index] = 1

        m = 1
        while m < n * 2 - 1:
            m <<= 1
        
        p = 3 * (1 << 18) + 1
        g = 10
        w = quick_power(g, (p - 1) // m, p)
        w_list = [1]
        for _ in range(m - 1):
            w_list.append(w_list[-1] * w % p)

        rw = w_list[-1]
        rw_list = [1]
        for _ in range(m - 1):
            rw_list.append(rw_list[-1] * rw % p)

        def ntt(f, m, w_list, mod):
            f.extend([0] * (m - len(f)))
            for index in range(m):
                v = index
                b = m >> 1
                x = 0
                while v:
                    if v & 1:
                        x |= b
                    b >>= 1
                    v >>= 1
                
                if index < x:
                    f[index], f[x] = f[x], f[index]
            
            length = 2
            while length <= m:
                for part in range(m // length):
                    for index in range(length // 2):
                        left = part * length + index
                        right = part * length + index + length // 2
                        u = f[left]
                        v = f[right] * w_list[m // length * index] % mod
                        f[left] = u + v
                        if f[left] >= mod:
                            f[left] -= mod
                        f[right] = u - v
                        if f[right] < 0:
                            f[right] += mod
                length <<= 1

        for x in range(26):
            ntt(f[x], m, w_list, p)

        g = [0] * m
        for x in range(26):
            for y in range(x + 1, 26):
                dis = abs(x - y)
                for index in range(m):
                    g[index] += min(dis, 26 - dis) * f[x][index] % p * f[y][index] % p
                    if g[index] >= p:
                        g[index] -= p

        ntt(g, m, rw_list, p)
        rm = p - (p - 1) // m
        for index in range(m):
            g[index] = g[index] * rm % p
        for index in range(n, m):
            g[index % n] += g[index]

        res = g[n - 1]
        for r in range(1, n):
            res = min(res, r + g[(r * 2 - 1) % n])
        return res
```
