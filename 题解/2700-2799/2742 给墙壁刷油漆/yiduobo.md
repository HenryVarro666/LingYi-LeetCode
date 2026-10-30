---
title: "2742. 给墙壁刷油漆"
aliases: ["yiduobo的每日leetcode 2742.给墙壁刷油漆"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653405236"
zhihu_id: "653405236"
zhihu_title: "yiduobo的每日leetcode 2742.给墙壁刷油漆"
question_id: "2742"
question: "给墙壁刷油漆"
problem_url: "https://leetcode.cn/problems/painting-the-walls/"
difficulty: "Hard"
rating: 2425
created: "2023-08-31T02:44:08+08:00"
updated: "2023-08-31T02:44:08+08:00"
upvotes: 0
comments: 0
---

# 2742. 给墙壁刷油漆

> **[yiduobo的每日leetcode 2742.给墙壁刷油漆](https://zhuanlan.zhihu.com/p/653405236) · 知乎 · 2023-08-31 · 赞同 0**
> 力扣：[2742. 给墙壁刷油漆](https://leetcode.cn/problems/painting-the-walls/) · Hard · 灵茶山艾府：[两种方法：状态优化 / 转换成 0-1 背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2742.给墙壁刷油漆

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/painting-the-walls/)

雇佣一位花费为cost[i]的粉刷匠可以工作time[i]的时间，也就是可以白嫖刷掉time[i]堵墙。换言之，雇佣这位粉刷匠相当于使用cost[i]来刷掉time[i] + 1堵墙，那么到了这里，问题就可以转化成背包问题了。不过与常规背包问题不同的是，本题中的物品大小是可以超出背包大小的，因此需要对这些情况进行特殊处理。

令f[i][j]表示前i种付费方案，刷掉j堵墙所需的最小花销，那么对于f[i][j]，首先可以直接跳过cost[i]这种方案，于是可以初始化f[i][j] \= f[i - 1][j]。

接下来考虑time[i] + 1与j的关系。若time[i] + 1 >\= j，此时只需采用cost[i]这一个方案就可以刷掉全部的j堵墙，于是就有f[i][j] \= min(f[i][j], cost[i])，否则就有f[i][j] \= min(f[i][j], f[i - 1][j - (time[i] + 1)] + cost[i])。

另外，注意到f的每一轮只与上一轮有关，因此可以通过倒序计算省略掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def paintWalls(self, cost, time):
        """
        :type cost: List[int]
        :type time: List[int]
        :rtype: int
        """

        n = len(cost)
        f = [None] * (n + 1)
        f[0] = 0
        res = None
        for c, t in zip(cost, time):
            if t + 1 >= n:
                if f[n] is None or f[n] > c:
                    f[n] = c
            else:
                for index in range(n, t, -1):
                    if f[index - (t + 1)] is not None and (f[index] is None or f[index] > f[index - (t + 1)] + c):
                        f[index] = f[index - (t + 1)] + c
                for index in range(t, 0, -1):
                    if f[index] is None or f[index] > c:
                        f[index] = c

        return f[-1]
```
