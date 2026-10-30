---
title: "3402. 使每一列严格递增的最少操作次数"
aliases: ["yiduobo的每日leetcode 3402.使每一列严格递增的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31140592453"
zhihu_id: "31140592453"
zhihu_title: "yiduobo的每日leetcode 3402.使每一列严格递增的最少操作次数"
question_id: "3402"
question: "使每一列严格递增的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-columns-strictly-increasing/"
difficulty: "Easy"
rating: 1246
created: "2025-03-18T22:32:44+08:00"
updated: "2025-03-18T22:32:44+08:00"
upvotes: 0
comments: 0
---

# 3402. 使每一列严格递增的最少操作次数

> **[yiduobo的每日leetcode 3402.使每一列严格递增的最少操作次数](https://zhuanlan.zhihu.com/p/31140592453) · 知乎 · 2025-03-18 · 赞同 0**
> 力扣：[3402. 使每一列严格递增的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-columns-strictly-increasing/) · Easy · 灵茶山艾府：[从上到下贪心，附变形题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3402.使每一列严格递增的最少操作次数

[3402. 使每一列严格递增的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-columns-strictly-increasing/description/)

题目给出一个大小m \* n的非负矩阵grid，在每次操作中，可以将grid中任意元素加上1。问至少需要多少次操作，才能使得grid中的每一列都严格递增。

由于题目要求所有列都严格递增，但是列与列之间是无关的，因此可以单独考虑每一列。又由于题目只支持加1操作，那么对于靠前的行就应该在满足递增的前提下越小越好，于是对于每列，只需从第1行开始遍历，对于当前元素，若其小于等于上面的相邻元素，就将其增加到上面相邻元素加1并更新答案，反之则无需进行操作。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        res = 0
        for j in range(n):
            for i in range(1, m):
                if grid[i][j] <= grid[i - 1][j]:
                    res += grid[i - 1][j] + 1 - grid[i][j]
                    grid[i][j] = grid[i - 1][j] + 1
        
        return res
```
