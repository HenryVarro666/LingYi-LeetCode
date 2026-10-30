---
title: "1219. 黄金矿工"
aliases: ["yiduobo的每日leetcode 1219.黄金矿工"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383053176"
zhihu_id: "383053176"
zhihu_title: "yiduobo的每日leetcode 1219.黄金矿工"
question_id: "1219"
question: "黄金矿工"
problem_url: "https://leetcode.cn/problems/path-with-maximum-gold/"
created: "2021-06-22T22:12:25+08:00"
updated: "2021-06-22T22:12:25+08:00"
upvotes: 0
comments: 0
---

# 1219. 黄金矿工

> **[yiduobo的每日leetcode 1219.黄金矿工](https://zhuanlan.zhihu.com/p/383053176) · 知乎 · 2021-06-22 · 赞同 0**
> 力扣：[1219. 黄金矿工](https://leetcode.cn/problems/path-with-maximum-gold/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1219.黄金矿工

[力扣](https://leetcode-cn.com/problems/path-with-maximum-gold/)

没有想出什么比较好的多项式算法，由于有25个格子因此使用状态压缩动态规划也不太适用，于是使用朴素的dfs试试看。

首先扫描grid，对于每块黄金都进行编号，然后若两块黄金相连，那么就在图中给这两个点连上一条边。扫描完毕后，就能得到一张最多25个点的无向图。

接下来枚举起点，然后从起点开始进行dfs即可。

虽然dfs理论上的复杂度可以到O(n!)，n表示黄金的数量，但是实际上由于grid是网格状，因此最终得到的无向图是很稀疏的图，因此复杂度应该不是太高。

最后附上python代码:

```python
class Solution(object):
    def getMaximumGold(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        g = {}
        v = []
        cnt = 0
        num_dict = {}
        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    g[cnt] = set()
                    num_dict[(i, j)] = cnt
                    v.append(grid[i][j])
                    if i > 0 and grid[i - 1][j] > 0:
                        p = num_dict[(i - 1, j)]
                        g[p].add(cnt)
                        g[cnt].add(p)
                    if j > 0 and grid[i][j - 1] > 0:
                        p = num_dict[(i, j - 1)]
                        g[p].add(cnt)
                        g[cnt].add(p)
                    cnt += 1
        
        used = [False] * cnt
        res = 0
        for index in range(cnt):
            used[index] = True
            res = max(res, self.dfs(index, used, g, v))
            used[index] = False
        return res

    def dfs(self, now, used, g, v):
        max_next = 0
        for next in g[now]:
            if not used[next]:
                used[next] = True
                end_flag = False
                max_next = max(max_next, self.dfs(next, used, g, v))
                used[next] = False
        
        return max_next + v[now]
```
