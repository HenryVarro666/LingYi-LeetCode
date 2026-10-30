---
title: "1329. 将矩阵按对角线排序"
aliases: ["yiduobo的每日leetcode 1329.将矩阵按对角线排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394792394"
zhihu_id: "394792394"
zhihu_title: "yiduobo的每日leetcode 1329.将矩阵按对角线排序"
question_id: "1329"
question: "将矩阵按对角线排序"
problem_url: "https://leetcode.cn/problems/sort-the-matrix-diagonally/"
difficulty: "Medium"
rating: 1548
created: "2021-07-30T22:29:42+08:00"
updated: "2021-07-30T22:29:42+08:00"
upvotes: 0
comments: 2
---

# 1329. 将矩阵按对角线排序

> **[yiduobo的每日leetcode 1329.将矩阵按对角线排序](https://zhuanlan.zhihu.com/p/394792394) · 知乎 · 2021-07-30 · 赞同 0**
> 力扣：[1329. 将矩阵按对角线排序](https://leetcode.cn/problems/sort-the-matrix-diagonally/) · Medium · 灵茶山艾府：[对角线排序（附原地排序）Python/Java/C++/Go/JS/Rust](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1329.将矩阵按对角线排序

[力扣](https://leetcode-cn.com/problems/sort-the-matrix-diagonally/)

右对角线上的格子符合处于同一对角线上的格子，行减去列的值都是一样的，因此我们可以先根据行减列的值将矩阵中的所有格子分别收集起来，分别排序之后然后填充到答案中。

最后附上python代码：

```python
class Solution(object):
    def diagonalSort(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: List[List[int]]
        """

        num_dict = {}
        m = len(mat)
        n = len(mat[0])
        for i in range(m):
            for j in range(n):
                if i - j not in num_dict:
                    num_dict[i - j] = []
                num_dict[i - j].append(mat[i][j])
        
        for key in num_dict.keys():
            num_dict[key] = sorted(num_dict[key])
        res = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n):
                res[i][j] = num_dict[i - j][-1]
                num_dict[i - j].pop()
        
        return res
```
