---
title: "3923. 得到目标点的最少代数"
aliases: ["yiduobo的每日leetcode 3923.得到目标点的最少代数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2037661934204482349"
zhihu_id: "2037661934204482349"
zhihu_title: "yiduobo的每日leetcode 3923.得到目标点的最少代数"
question_id: "3923"
question: "得到目标点的最少代数"
problem_url: "https://leetcode.cn/problems/minimum-generations-to-target-point/"
difficulty: "Medium"
created: "2026-05-13T01:49:34+08:00"
updated: "2026-05-13T01:49:35+08:00"
upvotes: 2
comments: 0
---

# 3923. 得到目标点的最少代数

> **[yiduobo的每日leetcode 3923.得到目标点的最少代数](https://zhuanlan.zhihu.com/p/2037661934204482349) · 知乎 · 2026-05-13 · 赞同 2**
> 力扣：[3923. 得到目标点的最少代数](https://leetcode.cn/problems/minimum-generations-to-target-point/) · Medium · 灵茶山艾府：[暴力模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3923.得到目标点的最少代数

<https://leetcode.cn/problems/minimum-generations-to-target-point/description/>

题目给出一个二维整数数组points，其中points\[index\] \= \[x\[index\], y\[index\], z\[index\]\]，表示三维空间的一个点。这里的points长度不超过20，其中所有的x、y、z都在0到6之间。

另外给出一个表示目标点的整数数组target \= [tx, ty, tz]，其中所有的元素同样在0到6之间。

定义第0代的为初始点的列表points，接下来对于每个整数k >\= 1，按照如下方式形成第k代：

- 考虑从0到第k - 1代所有点中的不同点对a \= [x1, y1, z1]以及b \= [x2, y2, z2]，这里的不同指的是两个点在至少一个维度上不一样。
- 对于所有点对，计算c \= [(x1 + x2) // 2, (y1 + y2) // 2, (z1 + z2) // 2]，这里的//表示向下取整的除法。接下来，将所有这样的点c收录到第k代的点中。

现在要求找出最小的整数k，是的target出现在这一代点集中。若target一开始就存在于points中，则返回0；若无法获得target，则返回-1。

由于题目中元素的取值范围都在0到6之间，那么就意味着最多也只有7 \* 7 \* 7 \= 343种不同的点，因此在这里完全可以直接暴力计算。使用一个标记变量changed记录是否在上一轮中出现了新的点，然后开始执行循环生成新的点，直到target出现在点集中，或者changed为false，即没有新的点出现。

每一轮生成操作中，先将changed置为false，然后两两枚举当前点集中的所有点对，然后计算生成的点。若这个新点是第一次出现，那么就将其加入到点集中，并将changed置为true。

由于每一轮都至少会生成一个新的点，而每轮操作中需要枚举所有的点对，因此最终的计算总次数不会超过343 \* 343 \* 343次，而且实际上应该比这个值小得多。

最后附上python代码：

```python
class Solution(object):
    def minGenerations(self, points, target):
        """
        :type points: List[List[int]]
        :type target: List[int]
        :rtype: int
        """
        
        vis = set()
        for x, y, z in points:
            vis.add((x, y, z))
        
        changed = True
        t = (target[0], target[1], target[2])
        res = 0
        while t not in vis and changed:
            changed = False
            points = list(vis)
            for i in range(len(points) - 1):
                for j in range(i + 1, len(points)):
                    x = (points[i][0] + points[j][0]) // 2
                    y = (points[i][1] + points[j][1]) // 2
                    z = (points[i][2] + points[j][2]) // 2
                    p = (x, y, z)
                    if p not in vis:
                        vis.add(p)
                        changed = True
            res += 1
        
        if t not in vis:
            return -1
        return res
```
