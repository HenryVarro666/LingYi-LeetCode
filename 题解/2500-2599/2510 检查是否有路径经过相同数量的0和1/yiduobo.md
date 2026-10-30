---
title: "2510. 检查是否有路径经过相同数量的0和1"
aliases: ["yiduobo的每日leetcode 2510.检查是否有路径经过相同数量的0和1"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632914856"
zhihu_id: "632914856"
zhihu_title: "yiduobo的每日leetcode 2510.检查是否有路径经过相同数量的0和1"
question_id: "2510"
question: "检查是否有路径经过相同数量的0和1"
problem_url: "https://leetcode.cn/problems/check-if-there-is-a-path-with-equal-number-of-0s-and-1s/"
created: "2023-05-29T02:40:28+08:00"
updated: "2023-05-29T02:40:28+08:00"
upvotes: 0
comments: 0
---

# 2510. 检查是否有路径经过相同数量的0和1

> **[yiduobo的每日leetcode 2510.检查是否有路径经过相同数量的0和1](https://zhuanlan.zhihu.com/p/632914856) · 知乎 · 2023-05-29 · 赞同 0**
> 力扣：[2510. 检查是否有路径经过相同数量的0和1](https://leetcode.cn/problems/check-if-there-is-a-path-with-equal-number-of-0s-and-1s/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2510.检查是否有路径经过相同数量的0和1

[力扣](https://leetcode.cn/problems/check-if-there-is-a-path-with-equal-number-of-0s-and-1s/)

经典动态规划问题的升级版，令f[i][j][k]表示来到位置(i, j)，经过的1的数量比0的数量之差是否可能为k。那么对于f[i][j][k]，若grid[i][j]为0，那么就可以从f[i - 1][j][k + 1]以及f[i][j - 1][k + 1]转移过来，反之则可以从f[i - 1][j][k - 1]以及f[i][j - 1][k - 1]转移过来。计算完成后，f[-1][-1][0]即为最终答案。

在具体实现上，由于k这一维实际可能覆盖的数值范围是比较稀疏的，因此也可以使用集合来替换掉k这一维。

最后附上python代码：

```python
class Solution(object):
    def isThereAPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])

        f = [[set() for j in range(n)] for i in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    delta = -1
                else:
                    delta = 1

                if i == 0 and j == 0:
                    f[i][j].add(delta)
                else:
                    if i > 0:
                        for v in f[i - 1][j]:
                            f[i][j].add(v + delta)
                
                    if j > 0:
                        for v in f[i][j - 1]:
                            f[i][j].add(v + delta)
        
        return 0 in f[-1][-1]
```
