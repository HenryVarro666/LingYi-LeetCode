---
title: "2930. 重新排列后包含指定子字符串的字符串数目"
aliases: ["yiduobo的每日leetcode 2930.重新排列后包含指定子字符串的字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/其他", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690473857"
zhihu_id: "690473857"
zhihu_title: "yiduobo的每日leetcode 2930.重新排列后包含指定子字符串的字符串数目"
question_id: "2930"
question: "重新排列后包含指定子字符串的字符串数目"
problem_url: "https://leetcode.cn/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/"
difficulty: "Medium"
rating: 2227
created: "2024-04-03T02:08:06+08:00"
updated: "2024-04-03T02:08:06+08:00"
upvotes: 1
comments: 0
---

# 2930. 重新排列后包含指定子字符串的字符串数目

> **[yiduobo的每日leetcode 2930.重新排列后包含指定子字符串的字符串数目](https://zhuanlan.zhihu.com/p/690473857) · 知乎 · 2024-04-03 · 赞同 1**
> 力扣：[2930. 重新排列后包含指定子字符串的字符串数目](https://leetcode.cn/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/) · Medium · 灵茶山艾府：[O(log n) 容斥原理（附记忆化搜索）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2930.重新排列后包含指定子字符串的字符串数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/description/)

题目实际上就是要求找出长度为n的字符串中，l和t都至少出现一次，e至少出现两次的字符串数量，那么在这里只需要将这些信息都表达出来，就能很容易得到一种动态规划的状态表示。

令f[i][l][e][t]表示长度为i且包含l个字符'l'，e个字符'e'，t个字符't'的字符串数量。可以发现，这里l、e、t的数量可能会非常大，但是在这里l和t的数量只需要大于等于1，e的数量只需要大于等于2，因此在这里可以精简一下状态表示，将所有大于1的l和t归类到至少存在一个'l'和't'，将大于2的e归类到至少存在两个'e'，因此在这里每个长度为i的字符串只会对应到2\*3\*2 \= 12种状态，而对于每种状态，都可以从上一轮某个字符数减1的状态带上特定字符，或者上一轮的同一状态带上非特定字符转移得到。

需要特别注意的事，在这里l取值为1、e取值为2、t取值为1时表示的是至少存在一个，因此上一轮的同一状态对应的非特定字符除了非'l'、'e'、't'的23个字符外，当l为1时也可以取'l'，当e为2时也可以取'e'，当t为1时也可以取't'，可以得到如下的状态转移方程：

f[i][0][0][0] \= f[i - 1][0][0][0] \* 23

f[i][0][0][1] \= f[i - 1][0][0][0] + f[i - 1][0][0][1] \* 24

f[i][0][1][0] \= f[i - 1][0][0][0] + f[i - 1][0][1][0] \* 23

f[i][0][1][1] \= f[i - 1][0][0][1] + f[i - 1][0][1][0] + f[i - 1][0][1][1] \* 24

f[i][0][2][0] \= f[i - 1][0][1][0] + f[i - 1][0][2][0] \* 24

f[i][0][2][1] \= f[i - 1][0][1][1] + f[i - 1][0][2][0] + f[i - 1][0][2][1] \* 25

f[i][1][0][0] \= f[i - 1][0][0][0] + f[i - 1][1][0][0] \* 24

f[i][1][0][1] \= f[i - 1][0][0][1] + f[i - 1][1][0][0] + f[i - 1][1][0][1] \* 25

f[i][1][1][0] \= f[i - 1][0][1][0] + f[i - 1][1][0][0] + f[i - 1][1][1][0] \* 24

f[i][1][1][1] \= f[i - 1][0][1][1] + f[i - 1][1][0][1] + f[i - 1][1][1][0] + f[i - 1][1][1][1] \* 25

f[i][1][2][0] \= f[i - 1][0][2][0] + f[i - 1][1][1][0] + f[i - 1][1][2][0] \* 25

f[i][1][2][1] \= f[i - 1][0][2][1] + f[i - 1][1][1][1] + f[i - 1][1][2][0] + f[i - 1][1][2][1] \* 26

计算完成后，f[n][1][2][1]即为最终答案。

另外，在这里每一轮的状态只与上一轮有关，因此可以使用滚动数组来优化掉i这一维。除此之外，在这里也可以写成矩阵乘法的形式优化时间复杂度，不过构造的矩阵很大会带来很大的常数。

最后附上python代码：

```python
class Solution(object):
    def stringCount(self, n):
        """
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        f = [0] * 12
        f[0] = 1
        for i in range(n):
            g = f[:]
            f = [0] * 12

            f[0] = g[0] * 23 % mod
            f[1] = (g[0] + g[1] * 24) % mod
            f[2] = (g[0] + g[2] * 23) % mod
            f[3] = (g[1] + g[2] + g[3] * 24) % mod
            f[4] = (g[2] + g[4] * 24) % mod
            f[5] = (g[3] + g[4] + g[5] * 25) % mod

            f[6] = (g[0] + g[6] * 24) % mod
            f[7] = (g[1] + g[6] + g[7] * 25) % mod
            f[8] = (g[2] + g[6] + g[8] * 24) % mod
            f[9] = (g[3] + g[7] + g[8] + g[9] * 25) % mod
            f[10] = (g[4] + g[8] + g[10] * 25) % mod
            f[11] = (g[5] + g[9] + g[10] + g[11] * 26) % mod
        
        return f[-1]
```
