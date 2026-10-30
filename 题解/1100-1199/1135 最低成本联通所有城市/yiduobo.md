---
title: "1135. 最低成本联通所有城市"
aliases: ["yiduobo的每日leetcode 1135.最低成本联通所有城市"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610558553"
zhihu_id: "610558553"
zhihu_title: "yiduobo的每日leetcode 1135.最低成本联通所有城市"
question_id: "1135"
question: "最低成本联通所有城市"
problem_url: "https://leetcode.cn/problems/connecting-cities-with-minimum-cost/"
created: "2023-03-01T21:38:03+08:00"
updated: "2023-03-01T21:38:03+08:00"
upvotes: 0
comments: 0
---

# 1135. 最低成本联通所有城市

> **[yiduobo的每日leetcode 1135.最低成本联通所有城市](https://zhuanlan.zhihu.com/p/610558553) · 知乎 · 2023-03-01 · 赞同 0**
> 力扣：[1135. 最低成本联通所有城市](https://leetcode.cn/problems/connecting-cities-with-minimum-cost/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1135.最低成本连通所有城市

[力扣](https://leetcode.cn/problems/connecting-cities-with-minimum-cost/)

非常标准的最小生成树问题，常规的处理方法有prim算法以及kruskal算法。我在这里使用的是后者。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, n, connections):
        """
        :type n: int
        :type connections: List[List[int]]
        :rtype: int
        """

        fa = range(n)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = 0
        linked = 0
        for x, y, cost in sorted(connections, key=lambda d:d[2]):
            fa_x = find(x - 1)
            fa_y = find(y - 1)
            if fa_x != fa_y:
                fa[fa_x] = fa_y
                linked += 1
                res += cost
                if linked == n - 1:
                    return res
        
        return -1
```
