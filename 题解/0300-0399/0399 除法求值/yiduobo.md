---
title: "399. 除法求值"
aliases: ["yiduobo的每日leetcode 399.除法求值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/union-find", "leetcode/graph", "leetcode/math", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/七-并查集", "题单/面试经典-150-题/图"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/181712912"
zhihu_id: "181712912"
zhihu_title: "yiduobo的每日leetcode 399.除法求值"
question_id: "399"
question: "除法求值"
problem_url: "https://leetcode.cn/problems/evaluate-division/"
difficulty: "Medium"
created: "2020-08-12T22:25:34+08:00"
updated: "2020-08-12T22:25:34+08:00"
upvotes: 0
comments: 0
---

# 399. 除法求值

> **[yiduobo的每日leetcode 399.除法求值](https://zhuanlan.zhihu.com/p/181712912) · 知乎 · 2020-08-12 · 赞同 0**
> 力扣：[399. 除法求值](https://leetcode.cn/problems/evaluate-division/) · Medium · 灵茶山艾府：[带权并查集（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

399.除法求值<https://leetcode-cn.com/problems/evaluate-division/>

我在这里采用的是图论的思路。对于题目给出的A/B\=k，可以看做是在点A到点B之间有一条有向边，权重为k。不妨设现在需要求解x/y，那么若x和y之间本来就有边，那么可以直接得出答案，否则就从x开始进行dfs，枚举x的邻接点tmp，递归求解tmp/y的值。若可以求出tmp/y的值，那么就通过x/tmp \* tmp/y来得到x/y，否则继续枚举下一个tmp。

过程中可以使用f[x][y]来保存x/y的值来避免重复运算。

最后附上python代码：

```python
class Solution(object):
    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type queries: List[List[str]]
        :rtype: List[float]
        """

        f = {}
        for index in range(len(equations)):
            x, y = equations[index]
            value = values[index]
            if x not in f:
                f[x] = {}
                f[x][x] = 1.0
            if y not in f:
                f[y] = {}
                f[y][y] = 1.0
            f[x][y] = value
            f[y][x] = 1 / value

        used = {}
        for x in f:
            used[x] = False
        
        res = []
        for x, y in queries:
            if x not in f or y not in f:
                res.append(-1.0)
            else:
                used[x] = True
                self.dfs(x, y, f, used)
                used[x] = False
                if y in f[x]:
                    res.append(f[x][y])
                else:
                    res.append(-1.0)

        return res

    def dfs(self, x, y, f, used):
        if y in f[x] or x in f[y]:
            return

        for tmp in f[x]:
            if not used[tmp]:
                used[tmp] = True
                self.dfs(tmp, y, f, used)
                used[tmp] = False
                if y not in f[tmp] and tmp in f[y]:
                    f[tmp][y] = 1 / f[y][tmp]
                if y in f[tmp] and f[tmp][y] > 0:
                    f[x][y] = f[x][tmp] * f[tmp][y]
                    f[y][x] = 1 / f[x][y]
                    return

        return
```
