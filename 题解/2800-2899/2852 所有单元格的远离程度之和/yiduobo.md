---
title: "2852. 所有单元格的远离程度之和"
aliases: ["yiduobo的每日leetcode 2852.所有单元格的远离程度之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660819872"
zhihu_id: "660819872"
zhihu_title: "yiduobo的每日leetcode 2852.所有单元格的远离程度之和"
question_id: "2852"
question: "所有单元格的远离程度之和"
problem_url: "https://leetcode.cn/problems/sum-of-remoteness-of-all-cells/"
created: "2023-10-12T03:40:50+08:00"
updated: "2023-10-12T03:40:50+08:00"
upvotes: 0
comments: 0
---

# 2852. 所有单元格的远离程度之和

> **[yiduobo的每日leetcode 2852.所有单元格的远离程度之和](https://zhuanlan.zhihu.com/p/660819872) · 知乎 · 2023-10-12 · 赞同 0**
> 力扣：[2852. 所有单元格的远离程度之和](https://leetcode.cn/problems/sum-of-remoteness-of-all-cells/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2852.所有单元格的远离程度之和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-of-remoteness-of-all-cells/description/)

题目中单元格的远离程度计算不会考虑来自相同连通块中单元格的影响，那么对于其中的某个连通块，设其中有k个单元格，这些单元格的数值之和为s，那么这些单元格对最终答案产生的影响就是k \* (tot_s - s)，其中tot_s是矩阵中所有单元格之和。这里的tot_s - s就是非当前连通块中的单元格权值之和，而对于当前连通块中的每个单元格，其对应的远离程度都是这个值，因此最终影响就是k \* (tot_s - s)。

到了这里，就只需使用floodfill找出网格中所有连通块，并计算出每个连通块中单元格的数目以及元素之和，接下来再遍历这些连通块，通过上面的式子计算出最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def sumRemoteness(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        parts = []

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        for i in range(m):
            for j in range(n):
                if grid[i][j] != -1:
                    q = [[i, j]]
                    head, tail = 0, 1
                    s = grid[i][j]
                    grid[i][j] = -1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for d in range(4):
                            x = nowx + dx[d]
                            y = nowy + dy[d]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] > 0:
                                s += grid[x][y]
                                q.append([x, y])
                                tail += 1
                                grid[x][y] = -1
                    
                    parts.append([len(q), s])
        
        tot_s = sum([x[1] for x in parts])
        res = 0
        for cnt, s in parts:
            res += (tot_s - s) * cnt
        
        return res
```
