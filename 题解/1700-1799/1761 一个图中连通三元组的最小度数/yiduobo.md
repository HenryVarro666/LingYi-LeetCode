---
title: "1761. 一个图中连通三元组的最小度数"
aliases: ["yiduobo的每日leetcode 1761.一个图中连通三元组的最小度数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460083118"
zhihu_id: "460083118"
zhihu_title: "yiduobo的每日leetcode 1761.一个图中连通三元组的最小度数"
question_id: "1761"
question: "一个图中连通三元组的最小度数"
problem_url: "https://leetcode.cn/problems/minimum-degree-of-a-connected-trio-in-a-graph/"
created: "2022-01-20T23:38:08+08:00"
updated: "2022-01-20T23:38:08+08:00"
upvotes: 0
comments: 0
---

# 1761. 一个图中连通三元组的最小度数

> **[yiduobo的每日leetcode 1761.一个图中连通三元组的最小度数](https://zhuanlan.zhihu.com/p/460083118) · 知乎 · 2022-01-20 · 赞同 0**
> 力扣：[1761. 一个图中连通三元组的最小度数](https://leetcode.cn/problems/minimum-degree-of-a-connected-trio-in-a-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1761.一个图中连通三元组的最小度数

[力扣](https://leetcode-cn.com/problems/minimum-degree-of-a-connected-trio-in-a-graph/)

没有什么特别好的想法，不过好在数据规模有限，因此可以直接暴力求解。枚举三个点i、j、k，若三者两两相连，那么最终度数就等于d[i] + d[j] + d[k] - 6，其中d[i]表示i这个节点的度数，而减6的原因是三个点之间两两相连的边，一共3条边会提供6的度数，因此需要减去6。

最后附上python代码：

```python
class Solution(object):
    def minTrioDegree(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        if n < 3:
            return -1

        d = [0] * n
        f = [[False] * n for _ in range(n)]
        for x, y in edges:
            x -= 1
            y -= 1
            d[x] += 1
            d[y] += 1
            f[x][y] = f[y][x] = True
            
        res = n * 3
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                if f[i][j] and d[i] + d[j] - 4 < res:
                    for k in range(j + 1, n):
                        if f[i][k] and f[j][k] and d[i] + d[j] + d[k] - 6 < res:
                            res = min(d[i] + d[j] + d[k] - 6, res)

        if res == n * 3:
            res = -1
        
        return res
```
