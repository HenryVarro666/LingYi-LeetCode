---
title: "903. DI序列的有效排列"
aliases: ["yiduobo的每日leetcode 903.DI序列的有效排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353583246"
zhihu_id: "353583246"
zhihu_title: "yiduobo的每日leetcode 903.DI序列的有效排列"
question_id: "903"
question: "DI序列的有效排列"
problem_url: "https://leetcode.cn/problems/valid-permutations-for-di-sequence/"
created: "2021-02-28T20:58:40+08:00"
updated: "2021-02-28T20:58:40+08:00"
upvotes: 0
comments: 0
---

# 903. DI序列的有效排列

> **[yiduobo的每日leetcode 903.DI序列的有效排列](https://zhuanlan.zhihu.com/p/353583246) · 知乎 · 2021-02-28 · 赞同 0**
> 力扣：[903. DI序列的有效排列](https://leetcode.cn/problems/valid-permutations-for-di-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

903.DI序列的有效排列

[力扣](https://leetcode-cn.com/problems/valid-permutations-for-di-sequence/)

首先，注意到这里的D和I只涉及到相对大小，不关注每个数的绝对大小，同时这里是对一个0到n的排列进行处理，因此对于一个规模为k的子问题，我们无需关心这k + 1个数到底是什么，因为其答案都是一样的。

接下来，由于D和I涉及到大小，因此一个自然的想法就是先把当前最小的数给安排上，然后再进行分析。设f[l][r]表示S的l到r - 1这一段有多少种合法的情况，那么：

1、若S[l]为'i'，那么此时我们可以将最小值放在序列的最前面，然后根据上面的结论，这里就转化为了一个S的l + 1到r - 1的子问题。于是这里有

f[l][r] +\= f[l + 1][r]

2、若S[index - 1]为'd'，且s[index]为'i'，那么此时我们可以将最小值放在序列的第index位，此时就将序列分割成了l到index - 1以及index + 1到r - 1这两段。已知此时有r - l + 1个数，去除掉最小值之后还剩下r - l个，需要将其分为两个部分。由于我们不关心序列的具体构成，因此可以简单地认为这就是一个从r - l个数中选择index - l有多少种情况的问题，那么对应的方案就有C(r - l，index - l)种。于是这里有

f[l][r] +\= C(r - l, index - l) \* f[l][index - 1] \* f[index+ 1][r]

3、若S[r - 1]为'd'，那么此时我们可以将最小值放在序列的最后一位，于是这里有

f[l][r] +\= f[l][r - 1]

为了提高效率，步骤2中C可以先通过动态规划预先计算好，然后再进行动态规划。

最后附上python代码：

```python
class Solution(object):
    def numPermsDISequence(self, S):
        """
        :type S: str
        :rtype: int
        """

        n = len(S)
        mod = 10 ** 9 + 7

        C = [[1, 0]]
        for i in range(n):
            C.append([])
            for j in range(i + 2):
                C[-1].append((C[-2][j] + C[-2][j - 1]) % mod)
            C[-1].append(0)

        f = [[None] * (n + 1) for _ in range(n + 1)]
        return self.dfs(0, n, S, f, C, mod)

    def dfs(self, l, r, S, f, C, mod):
        if f[l][r] is None:
            if l == r:
                f[l][r] = 1
            else:
                f[l][r] = 0
                for cut_pos in range(l, r):
                    if S[cut_pos] == 'I':
                        if cut_pos == l:
                            f[l][r] += self.dfs(l + 1, r, S, f, C, mod)
                            f[l][r] %= mod
                        elif S[cut_pos - 1] == 'D':
                            f[l][r] += C[r - l][cut_pos - l] * self.dfs(l, cut_pos - 1, S, f, C, mod) * self.dfs(cut_pos + 1, r, S, f, C, mod)
                            f[l][r] %= mod
                    elif cut_pos == r - 1 and S[cut_pos] == 'D':
                        f[l][r] += self.dfs(l, r - 1, S, f, C, mod)
                        f[l][r] %= mod

        return f[l][r]
```
