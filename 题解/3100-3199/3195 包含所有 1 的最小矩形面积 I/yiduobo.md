---
title: "3195. 包含所有1的最小矩形面积I"
aliases: ["yiduobo的每日leetcode 3195.包含所有1的最小矩形面积I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706907219"
zhihu_id: "706907219"
zhihu_title: "yiduobo的每日leetcode 3195.包含所有1的最小矩形面积I"
question_id: "3195"
question: "包含所有 1 的最小矩形面积 I"
problem_url: "https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-i/"
difficulty: "Medium"
created: "2024-07-04T00:10:20+08:00"
updated: "2024-07-04T00:10:20+08:00"
upvotes: 0
comments: 0
---

# 3195. 包含所有1的最小矩形面积I

> **[yiduobo的每日leetcode 3195.包含所有1的最小矩形面积I](https://zhuanlan.zhihu.com/p/706907219) · 知乎 · 2024-07-04 · 赞同 0**
> 力扣：[3195. 包含所有 1 的最小矩形面积 I](https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-i/) · Medium · 灵茶山艾府：[寻找矩形的左右上下边界（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3915.包含所有1的最小矩形面积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-i/description/)

题目给出一个二维的二进制数组grid，要求找出边在水平与竖直方向上，且面积最小的矩形，其包含grid中所有的1。问这个最小的面积是多少。

令grid中最左侧和最右侧1所在的列分别为left和right，最上方和最下方的1所在的行分别为top和bottom，那么最终答案中的矩形在列上至少需要覆盖住left到right这一段，在行上则需要覆盖住top到bottom这一段。

另一方面，对于grid中的所有1，其所在的列j都满足left \<\= j \<\= right，其所在的行i都满足top \<\= i \<\= bottom。换言之，只要矩形能覆盖住最外侧的1，那么就必然可以覆盖住内部的1。

综合起来，顶着left、right和top、bottom构造矩形就是最优的选择，因此最终答案就是(bottom - top + 1) \* (right - left + 1)。

最后附上python代码：

```python
class Solution(object):
    def minimumArea(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        left, right = n - 1, 0
        top, bottom = m - 1, 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    top = min(top, i)
                    bottom = max(bottom, i)
                    left = min(left, j)
                    right = max(right, j)

        return (bottom - top + 1) * (right - left + 1)
```
