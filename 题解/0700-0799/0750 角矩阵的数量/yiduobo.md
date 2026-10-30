---
title: "750. 角矩阵的数量"
aliases: ["yiduobo的每日leetcode 750.角矩阵的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605553609"
zhihu_id: "605553609"
zhihu_title: "yiduobo的每日leetcode 750.角矩阵的数量"
question_id: "750"
question: "角矩阵的数量"
problem_url: "https://leetcode.cn/problems/number-of-corner-rectangles/"
created: "2023-02-11T23:50:07+08:00"
updated: "2023-02-11T23:50:07+08:00"
upvotes: 0
comments: 0
---

# 750. 角矩阵的数量

> **[yiduobo的每日leetcode 750.角矩阵的数量](https://zhuanlan.zhihu.com/p/605553609) · 知乎 · 2023-02-11 · 赞同 0**
> 力扣：[750. 角矩阵的数量](https://leetcode.cn/problems/number-of-corner-rectangles/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

750.角矩阵的数量

[力扣](https://leetcode.cn/problems/number-of-corner-rectangles/)

题目对于角矩阵的定义为grid中不同的四个位置(x1, y1)、(x1, y2)、(x2, y1)、(x2, y2)，要求这四个位置上对应的值都为1。

对于这个问题，可以先枚举行x，若行中存在两列y1和y2满足grid[x][y1] \= grid[x][y2] \= 1，同时在x上方的某些行中y1和y2这两列对应的值也为1，那么就找到了一个合法的角矩阵。更进一步的，可以使用一个哈希表储存每一行中值都为1的列的组合，那么对于后续的行，就只需要先找出行中值为1的列，然后两两枚举这些列并到哈希表中查找形成的角矩阵数量，最后更新哈希表即可。

最后附上python代码：

```python
class Solution(object):
    def countCornerRectangles(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        cnt = {}
        res = 0
        for i in range(m):
            pos = []
            for j in range(n):
                if grid[i][j] == 1:
                    for p in pos:
                        key = p * n + j
                        res += cnt.get(key, 0)
                        cnt[key] = cnt.get(key, 0) + 1
                        
                    pos.append(j)
        
        return res
```
