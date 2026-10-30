---
title: "787. K站中转内最便宜的航班"
aliases: ["yiduobo的每日leetcode 787.K站中转内最便宜的航班"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341216117"
zhihu_id: "341216117"
zhihu_title: "yiduobo的每日leetcode 787.K站中转内最便宜的航班"
question_id: "787"
question: "K站中转内最便宜的航班"
problem_url: "https://leetcode.cn/problems/cheapest-flights-within-k-stops/"
created: "2021-01-01T14:28:14+08:00"
updated: "2021-01-01T14:28:14+08:00"
upvotes: 0
comments: 0
---

# 787. K站中转内最便宜的航班

> **[yiduobo的每日leetcode 787.K站中转内最便宜的航班](https://zhuanlan.zhihu.com/p/341216117) · 知乎 · 2021-01-01 · 赞同 0**
> 力扣：[787. K站中转内最便宜的航班](https://leetcode.cn/problems/cheapest-flights-within-k-stops/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

787.K站中转内最便宜的航班

[力扣](https://leetcode-cn.com/problems/cheapest-flights-within-k-stops/)

看上去应该是可以用类似spfa的做法来做，不过可能有些细节需要想清楚。简单起见我在这里还是采用的动态规划的做法，f[i][x]表示从起点开始走i步，走到节点x的最低价格，边界条件自然是f[0][src] \= 0。

接下来从0开始计算每一轮的状态，一共需要执行k轮。设当前执行到第i轮，那么枚举第i - 1轮的所有状态，对于f[i - 1][x]，枚举所有以x为起点的边，设这条边的终点为y，那么我们此时可以从x走过去，即

f[i][y] \= min(f[i][y], f[i - 1][x] + dis(x, y))

若y为终点，则需要考察f[i][y]是否小于当前答案。

最后附上python代码：

```python
class Solution(object):
    def findCheapestPrice(self, n, flights, src, dst, K):
        """
        :type n: int
        :type flights: List[List[int]]
        :type src: int
        :type dst: int
        :type K: int
        :rtype: int
        """

        g = {}
        for x, y, v in flights:
            if x not in g:
                g[x] = {}
            g[x][y] = v

        f = [[None] * n for _ in range(K + 2)]
        f[0][src] = 0
        res = None
        for i in range(1, K + 2):
            for x in range(n):
                if f[i - 1][x] is not None:
                    for y in g.get(x, {}):
                        if f[i][y] is None or f[i][y] > f[i - 1][x] + g[x][y]:
                            f[i][y] = f[i - 1][x] + g[x][y]
                            if y == dst:
                                if res is None or res > f[i][y]:
                                    res = f[i][y]
        

        if res is None:
            return -1
        
        return res
```
