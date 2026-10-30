---
title: "1615. 最大网络秩"
aliases: ["yiduobo的每日leetcode 1615.最大网络秩"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435442548"
zhihu_id: "435442548"
zhihu_title: "yiduobo的每日leetcode 1615.最大网络秩"
question_id: "1615"
question: "最大网络秩"
problem_url: "https://leetcode.cn/problems/maximal-network-rank/"
created: "2021-11-19T22:42:56+08:00"
updated: "2021-11-19T22:42:56+08:00"
upvotes: 0
comments: 0
---

# 1615. 最大网络秩

> **[yiduobo的每日leetcode 1615.最大网络秩](https://zhuanlan.zhihu.com/p/435442548) · 知乎 · 2021-11-19 · 赞同 0**
> 力扣：[1615. 最大网络秩](https://leetcode.cn/problems/maximal-network-rank/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1615.最大网络秩

[力扣](https://leetcode-cn.com/problems/maximal-network-rank/)

由于题目点的规模非常小，因此可以直接记录每个点的度以及点对之间相连的情况，然后两两枚举点对。若两个点相连，那么此时的秩就是这两个点度的和减1，若不相连那么就是这两个点度的和。其中最大值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximalNetworkRank(self, n, roads):
        """
        :type n: int
        :type roads: List[List[int]]
        :rtype: int
        """

        g = [[0] * n for _ in range(n)]
        s = [0] * n
        for x, y in roads:
            g[x][y] = 1
            g[y][x] = 1
            s[x] += 1
            s[y] += 1

        res = 0
        for x in range(n - 1):
            for y in range(x + 1, n):
                res = max(res, s[x] + s[y] - g[x][y])
        
        return res
```
