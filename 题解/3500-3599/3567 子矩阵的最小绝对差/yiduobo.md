---
title: "3567. 子矩阵的最小绝对差"
aliases: ["yiduobo的每日leetcode 3567.子矩阵的最小绝对差"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1935831412050731966"
zhihu_id: "1935831412050731966"
zhihu_title: "yiduobo的每日leetcode 3567.子矩阵的最小绝对差"
question_id: "3567"
question: "子矩阵的最小绝对差"
problem_url: "https://leetcode.cn/problems/minimum-absolute-difference-in-sliding-submatrix/"
difficulty: "Medium"
created: "2025-08-04T22:47:18+08:00"
updated: "2025-08-04T22:47:18+08:00"
upvotes: 1
comments: 0
---

# 3567. 子矩阵的最小绝对差

> **[yiduobo的每日leetcode 3567.子矩阵的最小绝对差](https://zhuanlan.zhihu.com/p/1935831412050731966) · 知乎 · 2025-08-04 · 赞同 1**
> 力扣：[3567. 子矩阵的最小绝对差](https://leetcode.cn/problems/minimum-absolute-difference-in-sliding-submatrix/) · Medium · 灵茶山艾府：[暴力枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3567.子矩阵的最小绝对差

[3567. 子矩阵的最小绝对差 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-absolute-difference-in-sliding-submatrix/description/)

题目给出一个大小为m \* n的整数矩阵grid以及一个整数k，其中m和n都不超过30。

要求对于grid中每个连续的k \* k的子矩阵，计算其中任意两个不同值之间的最小绝对差。

题目的数据规模较小，因此可以直接暴力枚举每个k \* k的子矩阵，将其中的元素收集起来，排序后一趟遍历，计算相邻元素间的差值并记录最小差即可。

最后附上python代码：

```python
class Solution(object):
    def minAbsDiff(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """
        
        m = len(grid)
        n = len(grid[0])
        res = []
        for i in range(m - k + 1):
            res.append([])
            for j in range(n - k + 1):
                nums = []
                for x in range(i, i + k):
                    for y in range(j, j + k):
                        nums.append(grid[x][y])
                nums.sort()
                mi = 0
                for index in range(1, len(nums)):
                    diff = nums[index] - nums[index - 1]
                    if diff == 0:
                        continue
                    if mi == 0 or mi > diff:
                        mi = diff
                res[-1].append(mi)

        return res
```
