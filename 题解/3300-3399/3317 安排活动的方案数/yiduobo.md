---
title: "3317. 安排活动的方案数"
aliases: ["yiduobo的每日leetcode 3317.安排活动的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2033744491"
zhihu_id: "2033744491"
zhihu_title: "yiduobo的每日leetcode 3317.安排活动的方案数"
question_id: "3317"
question: "安排活动的方案数"
problem_url: "https://leetcode.cn/problems/find-the-number-of-possible-ways-for-an-event/"
difficulty: "Hard"
rating: 2414
created: "2024-10-19T22:28:31+08:00"
updated: "2024-10-19T22:28:31+08:00"
upvotes: 0
comments: 0
---

# 3317. 安排活动的方案数

> **[yiduobo的每日leetcode 3317.安排活动的方案数](https://zhuanlan.zhihu.com/p/2033744491) · 知乎 · 2024-10-19 · 赞同 0**
> 力扣：[3317. 安排活动的方案数](https://leetcode.cn/problems/find-the-number-of-possible-ways-for-an-event/) · Hard · 灵茶山艾府：[组合数学：第二类斯特林数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3317.安排活动的方案数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-possible-ways-for-an-event/)

题目给出三个整数n、x和y，其中n表示一个活动共有n位表演者，x表示一共有x个节点。每个表演者都需要被安排到一个节目中，但是并不是所有节目都需要安排表演者。

表演完毕之后，将有评委给有表演者的节目打分，分数为1到y之间的整数。问总的活动方案数是多少。

若两个活动方案满足以下条件之一，那么就视为不同的活动：

1、存在一个表演者在不同的节目中表演

2、存在一个节目的分数不同

看题面就是组合数学的题目，按照题意，这里的表演者是有区分的，节目也是有区分的，那么在这里可以先从这x个节目中选出前k个节目，然后计算将人分配进去的方案数，再乘上打分方案数就是所有恰好有k个人表演的总方案数了。

需要注意的是，由于节目有区分，因此选出前k个节目是排列而不是组合，对应的方案数是A(x, k)。

接下来需要计算将n个人分配到这k个节目中，要求每个节目都有人的方案数。需要特别注意的是，由于在上一步已经枚举了k个节目的排列，因此在这一步里面应该将这k个节目视为相同的节目。

不过由于人还是有区别的，因此在这里直接用组合数学计算依然不太方便，涉及到的去重会非常麻烦，因此可以考虑使用动态规划计算。

令f[i][j]表示将前i个人分配到j个节目中，且每个节目都有人的分配方案数，那么对于f[i][j]，若j \= 1，那么所有人都只能参与这个节目，那么就有f[i][j] \= 1，而对于j > 1的情况，可以考虑前i - 1个人的分配情况。若前i - 1个人只被分配到j - 1个节目中，那么第i个人只能分配到剩下的那个节目，对应的就是f[i - 1][j - 1]；若前i个人分配到了所有的j个节目中，那么第i个人可以任选节目，对应的就是f[i - 1][j] \* j；对于其他情况，至少有两个无人的节目，此时i无论如何分配，都无法满足所有节目都有人，因此对应的可行方案为0。

综合起来就是f[i][j] \= f[i - 1][j - 1] + f[i - 1][j] \* j

最后对于这k个节目，每个节目的得分在1到y之间，因此一共有y^k种打分分布。

以上三者相乘，就是恰好有k个节目有人表演的总方案数了。只需从1到x枚举有人表演的节目数k，按上面的方法计算即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, n, x, y):
        """
        :type n: int
        :type x: int
        :type y: int
        :rtype: int
        """
        
        mod = 10 ** 9 + 7
        
        f = [[0] * (x + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i in range(1, n + 1):
            for j in range(1, x + 1):
                f[i][j] = (f[i - 1][j - 1] + f[i - 1][j] * j) % mod

        score = 1
        a = 1
        res = 0
        for i in range(1, x + 1):
            a = a * (x - i + 1) % mod
            score = score * y % mod
            res = (res + a * f[n][i] % mod * score % mod) % mod
        
        return res
```
