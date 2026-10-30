---
title: "1223. 掷骰子模拟"
aliases: ["yiduobo的每日leetcode 1223.掷骰子模拟"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383722571"
zhihu_id: "383722571"
zhihu_title: "yiduobo的每日leetcode 1223.掷骰子模拟"
question_id: "1223"
question: "掷骰子模拟"
problem_url: "https://leetcode.cn/problems/dice-roll-simulation/"
difficulty: "Hard"
rating: 2008
created: "2021-06-24T22:54:42+08:00"
updated: "2021-06-24T22:54:42+08:00"
upvotes: 0
comments: 0
---

# 1223. 掷骰子模拟

> **[yiduobo的每日leetcode 1223.掷骰子模拟](https://zhuanlan.zhihu.com/p/383722571) · 知乎 · 2021-06-24 · 赞同 0**
> 力扣：[1223. 掷骰子模拟](https://leetcode.cn/problems/dice-roll-simulation/) · Hard · 灵茶山艾府：[教你一步步思考动态规划！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1223.掷骰子模拟

[力扣](https://leetcode-cn.com/problems/dice-roll-simulation/)

动态规划的题目，令f[i][j][k]表示掷i次骰子，最后一次的结果为j，且最后连续k轮的结果都是j。那么对于f[i][j][k]：

1、当k大于1时，说明上一次的结果也是j，那么就有

f[i][j][k] \= f[i - 1][j][k - 1]

2、当k等于1时，说明上一次的结果除了j都可以，而出现的次数只要在rollmax的范围之内就行，那么就有

f[i][j][1] \= sum(f[i - 1]) - sum(f[i - 1][j])

其中sum(f[i - 1])表示上一轮所有合法情况的总数，而sum(f[i - 1][j])则表示上一轮所有合法，且掷出j的情况的总数。

sum(f[i - 1])在每一轮更新完成后就能计算出来，而对于sum(f[i - 1][j])而言，展开来就是

f\[i - 1\]\[j\]\[1\] + fi - 1\]\[j\]\[2\] + ... + f\[i - 1\]\[j\]\[rollmax\[j\]\]\]

具体实现时，由于每一轮的结果只与上一轮有关，因此我们可以先省去i这一维。接下来，对于f[i][j][1]这一项来说，sum(f[i - 1])是可以在每一轮结束时计算出来的，而sum(f[i - 1][j])则可以在上一轮计算f[i - 1][j]时使用一个数组统计起来。

最后附上python代码：

```python
class Solution(object):
    def dieSimulator(self, n, rollMax):
        """
        :type n: int
        :type rollMax: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        f = [[0] * (max(rollMax) + 1) for _ in range(6)]
        f[0][1] = 1
        f[1][1] = 1
        f[2][1] = 1
        f[3][1] = 1
        f[4][1] = 1
        f[5][1] = 1
        last_s = [1, 1, 1, 1, 1, 1]
        for i in range(2, n + 1):
            s = [0, 0, 0, 0, 0, 0]
            for j in range(6):
                for k in range(min(i, rollMax[j]), 1, -1):
                    f[j][k] = f[j][k - 1]
                    s[j] += f[j][k]
                    s[j] %= mod
                f[j][1] = (sum(last_s) - last_s[j]) % mod
                s[j] += f[j][1]
                s[j] %= mod
        
            last_s = s[:]

        return sum(last_s) % mod
```
