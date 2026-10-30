---
title: "1334. 阈值距离内邻居最少的城市"
aliases: ["yiduobo的每日leetcode 1334.阈值距离内邻居最少的城市"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/395228293"
zhihu_id: "395228293"
zhihu_title: "yiduobo的每日leetcode 1334.阈值距离内邻居最少的城市"
question_id: "1334"
question: "阈值距离内邻居最少的城市"
problem_url: "https://leetcode.cn/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/"
difficulty: "Medium"
rating: 1855
created: "2021-08-01T19:53:47+08:00"
updated: "2021-08-01T19:53:47+08:00"
upvotes: 1
comments: 0
---

# 1334. 阈值距离内邻居最少的城市

> **[yiduobo的每日leetcode 1334.阈值距离内邻居最少的城市](https://zhuanlan.zhihu.com/p/395228293) · 知乎 · 2021-08-01 · 赞同 1**
> 力扣：[1334. 阈值距离内邻居最少的城市](https://leetcode.cn/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) · Medium · 灵茶山艾府：[带你发明 Floyd 算法：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1334.阈值距离内邻居最少的城市

[力扣](https://leetcode-cn.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)

题目需要知道对于每一个城市而言，与其距离小于等于threshold的城市的数目，因此我们需要首先知道每个城市两两之间的距离，那么可以先使用经典的弗洛伊德算法求解出城市两两之间的距离，然后对于每个城市，统计与其距离在threshold之内的其他城市的数目，并从中选出最小值对应的城市即可。

最后附上python代码：

```python
class Solution(object):
    def findTheCity(self, n, edges, distanceThreshold):
        """
        :type n: int
        :type edges: List[List[int]]
        :type distanceThreshold: int
        :rtype: int
        """

        f = [[None] * n for _ in range(n)]
        for index in range(n):
            f[index][index] = 0
        for x, y, dis in edges:
            f[x][y] = dis
            f[y][x] = dis
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if f[i][k] is not None and f[k][j] is not None:
                        if f[i][j] is None or f[i][j] > f[i][k] + f[k][j]:
                            f[i][j] = f[i][k] + f[k][j]
        
        min_cnt = n
        res = None
        for i in range(n):
            cnt = 0
            for j in range(n):
                if i == j:
                    continue
                if f[i][j] > distanceThreshold:
                    continue
                cnt += 1
            
            if cnt <= min_cnt:
                min_cnt = cnt
                res = i
        
        return res
```
