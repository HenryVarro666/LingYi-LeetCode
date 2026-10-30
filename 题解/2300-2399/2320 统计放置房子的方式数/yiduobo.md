---
title: "2320. 统计放置房子的方式数"
aliases: ["yiduobo的每日leetcode 2320.统计放置房子的方式数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557091265"
zhihu_id: "557091265"
zhihu_title: "yiduobo的每日leetcode 2320.统计放置房子的方式数"
question_id: "2320"
question: "统计放置房子的方式数"
problem_url: "https://leetcode.cn/problems/count-number-of-ways-to-place-houses/"
difficulty: "Medium"
rating: 1608
created: "2022-08-23T23:10:21+08:00"
updated: "2022-08-23T23:10:21+08:00"
upvotes: 0
comments: 0
---

# 2320. 统计放置房子的方式数

> **[yiduobo的每日leetcode 2320.统计放置房子的方式数](https://zhuanlan.zhihu.com/p/557091265) · 知乎 · 2022-08-23 · 赞同 0**
> 力扣：[2320. 统计放置房子的方式数](https://leetcode.cn/problems/count-number-of-ways-to-place-houses/) · Medium · 灵茶山艾府：[线性 DP（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2320.统计放置房子的方式数

[力扣](https://leetcode.cn/problems/count-number-of-ways-to-place-houses/)

首先，马路两侧的房子是互不影响的，不妨设其中一侧的放置方案数有k种，那么总的放置方案数就是k \* k。

接下来需要想办法计算马路单侧放置房子的方案数。令f[i]表示马路一侧前i个格子可以放置的房子数目，那么对于f[i]：

1、在第i个位置可以不放置房子，那么此时可以沿用f[i - 1]中的任意方案

2、在第i个位置如果要放置房子，那么在第i - 1个位置就不能放置房子，此时则可以沿用f[i - 2]中的任意方案

综合起来就是f[i] \= f[i - 1] + f[i - 2]

于是只需要一趟遍历计算出f[n]，最终答案就是f[n] \* f[n]

注意到这里的f只与前两轮的状态有关，因此可以使用变量来滚动，不需要使用数组。另外在这里也可以使用矩阵乘法进行优化。

最后附上python代码：

```python
class Solution(object):
    def countHousePlacements(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 4
        elif n == 2:
            return 9
        else:
            a, b = 2, 3
            mod = 10 ** 9 + 7
            for index in range(2, n):
                a, b = b, (a + b) % mod

            return b * b % mod
```
