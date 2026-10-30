---
title: "1872. 石子游戏VIII"
aliases: ["yiduobo的每日leetcode 1872.石子游戏VIII"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/game-theory", "leetcode/prefix-sum", "题单/动态规划", "题单/数学算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/475560309"
zhihu_id: "475560309"
zhihu_title: "yiduobo的每日leetcode 1872.石子游戏VIII"
question_id: "1872"
question: "石子游戏 VIII"
problem_url: "https://leetcode.cn/problems/stone-game-viii/"
difficulty: "Hard"
rating: 2440
created: "2022-03-04T02:55:25+08:00"
updated: "2022-03-04T02:55:26+08:00"
upvotes: 0
comments: 0
---

# 1872. 石子游戏VIII

> **[yiduobo的每日leetcode 1872.石子游戏VIII](https://zhuanlan.zhihu.com/p/475560309) · 知乎 · 2022-03-04 · 赞同 0**
> 力扣：[1872. 石子游戏 VIII](https://leetcode.cn/problems/stone-game-viii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1872.石子游戏VIII

[力扣](https://leetcode-cn.com/problems/stone-game-viii/)

可以发现，玩家每次都是拿走了石子的某个前缀，然后另一名玩家则只能从前一名玩家拿石子位置后面的某个位置拿，同样也是拿走石子的某个前缀，以此类推。

那么在这里，肯定是需要先把石子的前缀和s计算出来的，接下来则可以尝试倒推。令f[i]表示当前必须从第i个石子开始拿时先手与后手的最大分差，那么：

1、首先是边界情况，先手可以一次性全部拿掉，因此就有f[n - 1] \= s[n - 1]

2、接下来考虑一般情况。对于f[i]，有两种选择。

第一种是拿走到i为止的前缀，那么此时后手可以拿走从i + 1开始的前缀。先手拿走到i为止的前缀的收益是s[i]，而后手从i + 1开始拿，最终将比先手多得到f[i + 1]分，因此最终就有f[i] \= s[i] - f[i + 1]

第二种则是不选择拿走到i位置的后缀，那么这种情况完全可以视为从i + 1开始拿，此时就有f[i] \= f[i + 1]

综合起来，就是f[i] \= max(f[i + 1], s[i] - f[i + 1])

根据上面的式子从后向前倒推直到求出f[1]位置。需要注意的是，这里答案是f[1]而不是f[0]的原因是题目规定了先手不能只拿最前面的石头。

最后附上python代码：

```python
class Solution(object):
    def stoneGameVIII(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """

        s = [stones[0]]
        for stone in stones[1:]:
            s.append(s[-1] + stone)

        f = [s[-1]]
        for p in s[-2::-1]:
            f.append(f[-1])
            f[-1] = max(f[-1], p - f[-1])
        
        return f[-2]
```
