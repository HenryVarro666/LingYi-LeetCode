---
title: "LCP 07. 传递信息"
aliases: ["yiduobo的每日leetcode LCP07.传递信息"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570676466"
zhihu_id: "570676466"
zhihu_title: "yiduobo的每日leetcode LCP07.传递信息"
question_id: "LCP 07"
question: "传递信息"
problem_url: "https://leetcode.cn/problems/chuan-di-xin-xi/"
created: "2022-10-05T03:29:43+08:00"
updated: "2022-10-05T03:29:43+08:00"
upvotes: 1
comments: 0
---

# LCP 07. 传递信息

> **[yiduobo的每日leetcode LCP07.传递信息](https://zhuanlan.zhihu.com/p/570676466) · 知乎 · 2022-10-05 · 赞同 1**
> 力扣：[LCP 07. 传递信息](https://leetcode.cn/problems/chuan-di-xin-xi/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP07.传递信息

[力扣](https://leetcode.cn/problems/chuan-di-xin-xi/)

题目给出一张有向图，求图中从节点0到节点n - 1，且长度为k的路径条数。这里的路径可以重复经过某个节点。

由于题目的数据规模非常小，直接暴力枚举每一条传递路径应该是可行的。

我在这里采用的是动态规划的做法，令f[i][j]表示长度为i，终点为j的所有可行路径条数。对于f[i][j]，可以认为从某条长度为i - 1的路径终点再走一步来到j，因此就有f[i][j] \= sum(f[i - 1][k])，其中k为所有存在到j的边的节点。

注意到每一类的状态只与上一轮有关，那么就可以通过滚动数组省略掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def numWays(self, n, relation, k):
        """
        :type n: int
        :type relation: List[List[int]]
        :type k: int
        :rtype: int
        """

        m = {}
        for x, y in relation:
            if x not in m:
                m[x] = set()
            m[x].add(y)
        
        f = [0] * n
        f[0] = 1
        for _ in range(k):
            g = [0] * n
            for x in range(n):
                if f[x] > 0:
                    for y in m.get(x, set()):
                        g[y] += f[x]
            f = g[:]
        
        return f[-1]
```
