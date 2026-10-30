---
title: "1260. 二维网格迁移"
aliases: ["yiduobo的每日leetcode 1260.二维网格迁移"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386432530"
zhihu_id: "386432530"
zhihu_title: "yiduobo的每日leetcode 1260.二维网格迁移"
question_id: "1260"
question: "二维网格迁移"
problem_url: "https://leetcode.cn/problems/shift-2d-grid/"
difficulty: "Easy"
created: "2021-07-05T01:58:14+08:00"
updated: "2021-07-05T01:58:14+08:00"
upvotes: 0
comments: 0
---

# 1260. 二维网格迁移

> **[yiduobo的每日leetcode 1260.二维网格迁移](https://zhuanlan.zhihu.com/p/386432530) · 知乎 · 2021-07-05 · 赞同 0**
> 力扣：[1260. 二维网格迁移](https://leetcode.cn/problems/shift-2d-grid/) · Easy · 灵茶山艾府：[两种方法：创建新数组 / 原地三次反转（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1260.二维网格迁移

[力扣](https://leetcode-cn.com/problems/shift-2d-grid/)

仔细观察这个迁移过程，如果我们按照从上到下从左到右的顺序来看这个矩阵，实际上就是每个数字都向后推移了k位，于是一个自然的想法就是将这个二维网格写成一维数组的形式，然后将这个数组的后k个数截断，并拼接在数组的前方，最后再将这个数组转化回二维网格的形式即可。

最后附上python代码：

```python
class Solution(object):
    def shiftGrid(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])
        k %= (m * n)
        if k == 0:
            return grid

        tmp = [grid[i][j] for i in range(m) for j in range(n)]
        tmp = tmp[m * n - k:] + tmp[:m * n - k]
        return [tmp[i * n : (i + 1) * n] for i in range(m)]
```
