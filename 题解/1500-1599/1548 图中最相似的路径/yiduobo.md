---
title: "1548. 图中最相似的路径"
aliases: ["yiduobo的每日leetcode 1548.图中最相似的路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617797065"
zhihu_id: "617797065"
zhihu_title: "yiduobo的每日leetcode 1548.图中最相似的路径"
question_id: "1548"
question: "图中最相似的路径"
problem_url: "https://leetcode.cn/problems/the-most-similar-path-in-a-graph/"
created: "2023-03-28T23:56:35+08:00"
updated: "2023-03-28T23:56:35+08:00"
upvotes: 0
comments: 0
---

# 1548. 图中最相似的路径

> **[yiduobo的每日leetcode 1548.图中最相似的路径](https://zhuanlan.zhihu.com/p/617797065) · 知乎 · 2023-03-28 · 赞同 0**
> 力扣：[1548. 图中最相似的路径](https://leetcode.cn/problems/the-most-similar-path-in-a-graph/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1548.图中最相似的路径

[力扣](https://leetcode.cn/problems/the-most-similar-path-in-a-graph/)

首先需要注意的是，题目中对编辑距离的定义是城市名粒度而不是字符粒度的，在计算的时候不要弄混了。

题目的数据规模不大，因此选择O(n^3)的算法也是可行的，那么一个可行的思路就是先通过roads建图，接下来令f[i][j]表示前i步，最后一步走到列表中的第j个城市时，与target最小的编辑距离是多少。为了避开多次字符串匹配的复杂度，在这里可以使用一个数组dis记录第i步走到第j个城市是否会额外新增编辑距离，那么对于f[i][j]：

1、当i \= 0时：

显然有f[i][j] \= dis[i][j]

2、当i > 0时：

此时则需要枚举第i - 1轮所在的城市neibor，那么就有

f[i][j] \= min(f[i][j], f[i - 1][neibor] + dis[i][j])，其中j与neibor相连

动态规划完成后，遍历所有城市，f[-1][j]中最小的那个j就是最后一个到达的城市。

需要注意的是，题目需要输出完整的路径，因此需要额外使用一个数组prev记录路径，具体来说prev[i][j]记录的是如果第i步走到第j个城市的话，其上一轮应该从哪个城市过来。这样一来，就可以从上面找到的j开始倒推找出完整的路径了。

最后附上python代码：

```python
class Solution(object):
    def mostSimilar(self, n, roads, names, targetPath):
        """
        :type n: int
        :type roads: List[List[int]]
        :type names: List[str]
        :type targetPath: List[str]
        :rtype: List[int]
        """
        
        dis = []
        for target in targetPath:
            dis.append([])
            for name in names:
                if target == name:
                    dis[-1].append(0)
                else:
                    dis[-1].append(1)
        
        g = [[] for _ in range(n)]
        for x, y in roads:
            g[x].append(y)
            g[y].append(x)
        
        f = [[1000] * n for _ in range(len(targetPath))]
        prev = [[None] * n for _ in range(len(targetPath))]
        for i in range(len(targetPath)):
            if i == 0:
                for j in range(n):
                    f[i][j] = min(f[i][j], dis[i][j])
            else:
                for j in range(n):
                    for neibor in g[j]:
                        if f[i - 1][neibor] + dis[i][j] < f[i][j]:
                            f[i][j] = f[i - 1][neibor] + dis[i][j]
                            prev[i][j] = neibor
        
        mi = 1000
        p = None
        for j in range(n):
            if f[-1][j] < mi:
                mi = f[-1][j]
                p = j

        res = []
        for i in range(len(targetPath) - 1, 0, -1):
            res.append(p)
            p = prev[i][p]
        
        res.append(p)
        res.reverse()

        return res
```
