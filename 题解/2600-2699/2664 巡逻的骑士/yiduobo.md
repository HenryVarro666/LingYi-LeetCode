---
title: "2664. 巡逻的骑士"
aliases: ["yiduobo的每日leetcode 2664.巡逻的骑士"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648601708"
zhihu_id: "648601708"
zhihu_title: "yiduobo的每日leetcode 2664.巡逻的骑士"
question_id: "2664"
question: "巡逻的骑士"
problem_url: "https://leetcode.cn/problems/the-knights-tour/"
created: "2023-08-07T23:12:48+08:00"
updated: "2023-08-07T23:12:48+08:00"
upvotes: 1
comments: 0
---

# 2664. 巡逻的骑士

> **[yiduobo的每日leetcode 2664.巡逻的骑士](https://zhuanlan.zhihu.com/p/648601708) · 知乎 · 2023-08-07 · 赞同 1**
> 力扣：[2664. 巡逻的骑士](https://leetcode.cn/problems/the-knights-tour/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2664.巡逻的骑士

[力扣](https://leetcode.cn/problems/the-knights-tour/)

经典的骑士巡游问题，由于本题的数据规模很小，因此可以直接使用暴力搜索回溯进行求解。具体来说，就是每一轮都枚举8个目标落脚点，若落脚点合法，同时之前没有被访问过，那么就从这个落脚点继续向后执行搜索回溯，直到走完整个棋盘或者无法继续往下走。

最后附上python代码：

```python
class Solution(object):
    def tourOfKnight(self, m, n, r, c):
        """
        :type m: int
        :type n: int
        :type r: int
        :type c: int
        :rtype: List[List[int]]
        """

        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [2, 1, -1, -2, -2, -1, 1, 2]

        def dfs(level, nowx, nowy):
            if level == m * n:
                return True
            
            for d in range(8):
                x = nowx + dx[d]
                y = nowy + dy[d]
                if x >= 0 and x < m and y >= 0 and y < n and mat[x][y] is None:
                    mat[x][y] = mat[nowx][nowy] + 1
                    if dfs(level + 1, x, y):
                        return True
                    mat[x][y] = None
            
            return False

        mat = [[None] * n for _ in range(m)]
        mat[r][c] = 0
        dfs(1, r, c)

        return mat
```
