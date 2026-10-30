---
title: "3320. 统计能获胜的出招序列数"
aliases: ["yiduobo的每日leetcode 3320.统计能获胜的出招序列数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2164822061"
zhihu_id: "2164822061"
zhihu_title: "yiduobo的每日leetcode 3320.统计能获胜的出招序列数"
question_id: "3320"
question: "统计能获胜的出招序列数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-winning-sequences/"
difficulty: "Hard"
rating: 2153
created: "2024-10-21T02:29:57+08:00"
updated: "2024-10-21T02:29:57+08:00"
upvotes: 0
comments: 0
---

# 3320. 统计能获胜的出招序列数

> **[yiduobo的每日leetcode 3320.统计能获胜的出招序列数](https://zhuanlan.zhihu.com/p/2164822061) · 知乎 · 2024-10-21 · 赞同 0**
> 力扣：[3320. 统计能获胜的出招序列数](https://leetcode.cn/problems/count-the-number-of-winning-sequences/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3320.统计能获胜的出招序列数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-winning-sequences/description/)

alice和bob在进行锤子剪刀布的游戏，一共需要进行n轮。每轮胜者得一分，平手则都不得分。现在已知alice的出招序列s，问bob有多少种可行的出招序列，使得bob最终的得分大于alice，且bob的出招序列中不会有连续两轮出同一招。

经典的动态规划问题，令f[i][t][s]表示前i轮，最后一轮bob的出招为t，且bob的净胜分为s时的可行出招序列。

第一轮bob的出招不受上一轮的限制，那么可以尝试所有的三种出招，并更新f。而对于后续的轮次，则可以枚举上一轮出招prev、本轮的出招now以及上一轮的净胜分score，那么当prev与now不同时，就可以将f\[i - 1\]\[prev\]\[score\]累加到f\[i\]\[now\]\[score + delta\[now\]\[s\[i\]\]\]中，这里的delta\[now\]\[s\[i\]\]指的是bob出now，alice出s\[i\]时的净胜分。

计算完成后，枚举每种出招p，然后枚举所有正的净胜分score，将所有f[n - 1][p][score]累加起来即为最终答案。

另外注意到这里每轮f只与上一轮有关，因此可以使用滚动数组来省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def countWinningSequences(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        n = len(s)
        f = {'F': {}, 'W': {}, 'E': {}}
        delta = {'F': {'F': 0, 'W': -1, 'E': 1},
                 'W': {'F': 1, 'W': 0, 'E': -1},
                 'E': {'F': -1, 'W': 1, 'E': 0}
        }

        poke = ['F', 'W', 'E']
        for p in poke:
            f[p][delta[p][s[0]]] = 1

        mod = 10 ** 9 + 7
        for c in s[1:]:
            g = copy.deepcopy(f)
            f = {'F': {}, 'W': {}, 'E': {}}
            for prev in poke:
                for now in poke:
                    if prev == now:
                        continue
                    for score in g[prev]:
                        now_score = score + delta[now][c]
                        f[now][now_score] = (f[now].get(now_score, 0) + g[prev][score]) % mod

        res = 0
        for p in poke:
            for score in f[p]:
                if score > 0:
                    res = (res + f[p][score]) % mod
        
        return res
```
