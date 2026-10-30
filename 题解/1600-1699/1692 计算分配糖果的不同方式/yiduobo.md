---
title: "1692. 计算分配糖果的不同方式"
aliases: ["yiduobo的每日leetcode 1692.计算分配糖果的不同方式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/619999006"
zhihu_id: "619999006"
zhihu_title: "yiduobo的每日leetcode 1692.计算分配糖果的不同方式"
question_id: "1692"
question: "计算分配糖果的不同方式"
problem_url: "https://leetcode.cn/problems/count-ways-to-distribute-candies/"
created: "2023-04-07T00:45:37+08:00"
updated: "2023-04-07T00:45:37+08:00"
upvotes: 0
comments: 0
---

# 1692. 计算分配糖果的不同方式

> **[yiduobo的每日leetcode 1692.计算分配糖果的不同方式](https://zhuanlan.zhihu.com/p/619999006) · 知乎 · 2023-04-07 · 赞同 0**
> 力扣：[1692. 计算分配糖果的不同方式](https://leetcode.cn/problems/count-ways-to-distribute-candies/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1692.计算分配糖果的不同方式

[力扣](https://leetcode.cn/problems/count-ways-to-distribute-candies/)

题目实际上就是要求将n个不同的球放入m个相同的盒子里，问一共有多少种放的方法。这是非常经典的组合数学问题，比较官方的名称是第二类斯特林数。

令f[i][j]表示将i个不同的球放入j个相同盒子中的方案数，那么对于f[i][j]，不妨考虑最后一个球：

1、最后这个球放在之前已经放过球的盒子中，那么就是f[i - 1][j] \* j种可能的方案

2、最后这个求放在一个新的盒子中，那么就是f[i - 1][j - 1]种可能的方案

综合上面两种情况，就有

f[i][j] \= f[i - 1][j] \* j + f[i - 1][j - 1]

上面动态规划算法成立的理由是各个盒子间以及盒子内部的球的编号的顺序是无关紧要的，那么为了避免重复计算，在这里就可以将每个盒子中按编号最小的球的编号排列好，同时将每个盒子内部的球按从小到大的顺序排列好，那么到了上面f[i][j]描述的第i个球，就只有上面描述的放置方案了。

最后附上python代码：

```python
class Solution(object):
    def waysToDistribute(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        mod = 10 ** 9 + 7
        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                f[i][j] = f[i - 1][j] * j + f[i - 1][j - 1]
                f[i][j] %= mod
        
        return f[-1][-1]
```
