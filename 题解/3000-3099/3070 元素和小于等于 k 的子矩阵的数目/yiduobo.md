---
title: "3070. 元素和小于等于k的子矩阵数目"
aliases: ["yiduobo的每日leetcode 3070.元素和小于等于k的子矩阵数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697379183"
zhihu_id: "697379183"
zhihu_title: "yiduobo的每日leetcode 3070.元素和小于等于k的子矩阵数目"
question_id: "3070"
question: "元素和小于等于 k 的子矩阵的数目"
problem_url: "https://leetcode.cn/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/"
difficulty: "Medium"
rating: 1499
created: "2024-05-13T03:04:10+08:00"
updated: "2024-05-13T03:04:10+08:00"
upvotes: 1
comments: 0
---

# 3070. 元素和小于等于k的子矩阵数目

> **[yiduobo的每日leetcode 3070.元素和小于等于k的子矩阵数目](https://zhuanlan.zhihu.com/p/697379183) · 知乎 · 2024-05-13 · 赞同 1**
> 力扣：[3070. 元素和小于等于 k 的子矩阵的数目](https://leetcode.cn/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/) · Medium · 灵茶山艾府：[两种方法：二维前缀和模板 / 维护每列元素和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3070.元素和小于等于k的子矩阵数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/description/)

非常标准的二维前缀和问题。令s[i][j]表示以(i, j)为右下角的子矩阵元素之和，那么对于s[i][j]，有s[i][j] \= s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + nums[i][j]，具体含义为利用之前的计算结果s[i - 1][j]以及s[i][j - 1]。其中s[i - 1][j]为当前子矩阵去掉最后一行所得，s[i][j - 1]则为当前子矩阵去掉最后一列所得，二者相加可以互相填补除nums[i][j]之外的最后一行以及最后一列，但是(i - 1, j - 1)为右下角的子矩阵将被计算两次，因此需要减掉。

最后附上python代码：

```python
class Solution(object):
    def countSubmatrices(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        s = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        s[i][j] = grid[i][j]
                    else:
                        s[i][j] = s[i][j - 1] + grid[i][j]
                elif j == 0:
                    s[i][j] = s[i - 1][j] + grid[i][j]
                else:
                    s[i][j] = s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1] + grid[i][j]
                    
                if s[i][j] <= k:
                    res += 1
                    
        return res
```
