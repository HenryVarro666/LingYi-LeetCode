---
title: "1406. 石子游戏III"
aliases: ["yiduobo的每日leetcode 1406.石子游戏III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/game-theory", "leetcode/monotonic-queue", "题单/动态规划", "题单/数学算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405928287"
zhihu_id: "405928287"
zhihu_title: "yiduobo的每日leetcode 1406.石子游戏III"
question_id: "1406"
question: "石子游戏 III"
problem_url: "https://leetcode.cn/problems/stone-game-iii/"
difficulty: "Hard"
rating: 2027
created: "2021-09-01T23:15:05+08:00"
updated: "2021-09-01T23:15:05+08:00"
upvotes: 1
comments: 0
---

# 1406. 石子游戏III

> **[yiduobo的每日leetcode 1406.石子游戏III](https://zhuanlan.zhihu.com/p/405928287) · 知乎 · 2021-09-01 · 赞同 1**
> 力扣：[1406. 石子游戏 III](https://leetcode.cn/problems/stone-game-iii/) · Hard · 灵茶山艾府：[三种方法：最大化得分之差 / 最大化个人得分 / 单调队列优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1406.石子游戏III

[力扣](https://leetcode-cn.com/problems/stone-game-iii/)

动态规划的题目，一个直观的想法是令f[i]表示对于剩下的第i到n - 1堆石子时，先手可以取得的最多石子数。

那么对于f[i]，那么有三种情况：

1、先手只选择了stone[i]，那么此时剩下的石头就是第i + 1到n - 1堆，那么此时后手能拿到的最多石子数就是f[i + 1]，因此先手能拿到的石子数，就可以用剩下石子的总数减去后手能拿到的石子数，也就是stone[i + 1] + stone[i + 2] + ... + stone[n - 1] - f[i + 1]，还需要加上一开始选择的stone[i]，因此就有

f[i] \= stone[i] + (stone[i + 1] + ... + stone[n - 1] - f[i + 1])

2、先手选择了stone[i]以及stone[i + 1]，那么与上面类似，后手拿到的最多石子数就是f[i + 2]，因此就有

f[i] \= stone[i] + stone[i + 1] + (stone[i + 2] + ... + stone[n - 1] - f[i + 2])

3、先手选择了stone[i]、stone[i + 1]以及stone[i + 2]，同样地，后手拿到的是f[i + 3]，因此就有

f[i] \= stone[i] + stone[i + 1] + stone[i + 2] + (stone[i + 3] + ... + stone[n - 1] - f[i + 3])

可以发现，去掉括号之后所有的stone项加起来就是

stone[i] + stone[i + 1] + ... + stone[n - 1]

即为stone的后缀和

将其记为s，那么就有

f[i] \= max(s - f[i + 1], s - f[i + 2], s - f[i + 3])

在具体实现时，可以使用记忆化搜索，我选择的是倒过来处理，从最后一块石头开始向前处理，那么上面算法的后缀和s在这里就变成了前缀和。不妨设g为动态规划数组，那么就有

g[i] \= max(s - g[i - 1], s - g[i - 2], s - g[i - 3])

另外，在处理时记得考虑边界的情况

全部计算完毕后，此时先手能拿到的最多石子数就是g[-1]，后手能拿到的就是s - g[ - 1]，只需要对比二者的大小就能确定胜负关系了。

最后附上python代码：

```python
class Solution(object):
    def stoneGameIII(self, stoneValue):
        """
        :type stoneValue: List[int]
        :rtype: str
        """
        
        f = [0]
        s =  0
        for index in range(1, len(stoneValue) + 1):
            s += stoneValue[-index]
            f.append(s - f[-1])
            if index > 1 and f[-1] < s - f[-3]:
                f[-1] = s - f[-3]
            if index > 2 and f[-1] < s - f[-4]:
                f[-1] = s - f[-4]

        if f[-1] > s - f[-1]:
            return "Alice"
        elif f[-1] == s - f[-1]:
            return "Tie"
        else:
            return "Bob"
```
