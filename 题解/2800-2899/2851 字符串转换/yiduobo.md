---
title: "2851. 字符串转换"
aliases: ["yiduobo的每日leetcode 2851.字符串转换"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "leetcode/string-matching", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660819574"
zhihu_id: "660819574"
zhihu_title: "yiduobo的每日leetcode 2851.字符串转换"
question_id: "2851"
question: "字符串转换"
problem_url: "https://leetcode.cn/problems/string-transformation/"
difficulty: "Hard"
rating: 2858
created: "2023-10-12T03:36:53+08:00"
updated: "2023-10-12T03:36:53+08:00"
upvotes: 0
comments: 0
---

# 2851. 字符串转换

> **[yiduobo的每日leetcode 2851.字符串转换](https://zhuanlan.zhihu.com/p/660819574) · 知乎 · 2023-10-12 · 赞同 0**
> 力扣：[2851. 字符串转换](https://leetcode.cn/problems/string-transformation/) · Hard · 灵茶山艾府：[KMP + 矩阵快速幂优化 DP（附题单）Python/Java/C++/Go/JS](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2851.字符串转换

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/string-transformation/description/)

题目每次移动相当于让字符串中的字符循环了一些位置，但是这里循环的位置限定在1到n - 1之间，这也就意味着不能保持不变。另外从样例2中可以发现，循环的s中可能存在多个位置可以让t来匹配。更进一步的，对于循环字符串的问题通常是原样复制一份拼在后面，那么在这里就可以先利用kmp算法计算出t在循环s中所有的匹配位置。

关于kmp算法相关的内容可以参考之前的28题，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 28.实现 strStr()](https://zhuanlan.zhihu.com/p/117670077)

不妨设一共有match个匹配位置，那么接下来就需要考虑每一轮如何对字符串进行操作。

若当前字符串已经变成了t，那么下一步操作中有match - 1种方案可以使得字符串依然保持在t，这里只有match - 1的理由是不能保持不变。反之，就有n - 1 - (match - 1)种方案会使得字符串变为非t。

另一方面，若当前字符串不是t，那么下一步操作中就有match种方案可以使得字符串变成t，反之就有n - 1 - match种方案会使得字符串保持在非t状态。

到了这里，就很容易想到一种动态规划的做法。令f[i]和g[i]分别表示经过i次操作之后可以使得字符串变为t和不能使得字符串变为t的方案数，那么对于f[i]和g[i]，首先考虑边界情况。当s一开始就和t一样时，有f[0] \= 1，g[0] \= 0，反之有f[0] \= 0, g[0] \= 1。接下来，对于i > 0的情况，有

f[i] \= f[i - 1] \* (match - 1) + g[i - 1] \* match

g[i] \= f[i - 1] \* (n - match) + g[i - 1] \* (n - 1 - match)

计算完成后，f[-1]即为最终答案。

不过在这里还有一个问题，就是题目中的k非常巨大，逐步计算肯定是不行的，需要进行优化。

对于上面f[i]、g[i]关于f[i - 1]、g[i - 1]的两个方程，如果将f[i]、g[i]以及f[i - 1]、g[i - 1]写成1 \* 2的矩阵，即

\[f\[i\], g\[i\]\]和\[f\[i - 1\]、g\[i - 1\]\]，那么在这里就是需要找到一个2 \* 2的矩阵A，使得

\[f\[i - 1\], g\[i - 1\]\] \* A \= \[f\[i\], g\[i\]\]

更具体的，就有

f[i - 1] \* A[0][0] + g[i - 1] \* A[1][0] \= f[i]

f[i - 1] \* A[0][1] + g[i - 1] \* A[1][1] \= g[i]

带入上面的方程很容易得到A \= \[\[match - 1, n - match\], \[match, n - 1 - match\]\]，而此时的\[f\[k\], g\[k\]\]可以写成\[f\[k\], g\[k\]\] \= \[f\[0\], g\[0\]\] \* A \* A \* ... \* A，这里一共是k个A。

又由于矩阵的乘法满足结合律，因此可以优先计算后面这k个A的乘积，接下来只需要使用快速幂求解，就可以在O(logk)的时间内计算出f[k]和g[k]了。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, s, t, k):
        """
        :type s: str
        :type t: str
        :type k: int
        :rtype: int
        """

        nxt = [0]
        n = len(s)
        p = 0
        for index in range(1, n):
            while p and t[p] != t[index]:
                p = nxt[p - 1]
            if t[p] == t[index]:
                p += 1
            nxt.append(p)
        
        match = 0
        p = 0
        for index in range(n + n - 1):
            while p > 0 and t[p] != s[index % n]:
                p = nxt[p - 1]
            if t[p] == s[index % n]:
                p += 1
            if p == n:
                match += 1
                p = nxt[p - 1]
        
        if s == t:
            f, g = 1, 0
        else:
            f, g = 0, 1
        
        #for i in range(k):
        #    f, g = f * (match - 1) + g * match, f * (n - match) + g * (n - 1 - match)
        mod = 10 ** 9 + 7
        base = [[match - 1, n - match], [match, n - 1 - match]]

        def matMul(a, b):
            c = [[0, 0], [0, 0]]
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        c[i][j] += a[i][k] * b[k][j]
                        c[i][j] %= mod
            return c

        def quickPow(base, k):
            if k == 1:
                return base[:]
            
            res = quickPow(base, k / 2)
            res = matMul(res, res)

            if k % 2 == 1:
                res = matMul(res, base)
            
            return res

        final = quickPow(base, k)
        return (f * final[0][0] + g * final[1][0]) % mod
```
