---
title: "3446. 按对角线进行矩阵排序"
aliases: ["yiduobo的每日leetcode 3446.按对角线进行矩阵排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/bian-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1892666682054529191"
zhihu_id: "1892666682054529191"
zhihu_title: "yiduobo的每日leetcode 3446.按对角线进行矩阵排序"
question_id: "3446"
question: "按对角线进行矩阵排序"
problem_url: "https://leetcode.cn/problems/sort-matrix-by-diagonals/"
difficulty: "Medium"
rating: 1373
created: "2025-04-07T20:10:27+08:00"
updated: "2025-04-07T20:10:27+08:00"
upvotes: 0
comments: 0
---

# 3446. 按对角线进行矩阵排序

> **[yiduobo的每日leetcode 3446.按对角线进行矩阵排序](https://zhuanlan.zhihu.com/p/1892666682054529191) · 知乎 · 2025-04-07 · 赞同 0**
> 力扣：[3446. 按对角线进行矩阵排序](https://leetcode.cn/problems/sort-matrix-by-diagonals/) · Medium · 灵茶山艾府：[【模板】遍历对角线（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3446.按对角线进行矩阵排序

[3446. 按对角线进行矩阵排序 - 力扣（LeetCode）](https://leetcode.cn/problems/sort-matrix-by-diagonals/description/)

题目给出一个大小为n \* n的整数方阵grid，要求对其进行一些调整：

1、左下角的三角形（包括主对角线）的对角线按非递增顺序排序

2、右上角的三角形的对角线按非递减顺序排序

要求返回调整后的矩阵。

按照题目要求进行模拟。

首先处理左下角的三角形。

按从上到下的顺序遍历左下角三角形中的每条对角线，可以发现这些对角线的起点都位于第0列，同时第index条对角线的起点位于第index行，这些对角线的终点则都位于最后一行。另一方面，对于这些对角线上的某个单元格(x, y)，其所属对角线上的下一个单元格为(x + 1, y + 1)。根据这两个结论，就可以遍历矩阵中的每一行，对于当前遍历到的行row，以第一个单元格(row, 0)作为当前对角线的起点不断向右下方行走，直到走到最后一行为止。使用一个数组nums收集行走过程中遍历到的元素，将nums从小到大排序后，按相同的走法将nums倒序填充回矩阵就行了。

接下来处理右上角的三角形，处理方法与上面类似。

按从上到下的顺序遍历右上角三角形中的每条对角线，可以发现这些对角线的起点都位于第0行，这些对角线的终点则都位于最后一列，同时第index条对角线的终点位于第index行。另一方面，对于这些对角线上的某个单元格(x, y)，其所属对角线上的上一个单元格为(x - 1, y - 1)。于是可以按上面类似的方法，遍历矩阵中的每一行，对于当前遍历到的行row，以最后一个单元格(row, n - 1)作为当前对角线的终点不断向左上方行走，直到走到第0行位置。使用一个数组nums收集行走过程中遍历到的元素，将nums从小到大排序后，按相同的走法将nums倒序重新填充回矩阵就行了。

最后附上python代码：

```python
class Solution(object):
    def sortMatrix(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """
        
        n = len(grid)

        for row in range(n):
            x = row
            y = 0
            nums = []
            while x < n:
                nums.append(grid[x][y])
                x += 1
                y += 1
            
            nums.sort()
            x = row
            y = 0
            while x < n:
                grid[x][y] = nums.pop()
                x += 1
                y += 1
        
        for row in range(n - 1):
            x = row
            y = n - 1
            nums = []
            while x >= 0:
                nums.append(grid[x][y])
                x -= 1
                y -= 1
            
            nums.sort()
            x = row
            y = n - 1
            while x >= 0:
                grid[x][y] = nums.pop()
                x -= 1
                y -= 1
        
        return grid
```
