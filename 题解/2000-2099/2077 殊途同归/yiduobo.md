---
title: "2077. 殊途同归"
aliases: ["yiduobo的每日leetcode 2077.殊途同归"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625947189"
zhihu_id: "625947189"
zhihu_title: "yiduobo的每日leetcode 2077.殊途同归"
question_id: "2077"
question: "殊途同归"
problem_url: "https://leetcode.cn/problems/paths-in-maze-that-lead-to-same-room/"
created: "2023-04-30T05:09:12+08:00"
updated: "2023-04-30T05:09:12+08:00"
upvotes: 0
comments: 0
---

# 2077. 殊途同归

> **[yiduobo的每日leetcode 2077.殊途同归](https://zhuanlan.zhihu.com/p/625947189) · 知乎 · 2023-04-30 · 赞同 0**
> 力扣：[2077. 殊途同归](https://leetcode.cn/problems/paths-in-maze-that-lead-to-same-room/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2077.殊途同归

[力扣](https://leetcode.cn/problems/paths-in-maze-that-lead-to-same-room/)

题目要求找出图中所有的三角形，是之前遇到过的LCP16题的弱化版，直接套用之前找三角形的分情况讨论算法就行了。简单描述就是按照每个节点的度与sqrt(2M)的大小将节点分为两类，对于度较小的这类节点可以枚举其相邻节点求解，因为度较小所以保证了枚举的复杂度。另一方面，度较大的节点数量是很稀少的，因此可以直接暴力枚举三个节点来求解。

具体可以参考

[yiduobo：yiduobo的每日leetcode LCP16.游乐园的游览计划](https://zhuanlan.zhihu.com/p/571671362)

最后附上python代码：

```python
class Solution(object):
    def numberOfPaths(self, n, corridors):
        """
        :type n: int
        :type corridors: List[List[int]]
        :rtype: int
        """

        linked = {}
        for x, y in corridors:
            if x not in linked:
                linked[x] = set()
            if y not in linked:
                linked[y] = set()
            linked[x].add(y)
            linked[y].add(x)
        
        m = len(corridors)
        threshold = int(sqrt(2 * m))
        triangle_set = set()

        over_set = set()

        for i in linked:
            if len(linked[i]) < threshold:
                for j in linked[i]:
                    for k in linked[i]:
                        if j == k or k not in linked[j]:
                            continue
                        triangle_set.add(tuple(sorted([i, j, k])))
            else:
                over_set.add(i)
        
        for i in over_set:
            for j in over_set:
                if i == j or j not in linked[i]:
                    continue
                for k in over_set:
                    if i == k or j == k or k not in linked[i] or k not in linked[j]:
                        continue
                    triangle_set.add(tuple(sorted([i, j, k])))
        
        return len(triangle_set)
```
