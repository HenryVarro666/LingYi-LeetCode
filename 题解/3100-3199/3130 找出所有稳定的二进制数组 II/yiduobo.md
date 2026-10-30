---
title: "3129. 找出所有稳定的二进制数组I & 3130. 找出所有稳定的二进制数组II"
aliases: ["yiduobo的每日leetcode 3129.找出所有稳定的二进制数组I && 3130.找出所有稳定的二进制数组II", "3129. 找出所有稳定的二进制数组I", "3130. 找出所有稳定的二进制数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/hard", "题单/动态规划", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702302113"
zhihu_id: "702302113"
zhihu_title: "yiduobo的每日leetcode 3129.找出所有稳定的二进制数组I && 3130.找出所有稳定的二进制数组II"
question_id: ["3129", "3130"]
question: ["找出所有稳定的二进制数组 I", "找出所有稳定的二进制数组 II"]
problem_url: ["https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-i/", "https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2825
created: "2024-06-08T00:14:57+08:00"
updated: "2024-06-08T00:14:57+08:00"
upvotes: 1
comments: 0
---

# 3129. 找出所有稳定的二进制数组I & 3130. 找出所有稳定的二进制数组II

> **[yiduobo的每日leetcode 3129.找出所有稳定的二进制数组I && 3130.找出所有稳定的二进制数组II](https://zhuanlan.zhihu.com/p/702302113) · 知乎 · 2024-06-08 · 赞同 1**
> 力扣：[3129. 找出所有稳定的二进制数组 I](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-i/) · Medium · 灵茶山艾府：[两种方法：动态规划 / 组合数学（Python/Java/C++/Go）](../3129%20找出所有稳定的二进制数组%20I/灵茶山艾府.md)
> 力扣：[3130. 找出所有稳定的二进制数组 II](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-ii/) · Hard · 灵茶山艾府：[从 DP 到组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3129.找出所有稳定的二进制数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-i/)

3130.找出所有稳定的二进制数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-ii/)

题目定义由zero个0，one个1组成的，且其中任意长度大于等于limit的子数组都同时包含了0和1的数组为稳定的二进制数组，给出zero、one以及limit，问可以组成多少个稳定的二进制数组。

两题的题设一致，后面这题的数据规模较大。

首先，基于本题的数据规模，只能考虑通过动态规划或者数学方法求解。数学方法对于limit的处理看上去会比较麻烦，所以先考虑能否使用动态规划求解。

由于限定了0和1的数目，那么在这里就需要考虑将当前情况下0和1的数组加入到状态表示中。又由于zero和one的取值范围较大，将二者的数目加入到状态表示中之后，状态数就已经来到了1000^2，此时已经不可能再将当前状态下的连续0或者连续1的数目加入到状态表示中来适配limit，而是只能通过状态转移来保证状态的合法性，因此在这里只能选择保留最后这一位是0还是1，即

令f[i][j]表示由i个0，j个1组成，且最后一位为0的稳定数组数目，令g[i][j]表示由i个0，j个1组成，且最后一位为1的稳定数组数目。

那么对于f[i][j]，在当前子数组的末尾可以是1、2、...、limit个连续的0，那么就有

f[i][j] \= g[i - 1][j] + g[i - 2][j] + ... + g[i - limit][j]

同样的，对于g[i][j]就有

g[i][j] \= f[i][j - 1] + f[i][j - 2] + ... + f[i][j - limit]

上面的转移方程复杂度为O(limit)，需要进行优化。

可以发现，f的转移方程是关于g的区间和，而g的转移方程则是关于f的区间和，那么一个自然的想法就是将区间和转化为前缀和，即令sf[i][j] \= f[i][0] + f[i][1] + ... + f[i][j]，令sf[i][j] \= g[0][j] + g[1][j] + ... + g[i][j]，那么上面的转移方程就可以写成

f[i][j] \= sg[i - 1][j] - sg[i - limit - 1][j]

g[i][j] \= sf[i][j - 1] - sf[i][j - limit - 1]

这样一来，转移的复杂度就优化到了O(1)。

另外在具体实现时，需要考虑i、j与limit的大小关系，避免在计算时越界。

最后附上python代码：

```python
class Solution(object):
    def numberOfStableArrays(self, zero, one, limit):
        """
        :type zero: int
        :type one: int
        :type limit: int
        :rtype: int
        """

        f = [[0] * (one + 1) for _ in range(zero + 1)]
        g = [[0] * (one + 1) for _ in range(zero + 1)]
        sf = [[0] * (one + 1) for _ in range(zero + 1)]
        sg = [[0] * (one + 1) for _ in range(zero + 1)]

        f[0][0] = g[0][0] = 1
        sf[0][0] = sg[0][0] = 0

        mod = 10 ** 9 + 7

        for i in range(zero + 1):
            for j in range(one + 1):
                if i > limit:
                    f[i][j] = (sg[i - 1][j] - sg[i - limit - 1][j] + mod) % mod
                elif i > 0:
                    f[i][j] = sg[i - 1][j]

                if j > limit:
                    g[i][j] = (sf[i][j - 1] - sf[i][j - limit - 1] + mod) % mod
                elif j > 0:
                    g[i][j] = sf[i][j - 1]

                if j > 0:
                    sf[i][j] = sf[i][j - 1]
                sf[i][j] = (sf[i][j] + f[i][j]) % mod

                if i > 0:
                    sg[i][j] = sg[i - 1][j]
                sg[i][j] = (sg[i][j] + g[i][j]) % mod

        return (f[-1][-1] + g[-1][-1]) % mod
```
