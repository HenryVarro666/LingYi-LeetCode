---
title: "1563. 石子游戏V"
aliases: ["yiduobo的每日leetcode 1563.石子游戏V"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/十一-优化-DP", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426985964"
zhihu_id: "426985964"
zhihu_title: "yiduobo的每日leetcode 1563.石子游戏V"
question_id: "1563"
question: "石子游戏 V"
problem_url: "https://leetcode.cn/problems/stone-game-v/"
difficulty: "Hard"
rating: 2087
created: "2021-10-31T18:38:04+08:00"
updated: "2021-10-31T18:38:04+08:00"
upvotes: 0
comments: 0
---

# 1563. 石子游戏V

> **[yiduobo的每日leetcode 1563.石子游戏V](https://zhuanlan.zhihu.com/p/426985964) · 知乎 · 2021-10-31 · 赞同 0**
> 力扣：[1563. 石子游戏 V](https://leetcode.cn/problems/stone-game-v/) · Hard · 灵茶山艾府：[动态规划：从 O(n^3) 到 O(n^2)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1563.石子游戏V

[力扣](https://leetcode-cn.com/problems/stone-game-v/)

经典的区间动态规划问题。令f[i][j]表示i到j这一段所能得到的最大分数，那么对于f[i][j]：

1、若i \= j，那么必然有f[i][j] \= 0

2、若i \< j，那么可以从i到j - 1枚举分割点cut_pos。此时计算i到cut_pos以及cut_pos + 1到j这两段石子的和，分别记为l_s和r_s：

2-1）若l_s \< r_s，那么bob将清理掉cut_pos + 1到j这一段石子，于是有

f[i][j] \= max(f[i][j], f[i][cut_pos] + l_s)

2-2）若l_s > r_s，那么bob将清理掉i到cut_pos这一段石子，于是有

f[i][j] \= max(f[i][j], f[cut_pos + 1][j] + r_s)

2-3）若l_s \= r_s，那么alice可以选择留下其中一段石子，而无论留下哪段石子，本次操作的得分都是l_s，于是有

f[i][j] \= max(f[i][j], max(f[i][cut_pos], f[cut_pos + 1][j]) + l_s)

动态规划完成后，f[0][n - 1]就是最终答案。

上面做法是O(n^3)的，时间复杂度上还是比较吃紧的。注意到上面l_s和r_s的三种大小关系，实际上完全可以在动态规划之前就通过预处理求出对于所有的f[i][j]而言，l_s和r_s大小关系发生变化的临界位置在哪里，不妨记为pos[i][j]。那么对于f[i][j]而言，三种情况就都有一个确切的边界了。对于pos的求解，则可以利用正数数组前缀和的单调性，在O(n^2)的时间复杂度内解决。除此之外，如果将状态转移方程中的l_s和r_s拆分开，那么就有

2-1）l_s \< r_s：

f[i][j] \= max(f[i][j], f[i][i] + stone[i], f[i][i + 1] + stone[i] + stone[i + 1], ...

f\[i\]\[pos\[i\]\[j\]\] + stone\[i\] + stone\[i + 1\] + ... + stone\[pos\[i\]\[j\]\])

可以发现，后续的这些项可以认为是以i起点的某种区间最大值。由于这些项在之前都已经求解过，那么完全可以使用一个数组维护其这个固定起点的区间最大值。令g[i][j]表示左边界为i，右边界k \<\= j的区间中，f[i][k] + stone[i] + stone[i + 1] + ... + stone[k]的最大值，那么上面的状态转移方程就可以写成

f\[i\]\[j\] \= max(f\[i\]\[j\], g\[i\]\[pos\]\[i\]\[j\]\])

2-2）l_s > r_s：

与2-1类似，此时是右侧区间，因此可以使用一个数组h，其中h[i][j]表示右边界为j，左边界k >\= i的区间中，f[k][j] + stone[k] + stone[k + 1] + ... + stone[j]的最大值，此时状态转移方程可以写成

f[i][j] \= max(f[i][j], h[pos[i][j] + 2][j])

这里pos[i][j] + 2的理由是根据定义，有

(stone\[i\] + stone\[i + 1\] + ... + stone\[pos\[i\]\[j\]\]) \* 2 \<\= stone\[i\] + stone\[i + 1\] + ... + stone\[j\]

此时若选取右侧式子的左边界为pos[i][j] + 1，那么右侧石子的总数

(stone[pos[i][j] + 1] + ... + stone[j]) \* 2 >\= stone[i] + stone[i + 1] + ... + stone[j]

从而得出

stone\[pos\[i\]\[j\] + 1\] + ... + stone\[j\] >\= stone\[i\] + stone\[i + 1\] + ... + stone\[pos\[i\]\[j\]\]

不符合2-2的假设l_s > r_s

而此时如果选择的是pos[i][j] + 2，由于

(stone\[i\] + stone\[i + 1\] + ... + stone\[pos\[i\]\[j\]\] + stone\[pos\[i\]\[j\] + 1\]) \* 2 > stone\[i\] + stone\[i + 1\] + ... + stone\[j\]

因此右侧石子的总数

(stone[pos[i][j] + 2] + ... + stone[j]) \* 2 \< stone[i] + stone[i + 1] + ... + stone[j]

这样一来就符合2-2的假设了

2-3）l_s \= r_s：

转化一下就是

(stone\[i\] + stone\[i + 1\] + ... + stone\[pos\[i\]\[j\]\]) \* 2 \= stone\[i\] + stone\[i + 1\] + ... + stone\[j\]

此时就有左半部分的转移方程依然是

f\[i\]\[j\] \= max(f\[i\]\[j\], g\[i\]\[pos\[i\]\[j\]\])

已经被情况1完全覆盖住了，因此在这里不需要进行额外的处理

右半部分的转移方程则是

f[i][j] \= max(f[i][j], h[pos[i][j] + 1][j])

此时，通过pos、g、h三个数组的帮助，就可以在O(1)的时间内完成状态转移了。而对于g自身而言，有

g[i][j] \= max(g[i][j - 1], f[i][j] + stone[i] + stone[i + 1] + ... + stone[j])

表示以i为左边界，右边界小于等于j时的最大值而言，若不考虑f[i][j]的值，即为g[i][j - 1]，若考虑f[i][j]的值，那么就是f[i][j] + stone[i] + stone[i + 1] + ... + stone[j]

同样的，对于h自身而言，有

h[i][j] \= max(h[i + 1][j], f[i][j] + stone[i] + stone[i + 1] + ... + stone[j])

这样一来，最终的时间复杂度就由O(n^3)优化到了O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def stoneGameV(self, stoneValue):
        """
        :type stoneValue: List[int]
        :rtype: int
        """

        n = len(stoneValue)
        f = [[0] * n for _ in range(n)]
        g = [[0] * n for _ in range(n)]
        h = [[0] * n for _ in range(n)]
        s = [stoneValue[0]]
        for index in range(1, n):
            s.append(s[-1] + stoneValue[index])

        pos = [[None] * n for _ in range(n)]
        for i in range(n):
            now_s = 0
            p = i - 1
            for j in range(i + 1, n):
                tot_s = s[j]
                if i > 0:
                    tot_s -= s[i - 1]
                
                while p < j and (now_s + stoneValue[p + 1]) * 2 <= tot_s:
                    now_s += stoneValue[p + 1]
                    p += 1
                
                pos[i][j] = p
        
        for l in range(1, n + 1):
            for i in range(n):
                j = i + l - 1
                if j >= n:
                    continue
                
                if l == 1:
                    g[i][j] = h[i][j] = stoneValue[i]
                    continue

                tot_s = s[j]
                if i > 0:
                    tot_s -= s[i - 1]

                if i <= pos[i][j]:
                    f[i][j] = max(f[i][j], g[i][pos[i][j]])
                    l_s = s[pos[i][j]]
                    if i > 0:
                        l_s -= s[i - 1]
                    if l_s + l_s == tot_s:
                        f[i][j] = max(f[i][j], h[pos[i][j] + 1][j])

                if pos[i][j] + 1 < j:
                    f[i][j] = max(f[i][j], h[pos[i][j] + 2][j])
                

                g[i][j] = max(g[i][j - 1], f[i][j] + tot_s)
                h[i][j] = max(h[i + 1][j], f[i][j] + tot_s)

        return f[0][n - 1]
```
