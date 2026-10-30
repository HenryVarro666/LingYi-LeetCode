---
title: "885. 螺旋矩阵III"
aliases: ["yiduobo的每日leetcode 885.螺旋矩阵III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351541732"
zhihu_id: "351541732"
zhihu_title: "yiduobo的每日leetcode 885.螺旋矩阵III"
question_id: "885"
question: "螺旋矩阵III"
problem_url: "https://leetcode.cn/problems/spiral-matrix-iii/"
created: "2021-02-19T22:14:22+08:00"
updated: "2021-02-19T22:14:41+08:00"
upvotes: 1
comments: 0
---

# 885. 螺旋矩阵III

> **[yiduobo的每日leetcode 885.螺旋矩阵III](https://zhuanlan.zhihu.com/p/351541732) · 知乎 · 2021-02-19 · 赞同 1**
> 力扣：[885. 螺旋矩阵III](https://leetcode.cn/problems/spiral-matrix-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

885.螺旋矩阵III

[力扣](https://leetcode-cn.com/problems/spiral-matrix-iii/)

我们将右、下、左、上作为一个轮次来看，那么从1开始，行动规则如下：

第一轮：向右走1步 -> 向下走1步 -> 向左走2步 -> 向上走2步

第二轮：向右走3步 -> 向下走3步 -> 向左走4步 -> 向上走4步

第三轮：向右走5步 -> 向下走5步 -> 向左走6步 -> 向上走6步

从中可以发现规律，即每变换两次方向之后走的步长将加1。于是我们可以从1开始模拟整个行走过程，按照右、下、左、上的顺序行走，同时维护当前应该走的步长。当目的地在矩阵之内，则将其加入到答案当中，直到走完整个矩阵。

最后附上python代码：

```python
class Solution(object):
    def spiralMatrixIII(self, R, C, r0, c0):
        """
        :type R: int
        :type C: int
        :type r0: int
        :type c0: int
        :rtype: List[List[int]]
        """

        step = 0
        nowx = r0
        nowy = c0
        res = [[nowx, nowy]]
        while len(res) < R * C:
            step += 1
            for _ in range(step):
                nowy += 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            for _ in range(step):
                nowx += 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            step += 1
            for _ in range(step):
                nowy -= 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
            for _ in range(step):
                nowx -= 1
                if nowx >= 0 and nowx < R and nowy >= 0 and nowy < C:
                    res.append([nowx, nowy])
        
        return res
```
