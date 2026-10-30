---
title: "1971. 寻找图中是否存在路径"
aliases: ["yiduobo的每日leetcode 1971.寻找图中是否存在路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/495827548"
zhihu_id: "495827548"
zhihu_title: "yiduobo的每日leetcode 1971.寻找图中是否存在路径"
question_id: "1971"
question: "寻找图中是否存在路径"
problem_url: "https://leetcode.cn/problems/find-if-path-exists-in-graph/"
created: "2022-04-09T20:25:32+08:00"
updated: "2022-04-09T20:25:32+08:00"
upvotes: 0
comments: 0
---

# 1971. 寻找图中是否存在路径

> **[yiduobo的每日leetcode 1971.寻找图中是否存在路径](https://zhuanlan.zhihu.com/p/495827548) · 知乎 · 2022-04-09 · 赞同 0**
> 力扣：[1971. 寻找图中是否存在路径](https://leetcode.cn/problems/find-if-path-exists-in-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1971.寻找图中是否存在路径

[力扣](https://leetcode-cn.com/problems/find-if-path-exists-in-graph/)

比较基础的题目，有各式各样的方法。我在这里采用的是从start开始进行bfs，判断能否走到end。

最后附上python代码：

```python
class Solution(object):
    def validPath(self, n, edges, source, destination):
        """
        :type n: int
        :type edges: List[List[int]]
        :type source: int
        :type destination: int
        :rtype: bool
        """

        if source == destination:
            return True

        g = {x : set() for x in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        q = [source]
        l = 0
        r = 1
        used = set()
        used.add(source)

        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if next not in used:
                    if next == destination:
                        return True
                    used.add(next)
                    q.append(next)
                    r += 1

        return False
```
