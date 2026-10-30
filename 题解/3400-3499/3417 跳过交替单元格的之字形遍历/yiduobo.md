---
title: "3417. 跳过交替单元格的之字形遍历"
aliases: ["yiduobo的每日leetcode 3417.跳过交替单元格的之字形遍历"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32511475679"
zhihu_id: "32511475679"
zhihu_title: "yiduobo的每日leetcode 3417.跳过交替单元格的之字形遍历"
question_id: "3417"
question: "跳过交替单元格的之字形遍历"
problem_url: "https://leetcode.cn/problems/zigzag-grid-traversal-with-skip/"
difficulty: "Easy"
created: "2025-03-25T03:48:30+08:00"
updated: "2025-03-25T03:48:30+08:00"
upvotes: 0
comments: 0
---

# 3417. 跳过交替单元格的之字形遍历

> **[yiduobo的每日leetcode 3417.跳过交替单元格的之字形遍历](https://zhuanlan.zhihu.com/p/32511475679) · 知乎 · 2025-03-25 · 赞同 0**
> 力扣：[3417. 跳过交替单元格的之字形遍历](https://leetcode.cn/problems/zigzag-grid-traversal-with-skip/) · Easy · 灵茶山艾府：[两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3417.跳过交替单元格的之字形遍历

[3417. 跳过交替单元格的之字形遍历 - 力扣（LeetCode）](https://leetcode.cn/problems/zigzag-grid-traversal-with-skip/description/)

题目给出一个由正整数组成，大小为m \* n的二维数组grid。现在要求按照之字形遍历grid，同时跳过交替的单元格。之字形遍历指的是从左上角的单元格(0, 0)开始，在当前行中向右移动，来到末尾，然后移动到下一行，在该行中向左移动，来到开头，然后在行间交替向右和向左移动，直到遍历完所有行。

观察题目给出的样例可以发现，所有被遍历到的单元格的奇偶下标之和都是偶数，也就是说只需按题目要求，对偶数行从左向右遍历，对奇数行从右向左遍历，然后按顺序将所有奇偶下标之和为偶数的单元格加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def zigzagTraversal(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[int]
        """
        
        m = len(grid)
        n = len(grid[0])
        
        res = []
        for i in range(m):
            if i % 2 == 0:
                start, end, step = 0, n, 1
            else:
                start, end, step = n - 1, -1, -1
            
            for j in range(start, end, step):
                if (i + j) % 2 == 0:
                    res.append(grid[i][j])
        
        return res
```
