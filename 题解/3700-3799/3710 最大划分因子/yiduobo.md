---
title: "3710. 最大划分因子"
aliases: ["yiduobo的每日leetcode 3710.最大划分因子"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/union-find", "leetcode/graph", "leetcode/recursion", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/常用数据结构", "题单/图论算法", "题单/二分算法/二-二分答案", "题单/常用数据结构/七-并查集", "题单/图论算法/七-二分图染色"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961188690555560144"
zhihu_id: "1961188690555560144"
zhihu_title: "yiduobo的每日leetcode 3710.最大划分因子"
question_id: "3710"
question: "最大划分因子"
problem_url: "https://leetcode.cn/problems/maximum-partition-factor/"
difficulty: "Hard"
rating: 2135
created: "2025-10-13T23:23:23+08:00"
updated: "2025-10-13T23:23:24+08:00"
upvotes: 2
comments: 0
---

# 3710. 最大划分因子

> **[yiduobo的每日leetcode 3710.最大划分因子](https://zhuanlan.zhihu.com/p/1961188690555560144) · 知乎 · 2025-10-13 · 赞同 2**
> 力扣：[3710. 最大划分因子](https://leetcode.cn/problems/maximum-partition-factor/) · Hard · 灵茶山艾府：[两种方法：二分答案+二分图 / 排序+带权并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3710.最大划分因子

[3710. 最大划分因子 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-partition-factor/description/)

题目给出一个二维整数数组points，其中points\[i\] \= \[x\[i\], y\[i\]\]，表示笛卡尔平面上第i个点的坐标。points的数量不超过500。

对于一组点对(points[i], points[j])，二者的曼哈顿距离为|x[i] - x[j]| + |y[i] - y[j]|。

现在要求将这n个点划分为两个非空的组，定义划分因子为同一组内所有点对之间最小的曼哈顿距离，问可能得到的最大划分因子是多少。

由于题目中点的数量不超过500，因此可以先计算出所有点两两之间的曼哈顿距离，方便后续使用。另一方面，划分因子越小，越可能得到可行的划分，因此在这里可以二分答案，将问题转化为对于特定的划分因子mid，能否得到可行的划分。而对于这个问题，则可以使用二分图染色的方式来进行判定。

具体来说，可以将这些点视为图中的点，当点对间的距离小于mid时，在点对间连上一条无向边，那么问题就变成了给出一张无向图，问能否对这张图进行染色，使得相邻点间的颜色互不相同。

由于只需要分成两个部分，也就是说只有两种颜色，因此在这里是一个判定问题，而不是一个决策问题：只需对所有点进行一趟遍历，若当前点无色，则将其染成一种颜色，然后递归从这个点开始进行染色。对于当前节点，遍历其所有相邻的节点，此时可以分成三种情况：

1、若相邻节点无色，则将其染成与当前节点颜色不同的另一种颜色，然后递归从相邻节点开始继续染色

2、若相邻节点与当前节点异色，则无需处理，直接跳过

3、若相邻节点与当前节点同色，说明出现同色的相邻节点，也就是说此时没有合法的染色方案

对于当前的mid，若可以成功染色，则应该调整二分的下界为mid，否则需要调整二分的上界为mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maxPartitionFactor(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        n = len(points)
        if n <= 2:
            return 0

        dis = [[0] * n for _ in range(n)]
        ma = 0
        for i in range(n):
            for j in range(i + 1, n):
                dis[i][j] = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                dis[j][i] = dis[i][j]
                ma = max(ma, dis[i][j])

        def check(now, threshold):
            for nxt in range(n):
                if now == nxt:
                    continue
                if dis[now][nxt] < threshold:
                    if color[nxt] is None:
                        color[nxt] = 1 - color[now]
                        if not check(nxt, threshold):
                            return False
                    elif color[nxt] == color[now]:
                        return False
            
            return True

        left = 0
        right = ma

        while left < right:
            mid = (left + right + 1) // 2
            color = [None] * n
            flag = True
            for i in range(n):
                if color[i] is None:
                    color[i] = 0
                    if not check(i, mid):
                        flag = False
                        break

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
```
