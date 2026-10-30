---
title: "1284. 转化为全零矩阵的最少翻转次数"
aliases: ["yiduobo的每日leetcode 1284.转化为全零矩阵的最少翻转次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388725900"
zhihu_id: "388725900"
zhihu_title: "yiduobo的每日leetcode 1284.转化为全零矩阵的最少翻转次数"
question_id: "1284"
question: "转化为全零矩阵的最少翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix/"
created: "2021-07-11T22:24:05+08:00"
updated: "2021-07-11T22:24:05+08:00"
upvotes: 0
comments: 0
---

# 1284. 转化为全零矩阵的最少翻转次数

> **[yiduobo的每日leetcode 1284.转化为全零矩阵的最少翻转次数](https://zhuanlan.zhihu.com/p/388725900) · 知乎 · 2021-07-11 · 赞同 0**
> 力扣：[1284. 转化为全零矩阵的最少翻转次数](https://leetcode.cn/problems/minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1284.转化为全零矩阵的最少翻转次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix/)

由于这里的矩阵最多只有9个格子，同时取值只能是0或者1，那么最多也就只有2^(m \* n)种不同的状态。

另外，由于这里是执行翻转操作，那么在二进制表示下就是异或操作，于是我们可以先预处理出对每个格子执行翻转操作时的变化情况，并将其记录在list当中。接下来从初始状态开始进行bfs，每一轮都尝试翻转每个格子，直到bfs完成或者出现全0的情况。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        near_list = []
        m = len(mat)
        n = len(mat[0])
        now = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                p = i * n + j
                if mat[i][j]:
                    now |= (1 << p)
                near = (1 << p)
                for index in range(4):
                    x = i + dx[index]
                    y = j + dy[index]
                    if x >= 0 and x < m and y >= 0 and y < n:
                        near_p = x * n + y
                        near |= (1 << near_p)
                near_list.append(near)
        
        if now == 0:
            return 0

        q = [now]
        l = 0
        r = 1
        used = [False] * (1 << (m * n))
        used[now] = True
        res = 0
        while l < r:
            res += 1
            for now in q[l : r]:
                for near in near_list:
                    next = now ^ near
                    if not used[next]:
                        used[next] = True
                        q.append(next)
        
            if used[0]:
                return res

            l, r = r, len(q)

        return -1
```
