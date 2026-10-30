---
title: "886. 可能的二分法"
aliases: ["yiduobo的每日leetcode 886.可能的二分法"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/图论算法", "题单/图论算法/七-二分图染色"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351756347"
zhihu_id: "351756347"
zhihu_title: "yiduobo的每日leetcode 886.可能的二分法"
question_id: "886"
question: "可能的二分法"
problem_url: "https://leetcode.cn/problems/possible-bipartition/"
difficulty: "Medium"
rating: 1795
created: "2021-02-20T20:56:52+08:00"
updated: "2021-02-20T20:56:52+08:00"
upvotes: 0
comments: 0
---

# 886. 可能的二分法

> **[yiduobo的每日leetcode 886.可能的二分法](https://zhuanlan.zhihu.com/p/351756347) · 知乎 · 2021-02-20 · 赞同 0**
> 力扣：[886. 可能的二分法](https://leetcode.cn/problems/possible-bipartition/) · Medium · 灵茶山艾府：[【模板】二分图染色（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

886.可能的二分法

[力扣](https://leetcode-cn.com/problems/possible-bipartition/)

如果把题目中的每个人看做图中的点，然后在存在dislike关系的两个人之间连上一条边，那么问题就转化成了判断这个图是否为二分图。对于二分图的判定，经典的做法就是01染色。对于当前节点，设其颜色为now，枚举其连接的所有节点：

1、若该节点无色，那么将该节点染成1 - now，然后对当前节点进行递归染色

2、若该节点颜色与当前节点相同，说明这张图不是二分图，返回false

3、若该节点与当前节点颜色不同，那么跳过该节点

最后附上python代码：

```python
class Solution(object):
    def possibleBipartition(self, N, dislikes):
        """
        :type N: int
        :type dislikes: List[List[int]]
        :rtype: bool
        """

        g = {}
        for x, y in dislikes:
            x -= 1
            y -= 1
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        color = [None] * N
        for x in range(N):
            if color[x] is None:
                color[x] = 0
                if not self.dfs(x, 0, g, color):
                    return False

        return True

    def dfs(self, x, now, g, color):
        for y in g.get(x, set()):
            if color[y] is None:
                color[y] = 1 - now
                if not self.dfs(y, 1 - now, g, color):
                    return False
            elif color[y] == color[x]:
                return False
        
        return True
```
