---
title: "3143. 正方形中的最多点数"
aliases: ["yiduobo的每日leetcode 3143.正方形中的最多点数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/binary-search", "leetcode/bian-li", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703287983"
zhihu_id: "703287983"
zhihu_title: "yiduobo的每日leetcode 3143.正方形中的最多点数"
question_id: "3143"
question: "正方形中的最多点数"
problem_url: "https://leetcode.cn/problems/maximum-points-inside-the-square/"
difficulty: "Medium"
rating: 1697
created: "2024-06-14T01:27:59+08:00"
updated: "2024-06-14T01:27:59+08:00"
upvotes: 0
comments: 0
---

# 3143. 正方形中的最多点数

> **[yiduobo的每日leetcode 3143.正方形中的最多点数](https://zhuanlan.zhihu.com/p/703287983) · 知乎 · 2024-06-14 · 赞同 0**
> 力扣：[3143. 正方形中的最多点数](https://leetcode.cn/problems/maximum-points-inside-the-square/) · Medium · 灵茶山艾府：[两种方法：从 O(nlog) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3143.正方形中的最多点数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-points-inside-the-square/description/)

题目给出二维平面上的一些点，每个点都有一个标签。现在要求找出一个中心处于(0, 0)的正方形，其边平行于坐标轴，且其中包含的点的标签各不相同，问正方形中最多可以包含多少个点。

首先，正方形的边长越长，其可能包含的点的数目就越多。另一方面，对于位于(x, y)的点，其在水平方向上与(0, 0)的距离为x的绝对值abs(x)，而在竖直方向上的距离则为y的绝对值abs(y)，那么当正方形边长的一半大于等于max(abs(x), abs(y))时，就说明(x, y)处于正方形中。根据这一点，就可以先将所有点按照max(abs(x), abs(y))从小到大排序，那么合法的正方形中包含的点必然是排序后点的一个前缀，于是只需枚举排序后点数组的所有前缀，判断当前前缀包含的点的标签是否各不相同即可。

最后附上python代码：

```python
class Solution(object):
    def maxPointsInsideSquare(self, points, s):
        """
        :type points: List[List[int]]
        :type s: str
        :rtype: int
        """

        dis = [max(abs(x), abs(y)) for x, y in points]

        rank = sorted(range(len(points)), key=lambda d:dis[d])
        p = 0
        vis = set()
        while p < len(rank):
            q = p
            while q < len(rank) and dis[rank[p]] == dis[rank[q]]:
                if s[rank[q]] in vis:
                    return p
                vis.add(s[rank[q]])
                q += 1
            
            p = q
        
        return p
```
