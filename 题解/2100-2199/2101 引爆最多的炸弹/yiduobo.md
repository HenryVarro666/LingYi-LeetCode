---
title: "2101. 引爆最多的炸弹"
aliases: ["yiduobo的每日leetcode 2101.引爆最多的炸弹"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/dfs", "题单/图论算法", "题单/图论算法/一-图的遍历", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521686845"
zhihu_id: "521686845"
zhihu_title: "yiduobo的每日leetcode 2101.引爆最多的炸弹"
question_id: "2101"
question: "引爆最多的炸弹"
problem_url: "https://leetcode.cn/problems/detonate-the-maximum-bombs/"
difficulty: "Medium"
rating: 1880
created: "2022-05-29T20:01:07+08:00"
updated: "2022-05-29T20:01:07+08:00"
upvotes: 0
comments: 0
---

# 2101. 引爆最多的炸弹

> **[yiduobo的每日leetcode 2101.引爆最多的炸弹](https://zhuanlan.zhihu.com/p/521686845) · 知乎 · 2022-05-29 · 赞同 0**
> 力扣：[2101. 引爆最多的炸弹](https://leetcode.cn/problems/detonate-the-maximum-bombs/) · Medium · 灵茶山艾府：[两种方法：DFS / Bitset+Floyd（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2101.引爆最多的炸弹

[力扣](https://leetcode.cn/problems/detonate-the-maximum-bombs/)

一个炸弹x可以引爆另一个炸弹y的条件是x和y之间的距离小于等于x的爆炸范围，那么就可以通过两两枚举所有的炸弹对，判断炸弹之间是否能互相引爆。

接下来，如果将炸弹视为图中的点，炸弹间是否能互相引爆视为图中的有向边，那么将得到一个有向图。题目实际上问的就是从图中哪一点开始能遍历到最多的节点。

最朴素的做法自然是枚举图中的每一个点，然后从这个点开始执行bfs或者dfs，记录从该点出发能遍历到的节点数目，这个做法最终的时间复杂度为O(n \* (m + n))，最坏情况下是O(n^3)的算法，不过对于本题已经足够了。

当然也存在更好的做法。首先，图中强联通分量中的点可以认为是等价的，因为这些点之间可以互相抵达，于是可以先通过tarjan算法找出图中所有的强联通分量，然后将每个强联通分量缩成一个点，并重新调整图中的边。这样一来，就得到了一张点有权重的有向无环图。接下来则可以利用经典的在拓扑排序中执行动态规划的做法来求解最终答案了。这个做法中的tarjan算法和以及拓扑排序的时间复杂度都是O(m + n)，最坏情况下可以认为是O(n^2)的算法。

我在这里偷懒，还是选择了朴素的做法。最后附上python代码：

```python
class Solution(object):
    def maximumDetonation(self, bombs):
        """
        :type bombs: List[List[int]]
        :rtype: int
        """

        n = len(bombs)
        g = {index : set() for index in range(n)}
        for i in range(n - 1):
            for j in range(i + 1, n):
                x1, y1, r1 = bombs[i]
                x2, y2, r2 = bombs[j]
                pow_d = (x1 -x2) ** 2 + (y1 - y2) ** 2
                if pow_d <= r1 * r1:
                    g[i].add(j)
                if pow_d <= r2 * r2:
                    g[j].add(i)
        
        res = 0
        for index in range(n):
            q = [index]
            used = set([index])
            l = 0
            r = 1
            while l < r:
                now = q[l]
                l += 1
                for next in g[now]:
                    if next not in used:
                        used.add(next)
                        q.append(next)
                        r += 1
            
            res = max(res, len(q))
        
        return res
```
