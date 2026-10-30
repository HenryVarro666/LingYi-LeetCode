---
title: "463. 岛屿的周长"
aliases: ["yiduobo的每日leetcode 463.岛屿的周长"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/网格图", "题单/贪心算法", "题单/网格图/一-网格图-DFS", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/226015391"
zhihu_id: "226015391"
zhihu_title: "yiduobo的每日leetcode 463.岛屿的周长"
question_id: "463"
question: "岛屿的周长"
problem_url: "https://leetcode.cn/problems/island-perimeter/"
difficulty: "Easy"
created: "2020-09-08T20:11:56+08:00"
updated: "2020-09-08T20:11:56+08:00"
upvotes: 0
comments: 0
---

# 463. 岛屿的周长

> **[yiduobo的每日leetcode 463.岛屿的周长](https://zhuanlan.zhihu.com/p/226015391) · 知乎 · 2020-09-08 · 赞同 0**
> 力扣：[463. 岛屿的周长](https://leetcode.cn/problems/island-perimeter/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

463.岛屿的周长<https://leetcode-cn.com/problems/island-perimeter/>

对于一块陆地而言，若其位于最左侧那一列，或者其左侧单元格为水域，那么这块陆地的左边就应该计入到周长当中。同样的，其右侧、上边以及下边都应该遵循这个规则。

于是遍历所有单元格，检验每个单元格的四条边即可。

最后附上python代码：

```python
class Solution(object):
    def islandPerimeter(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        res = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    if i == 0 or grid[i - 1][j] == 0:
                        res += 1
                    if j == 0 or grid[i][j - 1] == 0:
                        res += 1
                    if i == len(grid) - 1 or grid[i + 1][j] == 0:
                        res += 1
                    if j == len(grid[0]) - 1 or grid[i][j + 1] == 0:
                        res += 1

        return res
```
