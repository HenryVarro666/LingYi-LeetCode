---
title: "3898. 统计每个顶点的度"
aliases: ["yiduobo的每日leetcode 3898.统计每个顶点的度"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2027896860426160073"
zhihu_id: "2027896860426160073"
zhihu_title: "yiduobo的每日leetcode 3898.统计每个顶点的度"
question_id: "3898"
question: "统计每个顶点的度"
problem_url: "https://leetcode.cn/problems/find-the-degree-of-each-vertex/"
difficulty: "Easy"
created: "2026-04-15T23:55:15+08:00"
updated: "2026-04-15T23:55:19+08:00"
upvotes: 0
comments: 0
---

# 3898. 统计每个顶点的度

> **[yiduobo的每日leetcode 3898.统计每个顶点的度](https://zhuanlan.zhihu.com/p/2027896860426160073) · 知乎 · 2026-04-15 · 赞同 0**
> 力扣：[3898. 统计每个顶点的度](https://leetcode.cn/problems/find-the-degree-of-each-vertex/) · Easy · 灵茶山艾府：[阅读理解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3898.统计每个顶点的度

<https://leetcode.cn/problems/find-the-degree-of-each-vertex/description/>

题目给出一个大小为n \* n的二维整数数组matrix，以邻接矩阵的形式表示一个无向图。图中包含n个顶点，编号为0到n - 1。若matrix[i][j]为1，则表示i和j之间有一条边，反之若matrix[i][j]为0，则表示i和j之间不存在边。

要求返回一个长度为n的数组ans，其中ans[i]表示i的度。

对于第i个顶点，matrix[i]表达就是i的连接情况，更具体的，其中1的数量就是i与其他节点连边的数量，即i的度。因此只需遍历matrix的每一行，计算行的和即可。

最后附上python代码：

```python
class Solution(object):
    def findDegrees(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        
        return [sum(row) for row in matrix]
```
