---
title: "2661. 找出叠涂元素"
aliases: ["yiduobo的每日leetcode 2661.找出叠涂元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648378624"
zhihu_id: "648378624"
zhihu_title: "yiduobo的每日leetcode 2661.找出叠涂元素"
question_id: "2661"
question: "找出叠涂元素"
problem_url: "https://leetcode.cn/problems/first-completely-painted-row-or-column/"
created: "2023-08-07T01:10:12+08:00"
updated: "2023-08-07T01:10:12+08:00"
upvotes: 0
comments: 0
---

# 2661. 找出叠涂元素

> **[yiduobo的每日leetcode 2661.找出叠涂元素](https://zhuanlan.zhihu.com/p/648378624) · 知乎 · 2023-08-07 · 赞同 0**
> 力扣：[2661. 找出叠涂元素](https://leetcode.cn/problems/first-completely-painted-row-or-column/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2661.找出叠涂元素

[力扣](https://leetcode.cn/problems/first-completely-painted-row-or-column/)

对每一行和每一列都使用一个变量记录该行和该列的已经被填充的数的个数，接下来就只需要对arr进行一趟遍历，每次更新其所在行列对应变量的值。若某一行被填充的数的个数等于列的总数，或者某一列被填充的数的个数等于行的总数，那么就说明该行或者该列被填满，而答案就是当前遍历到的数在arr中的下标。

最后附上python代码：

```python
class Solution(object):
    def firstCompleteIndex(self, arr, mat):
        """
        :type arr: List[int]
        :type mat: List[List[int]]
        :rtype: int
        """

        k = len(arr)
        row = [None] * (k + 1)
        col = [None] * (k + 1)

        m = len(mat)
        n = len(mat[0])
        filled_row = [0] * m
        filled_col = [0] * n

        for i in range(m):
            for j in range(n):
                row[mat[i][j]] = i
                col[mat[i][j]] = j
        
        for index, v in enumerate(arr):
            filled_row[row[v]] += 1
            filled_col[col[v]] += 1
            if filled_row[row[v]] == n or filled_col[col[v]] == m:
                return index
```
