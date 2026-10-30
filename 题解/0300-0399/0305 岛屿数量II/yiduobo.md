---
title: "305. 岛屿数量II"
aliases: ["yiduobo的每日leetcode 305.岛屿数量II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595784585"
zhihu_id: "595784585"
zhihu_title: "yiduobo的每日leetcode 305.岛屿数量II"
question_id: "305"
question: "岛屿数量II"
problem_url: "https://leetcode.cn/problems/number-of-islands-ii/"
created: "2023-01-01T02:50:00+08:00"
updated: "2023-01-01T02:50:00+08:00"
upvotes: 0
comments: 0
---

# 305. 岛屿数量II

> **[yiduobo的每日leetcode 305.岛屿数量II](https://zhuanlan.zhihu.com/p/595784585) · 知乎 · 2023-01-01 · 赞同 0**
> 力扣：[305. 岛屿数量II](https://leetcode.cn/problems/number-of-islands-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

305.岛屿数量II

[力扣](https://leetcode.cn/problems/number-of-islands-ii/)

题目相当于在无向图不断往其中加入边，问每次加入边之后当前连通块的数量。对于这类加边判连通的问题，常见的做法是利用并查集来维护连通性。

对于本题，每当一个格子转换成陆地时，若这个格子之前是水域，那么就应该将当前连通块的数量now加上1。接下来，对于与当前格子相邻的四个格子，若这些格子是陆地，且属于其他的连通块，那么就需要将对应的连通块合并至当前格子所在的连通块，同时将now减去1。处理完合并操作后，就可以将now加入到答案中，然后继续处理下一个需要转换的格子了。

最后附上python代码：

```python
class Solution(object):
    def numIslands2(self, m, n, positions):
        """
        :type m: int
        :type n: int
        :type positions: List[List[int]]
        :rtype: List[int]
        """

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        fa = {}

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = []
        now = 0
        for x, y in positions:
            v = x * n + y
            if v not in fa:
                fa[v] = v
                now += 1

                for index in range(4):
                    xx = x + dx[index]
                    yy = y + dy[index]
                    if xx >= 0 and xx < m and yy >= 0 and yy < n:
                        vv = xx * n + yy
                        if vv in fa:
                            fa_vv = find(vv)
                            if fa_vv != v:
                                fa[fa_vv] = v
                                now -= 1
            res.append(now)
        
        return res
```
