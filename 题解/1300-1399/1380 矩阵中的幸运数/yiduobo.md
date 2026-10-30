---
title: "1380. 矩阵中的幸运数"
aliases: ["yiduobo的每日leetcode 1380.矩阵中的幸运数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402185679"
zhihu_id: "402185679"
zhihu_title: "yiduobo的每日leetcode 1380.矩阵中的幸运数"
question_id: "1380"
question: "矩阵中的幸运数"
problem_url: "https://leetcode.cn/problems/lucky-numbers-in-a-matrix/"
created: "2021-08-21T19:55:49+08:00"
updated: "2021-08-21T19:55:49+08:00"
upvotes: 0
comments: 0
---

# 1380. 矩阵中的幸运数

> **[yiduobo的每日leetcode 1380.矩阵中的幸运数](https://zhuanlan.zhihu.com/p/402185679) · 知乎 · 2021-08-21 · 赞同 0**
> 力扣：[1380. 矩阵中的幸运数](https://leetcode.cn/problems/lucky-numbers-in-a-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1380.矩阵中的幸运数

[力扣](https://leetcode-cn.com/problems/lucky-numbers-in-a-matrix/)

由于矩阵中的数都不相同，那么就意味着每一行都有唯一的最小值，每一列都有唯一的最大值。我们可以先找出每一行中的最小值位于哪一列，并使用一个数组row记录下来，接下来找出每一列中的最大值位于哪一行，同样是用一个数组col记录下来。

接下来，我们遍历每一行，对于当前行i，其最小值所在的列就是j \= row[i]，若此时满足col[j] \= i，也就是说j这一列的最大值位于第i行，那么就表示matrix[i][j]是第i行的最小值，同时也是第j列的最大值，因此matrix[i][j]是一个幸运数，将其加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def luckyNumbers (self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """

        row = []
        m = len(matrix)
        n = len(matrix[0])
        for i in range(m):
            now = 0
            for j in range(1, n):
                if matrix[i][now] > matrix[i][j]:
                    now = j
            row.append(now)
        
        col = []
        for j in range(n):
            now = 0
            for i in range(1, m):
                if matrix[now][j] < matrix[i][j]:
                    now = i
            col.append(now)
        
        res = []
        for i in range(m):
            j = row[i]
            if col[j] == i:
                res.append(matrix[i][j])
        
        return res
```
