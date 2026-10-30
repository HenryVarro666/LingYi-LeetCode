---
title: "2371. 最小化网络中的最大值"
aliases: ["yiduobo的每日leetcode 2371.最小化网络中的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630507642"
zhihu_id: "630507642"
zhihu_title: "yiduobo的每日leetcode 2371.最小化网络中的最大值"
question_id: "2371"
question: "最小化网络中的最大值"
problem_url: "https://leetcode.cn/problems/minimize-maximum-value-in-a-grid/"
created: "2023-05-19T02:51:50+08:00"
updated: "2023-05-19T02:51:50+08:00"
upvotes: 0
comments: 0
---

# 2371. 最小化网络中的最大值

> **[yiduobo的每日leetcode 2371.最小化网络中的最大值](https://zhuanlan.zhihu.com/p/630507642) · 知乎 · 2023-05-19 · 赞同 0**
> 力扣：[2371. 最小化网络中的最大值](https://leetcode.cn/problems/minimize-maximum-value-in-a-grid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2371.最小化网络中的最大值

[力扣](https://leetcode.cn/problems/minimize-maximum-value-in-a-grid/)

首先，网格中的最小值显然映射为1。不妨设这个最小值出现在网格中的位置(i, j)，其只会影响到第i行以及第j列。更进一步的，对于第i行以及第j列，下一个数的起点就必须从2开始。于是可以使用两个数组row以及col记录每一行和每一列当前的最大值，这样一来对于位置(i, j)，就可以通过row[i]以及col[j]来确定(i, j)可以填充的最小整数。于是可以将网格中的数从小到大进行排序，然后一趟遍历，利用row以及col确定网格中每个位置的映射值。

最后附上python代码：

```python
class Solution(object):
    def minScore(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])
        num_list = []
        for i in range(m):
            for j in range(n):
                num_list.append([grid[i][j], i, j])
        
        row = [0] * m
        col = [0] * n
        res = [[0] * n for _ in range(m)]
        for _, i, j in sorted(num_list):
            res[i][j] = max(row[i], col[j]) + 1
            row[i] = res[i][j]
            col[j] = res[i][j]
        
        return res
```
