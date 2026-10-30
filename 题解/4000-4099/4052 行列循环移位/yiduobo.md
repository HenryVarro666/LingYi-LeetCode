---
title: "4052. 行列循环移位"
aliases: ["yiduobo的每日leetcode 4052.行列循环移位"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2083671433532683066"
zhihu_id: "2083671433532683066"
zhihu_title: "yiduobo的每日leetcode 4052.行列循环移位"
question_id: "4052"
question: "行列循环移位"
problem_url: "https://leetcode.cn/problems/cyclically-shift-rows-and-columns/"
difficulty: "Easy"
created: "2026-09-16T21:43:58+08:00"
updated: "2026-09-16T21:43:58+08:00"
upvotes: 0
comments: 0
---

# 4052. 行列循环移位

> **[yiduobo的每日leetcode 4052.行列循环移位](https://zhuanlan.zhihu.com/p/2083671433532683066) · 知乎 · 2026-09-16 · 赞同 0**
> 力扣：[4052. 行列循环移位](https://leetcode.cn/problems/cyclically-shift-rows-and-columns/) · Easy · 灵茶山艾府：[两种写法：模拟 / 直接计算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4052.行列循环移位

<https://leetcode.cn/problems/cyclically-shift-rows-and-columns/description/>

题目给出一个大小为n \* n的二维整数数组grid，以及两个长度为n的整数数组rowShift以及colShift，其中：

- rowShift[i]表示将grid的第i行向左循环移位的位数
- colShift[j]表示将grid的第j列向上循环移位的位数

首先按照rowShift对每一行进行循环移位，然后按照colShift对每一列进行循环移位。

要求返回所有移位操作后的网格。

直接按照题目要求，先枚举每一行，执行左移操作，然后枚举每一列，执行上移操作即可。

在具体实现上，可以直接用后缀拼前缀的方式来达成移位的目标。

最后附上python代码：

```python
class Solution(object):
    def cyclicShift(self, n, grid, rowShift, colShift):
        """
        :type n: int
        :type grid: List[List[int]]
        :type rowShift: List[int]
        :type colShift: List[int]
        :rtype: List[List[int]]
        """
        
        for index, k in enumerate(rowShift):
            new_row = grid[index][k:] + grid[index][:k]
            grid[index] = new_row[:]
        
        for index, k in enumerate(colShift):
            col = [grid[r][index] for r in range(n)]
            new_col = col[k:] + col[:k]
            for r in range(n):
                grid[r][index] = new_col[r]
        
        return grid
```
