---
title: "1155. 掷骰子的N种方法"
aliases: ["yiduobo的每日leetcode 1155.掷骰子的N种方法"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/数学算法", "题单/动态规划/三-背包", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378150442"
zhihu_id: "378150442"
zhihu_title: "yiduobo的每日leetcode 1155.掷骰子的N种方法"
question_id: "1155"
question: "掷骰子等于目标和的方法数"
problem_url: "https://leetcode.cn/problems/number-of-dice-rolls-with-target-sum/"
difficulty: "Medium"
rating: 1654
created: "2021-06-05T15:06:13+08:00"
updated: "2021-06-05T15:06:13+08:00"
upvotes: 0
comments: 0
---

# 1155. 掷骰子的N种方法

> **[yiduobo的每日leetcode 1155.掷骰子的N种方法](https://zhuanlan.zhihu.com/p/378150442) · 知乎 · 2021-06-05 · 赞同 0**
> 力扣：[1155. 掷骰子等于目标和的方法数](https://leetcode.cn/problems/number-of-dice-rolls-with-target-sum/) · Medium · 灵茶山艾府：[从记忆化搜索到递推，教你一步步思考动态规划（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1155.掷骰子的N种方法

[力扣](https://leetcode-cn.com/problems/number-of-dice-rolls-with-target-sum/)

经典的动态规划问题，令g[i][j]表示前i个骰子得到总和为j一共有多少种情况，那么对于g[i][j]，当前这一轮可能掷出1到f，因就有

g[i][j] \= sum(g[i - 1][j - k])，其中1 \<\= k \<\= min(f, j)

注意到这里的g每一轮只与上一轮的状态有关，那么我们可以从target向下枚举j，这样就可以优化掉i这一维，于是现在就有

g[j] \= sum(g[j - k])，其中1 \<\= k \<\= min(f, j)

对于sum这一项来说，随着j的移动可以将其视为某种滑动窗口。为了描述情况我们先不考虑边界情况，同时以原始二维的动态规划形式来将括号展开看：

g[i][j] \= g[i - 1][j - 1] + g[i - 1][j - 2] + ... + g[i - 1][j - f]

g[i][j - 1] \= g[i - 1][j - 2] + g[i - 1][j - 3] + ... + g[i - 1][j - f - 1]

对比两个式子可以发现实际上后面的项中减去了g[i - 1][j - 1]然后加上g[i - 1][j - f - 1]，因此在这里可以使用一个变量维护后面这些项的和，然后随着j的移动同步更新这个值。

另外，需要特别注意的是，在二维的情况下最初的g[0][0] \= 1，而g[i][0]在i大于0时则应该等于0，因此在初始化时应该设g[0] \= 1，而首轮动态规划完成之后需要注意更新g[0] \= 0。

最后附上python代码：

```python
class Solution(object):
    def numRollsToTarget(self, d, f, target):
        """
        :type d: int
        :type f: int
        :type target: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        g = [0] * (target + 1)
        g[0] = 1
        for i in range(d):
            now = sum(g[max(0, target - f) : target]) % mod
            for j in range(target, 0, -1):
                g[j] = now
                now -= g[j - 1]
                if j - f - 1 >= 0:
                    now += g[j - f - 1]
                now = (now + mod) % mod
            g[0] = 0
            
        return g[target]
```
