---
title: "1510. 石子游戏IV"
aliases: ["yiduobo的每日leetcode 1510.石子游戏IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/420377170"
zhihu_id: "420377170"
zhihu_title: "yiduobo的每日leetcode 1510.石子游戏IV"
question_id: "1510"
question: "石子游戏 IV"
problem_url: "https://leetcode.cn/problems/stone-game-iv/"
difficulty: "Hard"
rating: 1787
created: "2021-10-11T23:51:09+08:00"
updated: "2021-10-11T23:51:09+08:00"
upvotes: 0
comments: 0
---

# 1510. 石子游戏IV

> **[yiduobo的每日leetcode 1510.石子游戏IV](https://zhuanlan.zhihu.com/p/420377170) · 知乎 · 2021-10-11 · 赞同 0**
> 力扣：[1510. 石子游戏 IV](https://leetcode.cn/problems/stone-game-iv/) · Hard · 灵茶山艾府：[三种写法：记忆化搜索/查表法/刷表法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1510.石子游戏IV

[力扣](https://leetcode-cn.com/problems/stone-game-iv/)

没想到博弈论的做法，只好老老实实用动态规划来做。

令f[i]表示剩余i颗式子的时候先手是否必胜，那么对于f[i]，可以枚举1到i之间的所有完全平方数，换言之可以从1到sqrt(i)进行枚举这个平方根x，若期间存在某个x满足f[i - x\*x]为假，那么此时先手拿走x\*x颗石头之后，后手面对剩下的i - x\*x颗石头是必败的，也就是说此时先手必胜，那么就有f[i]为真。若起见不存在这样的x，那么f[i]为假。

动态规划完成后，f[n]就是最终答案，总的时间复杂度为O(n \* sqrt(n))。

最后附上python代码：

```python
class Solution(object):
    def winnerSquareGame(self, n):
        """
        :type n: int
        :rtype: bool
        """

        f = [False] * (n + 1)
        for num in range(1, n + 1):
            x = 1
            while x * x <= num:
                if not f[num - x * x]:
                    f[num] = True
                    break

                x += 1
        
        return f[-1]
```
