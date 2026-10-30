---
title: "1553. 吃掉N个橘子的最少天数"
aliases: ["yiduobo的每日leetcode 1553.吃掉N个橘子的最少天数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/动态规划", "题单/动态规划/其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426539447"
zhihu_id: "426539447"
zhihu_title: "yiduobo的每日leetcode 1553.吃掉N个橘子的最少天数"
question_id: "1553"
question: "吃掉 N 个橘子的最少天数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-days-to-eat-n-oranges/"
difficulty: "Hard"
rating: 2048
created: "2021-10-27T23:14:44+08:00"
updated: "2021-10-27T23:14:44+08:00"
upvotes: 1
comments: 0
---

# 1553. 吃掉N个橘子的最少天数

> **[yiduobo的每日leetcode 1553.吃掉N个橘子的最少天数](https://zhuanlan.zhihu.com/p/426539447) · 知乎 · 2021-10-27 · 赞同 1**
> 力扣：[1553. 吃掉 N 个橘子的最少天数](https://leetcode.cn/problems/minimum-number-of-days-to-eat-n-oranges/) · Hard · 灵茶山艾府：[两种方法：记忆化搜索/最短路，附证明（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1553.吃掉N个橘子的最少天数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-days-to-eat-n-oranges/)

动态规划的题目，令f[i]表示吃掉i个橘子所需的最少天数，那么很容易写出转移方程：

f[i] \= min(f[i - 1], f[i / 2], f[i / 3]) + 1

这里后续的f[i / 2]的前提条件是i为2的倍数，而f[i / 3]的前提条件则是i为3的倍数。

不过这样做的话，复杂度太高了。将n写成二进制的情况，可以很容易得出答案的上限为2 \* log(n)，但是这样一来会形成3^(2 \* log(n))种状态。即使去掉其中重复的状态，复杂度同样是无法接受的。

仔细分析题目中有三种操作，但是相比除以2和乘以2/3这两种操作，减1这种操作就不太够看的。实际上也很容易证明，不会出现超过两次减1之后接上一个除以2这种情况，因为完全可以在可以除以2时就先除以2。同样地，也不会出现超过3次减一之后接上一个除以3这种情况。换言之，可以认为这里所有的减1都是为除以2和除以3做的铺垫，于是可以调整状态方程：

f[i] \= min(f[i / 2] + i mod 2 + 1, f[i / 3] + i mod 3 +1)

这里的模2和模3表示为除以2和除以3做铺垫的减1操作次数。

最后附上python代码：

```python
class Solution(object):
    def minDays(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = {}
        return self.dfs(n, f)

    def dfs(self, now, f):
        if now not in f:
            if now == 1:
                f[now] = 1
            elif now == 2:
                f[now] = 2
            else:
                f[now] = min(self.dfs(now / 2, f) + 1 + now % 2, self.dfs(now / 3, f) + 1 + now % 3)
        
        return f[now]
```
