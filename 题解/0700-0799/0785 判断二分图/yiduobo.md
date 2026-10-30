---
title: "785. 判断二分图"
aliases: ["yiduobo的每日leetcode 785.判断二分图"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "题单/图论算法", "题单/图论算法/七-二分图染色"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341099588"
zhihu_id: "341099588"
zhihu_title: "yiduobo的每日leetcode 785.判断二分图"
question_id: "785"
question: "判断二分图"
problem_url: "https://leetcode.cn/problems/is-graph-bipartite/"
difficulty: "Medium"
rating: 1625
created: "2020-12-31T20:27:12+08:00"
updated: "2020-12-31T20:27:12+08:00"
upvotes: 0
comments: 0
---

# 785. 判断二分图

> **[yiduobo的每日leetcode 785.判断二分图](https://zhuanlan.zhihu.com/p/341099588) · 知乎 · 2020-12-31 · 赞同 0**
> 力扣：[785. 判断二分图](https://leetcode.cn/problems/is-graph-bipartite/) · Medium · 灵茶山艾府：[【图解】交替染色法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

785.判断二分图

[力扣](https://leetcode-cn.com/problems/is-graph-bipartite/)

经典的判断二分图问题，常见的做法是对图中每个点进行01染色。简单来说就是将二分图左边的部分全部置为0，将右边的部分全部置为1，那么可以发现，任意相邻的两点颜色都不一样。

具体的染色算法为遍历每个点，若当前点now还没有被染色，那么将其染色为0，然后从该点开始往相邻的点进行dfs。对于相邻的点next，有三种可能的染色情况：

1、now和next的颜色一样，此时出现了同色的相邻点，说明这张图不是二分图

2、now和next的颜色相反，此时跳过next考虑下一个点

3、next无色，此时则需要将next置为now的反色，然后从next开始继续dfs

最后附上python代码：

```python
class Solution(object):
    def isBipartite(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: bool
        """

        n = len(graph)
        color = [None] * n
        for x in range(n):
            if color[x] is None:
                if not self.dfs(x, color, 0, graph):
                    return False

        return True

    def dfs(self, now, color, c, graph):
        color[now] = c
        for next in graph[now]:
            if color[next] == color[now]:
                return False
            if color[next] is None:
                if not self.dfs(next, color, 1 - c, graph):
                    return False
        return True
```
