---
title: "996. 正方形数组的数目"
aliases: ["yiduobo的每日leetcode 996.正方形数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365496103"
zhihu_id: "365496103"
zhihu_title: "yiduobo的每日leetcode 996.正方形数组的数目"
question_id: "996"
question: "平方数组的数目"
problem_url: "https://leetcode.cn/problems/number-of-squareful-arrays/"
difficulty: "Hard"
created: "2021-04-16T22:47:24+08:00"
updated: "2021-04-16T22:47:24+08:00"
upvotes: 0
comments: 0
---

# 996. 正方形数组的数目

> **[yiduobo的每日leetcode 996.正方形数组的数目](https://zhuanlan.zhihu.com/p/365496103) · 知乎 · 2021-04-16 · 赞同 0**
> 力扣：[996. 平方数组的数目](https://leetcode.cn/problems/number-of-squareful-arrays/) · Hard · 灵茶山艾府：[相邻相关状压 DP：记忆化搜索 -> 递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

996.正方形数组的数目

[力扣](https://leetcode-cn.com/problems/number-of-squareful-arrays/)

将每个数视为无向图中的一个点，那么对于A[i]和A[j]，若二者之和为完全平方数，那么A[i]和A[j]是可以相邻放置的，于是在图中建立一条连接i和j的边。那么现在问题就又变成了图中存在多少条汉密尔顿路径，依然是采用熟悉的状态压缩动态规划来解决。

建好图之后，设f[state][x]为当前使用了state中的数，最后一个数为A[x]时有多少种合法的方案，那么对于f[state][x]而言，可以枚举与x相邻的所有点next，若next未出现在state中，那么就有f[state | (1 \<\< next)][next] +\= f[state][x]。

求解完毕后，res \= sum(f[(1 \<\< n) - 1])就是合法的方案数。

最后还需要去重。不妨设有k个A[i]，那么这k个A[i]可以互相替换，将会产生k阶乘种重复的答案，因此此时应该将res除以k阶乘来达到消除由A[i]带来的重复。更进一步的，对于A中所有的数，我们都应该统计其出现的次数，然后将res除以这个次数的阶乘。

最后附上python代码：

```python
class Solution(object):
    def numSquarefulPerms(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        g = {}

        n = len(A)
        for i in range(n):
            g[i] = set()
            for j in range(n):
                if i == j:
                    continue
                if int(sqrt(A[i] + A[j])) ** 2 == A[i] + A[j]:
                    g[i].add(j)
        
        f = [[0] * n for _ in range(1 << n)]
        q = []
        for i in range(n):
            q.append([1 << i, i])
            f[1 << i][i] = 1
        
        l, r = 0, len(q)
        while l < r:
            for state, x in q[l : r]:
                for next in g[x]:
                    if state & (1 << next) == 0:
                        next_state = state | (1 << next)
                        if f[next_state][next] == 0:
                            q.append([next_state, next])
                        f[next_state][next] += f[state][x]
            
            l, r = r, len(q)

        res = sum(f[(1 << n) - 1])
        cnt_dict = {}
        for num in A:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        for cnt in cnt_dict.values():
            for i in range(cnt, 1, -1):
                res /= i
        
        return res
```
