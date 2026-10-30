---
title: "518. 零钱兑换II"
aliases: ["yiduobo的每日leetcode 518.零钱兑换II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260521115"
zhihu_id: "260521115"
zhihu_title: "yiduobo的每日leetcode 518.零钱兑换II"
question_id: "518"
question: "零钱兑换 II"
problem_url: "https://leetcode.cn/problems/coin-change-ii/"
difficulty: "Medium"
created: "2020-09-29T22:01:36+08:00"
updated: "2020-09-29T22:01:36+08:00"
upvotes: 0
comments: 0
---

# 518. 零钱兑换II

> **[yiduobo的每日leetcode 518.零钱兑换II](https://zhuanlan.zhihu.com/p/260521115) · 知乎 · 2020-09-29 · 赞同 0**
> 力扣：[518. 零钱兑换 II](https://leetcode.cn/problems/coin-change-ii/) · Medium · 灵茶山艾府：[【视频】完全背包：从记忆化搜索到递推，附题单！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

518.零钱兑换II <https://leetcode-cn.com/problems/coin-change-2/>

经典的背包问题，需要注意这里同样面试的硬币可以使用多次。

令f[i][j]表示用前i种硬币达成面值j能有多少种方法，那么就有

f\[i\]\[j\] \= f\[i - 1\]\[j\] + f\[i\]\[j - coin\[i\]\]

即使用前i -1种硬币直接达成面值j，或者使用前i - 1种硬币达成面值j - coin[i]同时带上一个coin[i]。

注意到这个状态转移方程是可以滚动的，于是可以写成

f\[j\] +\= f\[j - coin\[i\]\]

同时需要注意这里的j循环必须从小到大，即保证f\[i\]\[j - coin\[i\]\]能在f\[i\]\[j\]之前被处理到。

最后附上python代码：

```python
class Solution(object):
    def change(self, amount, coins):
        """
        :type amount: int
        :type coins: List[int]
        :rtype: int
        """

        f = [0] * (amount + 1)
        f[0] = 1
        for coin in coins:
            for index in range(coin, amount + 1):
                f[index] += f[index - coin]

        return f[amount]
```
