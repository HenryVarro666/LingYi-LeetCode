---
title: "542. 01矩阵"
aliases: ["yiduobo的每日leetcode 542. 01矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261214943"
zhihu_id: "261214943"
zhihu_title: "yiduobo的每日leetcode 542. 01矩阵"
question_id: "542"
question: "01矩阵"
problem_url: "https://leetcode.cn/problems/01-matrix/"
created: "2020-10-08T15:09:52+08:00"
updated: "2020-10-08T15:09:52+08:00"
upvotes: 0
comments: 0
---

# 542. 01矩阵

> **[yiduobo的每日leetcode 542. 01矩阵](https://zhuanlan.zhihu.com/p/261214943) · 知乎 · 2020-10-08 · 赞同 0**
> 力扣：[542. 01矩阵](https://leetcode.cn/problems/01-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

542\. 01矩阵<https://leetcode-cn.com/problems/01-matrix/>

比较基础的题目。从矩阵中的每个0开始，一趟bfs，每次往当前值不为0且没有被使用过的地方扩展一步即可。

最后附上python代码：

```python
class Solution(object):
    def updateMatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(matrix)
        n = len(matrix[0])
        used = [[False] * n for _ in range(m)]
        q = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    q.append([i,j])
                    used[i][j] = True

        l = 0
        r = len(q)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                    matrix[x][y] = matrix[nowx][nowy] + 1
                    q.append([x, y])
                    r += 1
                    used[x][y] = True
        
        return matrix
```
