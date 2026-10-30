---
title: "1924. 安装栅栏II"
aliases: ["yiduobo的每日leetcode 1924.安装栅栏II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/geometry", "leetcode/math", "leetcode/randomized", "leetcode/sui-ji", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623599349"
zhihu_id: "623599349"
zhihu_title: "yiduobo的每日leetcode 1924.安装栅栏II"
question_id: "1924"
question: "安装栅栏 II"
problem_url: "https://leetcode.cn/problems/erect-the-fence-ii/"
difficulty: "Hard"
created: "2023-04-21T02:21:30+08:00"
updated: "2023-04-21T02:21:30+08:00"
upvotes: 0
comments: 0
---

# 1924. 安装栅栏II

> **[yiduobo的每日leetcode 1924.安装栅栏II](https://zhuanlan.zhihu.com/p/623599349) · 知乎 · 2023-04-21 · 赞同 0**
> 力扣：[1924. 安装栅栏 II](https://leetcode.cn/problems/erect-the-fence-ii/) · Hard · 灵茶山艾府：[Go 最小圆覆盖 Welzl 算法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1924.安装栅栏II

[力扣](https://leetcode.cn/problems/erect-the-fence-ii/)

经典的最小圆覆盖问题，可以使用Welzl算法或者模拟退火来求解，我在这里采用的是Welzl算法。Welzl算法基于一个定理：对于一个覆盖了n个点圆，取圆外的一点p，那么覆盖这n个点以及点p的圆一定会通过点p。基于这个定理，就只需一趟遍历，对于当前遍历到的点，若其在已经得到的最小圆中，那么就跳过该点，否则就以新遍历到的点作为新圆的圆心，然后回过头去遍历之前已经遍历过的点，重复运用上面这个定理找出圆上最外侧的两个点或者三个点。

这个算法的期望时间复杂度为O(n)，最坏情况是O(n^3)的，因此在执行算法前需要将所有点的顺序先随机打乱。

最后附上python代码：

```python
class Solution(object):
    def outerTrees(self, trees):
        """
        :type trees: List[List[int]]
        :rtype: List[float]
        """

        random.shuffle(trees)
        center = trees[0][:]
        radius = 0.0
        n = len(trees)

        def dis(p1, p2):
            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

        for i in range(n):
            if dis(trees[i], center) > radius:
                center = trees[i][:]
                radius = 0.0
                for j in range(i):
                    if dis(trees[j], center) > radius:
                        center[0] = (trees[i][0] + trees[j][0]) * 0.5
                        center[1] = (trees[i][1] + trees[j][1]) * 0.5
                        radius = dis(center, trees[i])
                        for k in range(j):
                            if dis(trees[k], center) > radius:
                                a = trees[i][0] - trees[j][0]
                                b = trees[i][1] - trees[j][1]
                                c = trees[i][0] - trees[k][0]
                                d = trees[i][1] - trees[k][1]
                                if b * c == a * d:
                                    di = dis(trees[i], trees[k])
                                    dj = dis(trees[j], trees[k])
                                    if di > dj:
                                        p = trees[i]
                                    else:
                                        p = trees[j]
                                    
                                    center[0] = (p[0] + trees[k][0]) * 0.5
                                    center[1] = (p[1] + trees[k][1]) * 0.5
                                else:
                                    e = ((trees[i][0] ** 2 - trees[j][0] ** 2) - (trees[j][1] ** 2 - trees[i][1] ** 2)) * 0.5
                                    f = ((trees[i][0] ** 2 - trees[k][0] ** 2) - (trees[k][1] ** 2 - trees[i][1] ** 2)) * 0.5
                                    center[0] = -(d * e - b *f) / (b * c - a * d)
                                    center[1] = -(a * f - c *e) / (b * c - a * d)

                                radius = dis(center, trees[i])
        
        return [center[0], center[1], radius]
```
