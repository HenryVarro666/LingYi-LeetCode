---
title: "1914. 循环轮转矩阵"
aliases: ["yiduobo的每日leetcode 1914.循环轮转矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/483726993"
zhihu_id: "483726993"
zhihu_title: "yiduobo的每日leetcode 1914.循环轮转矩阵"
question_id: "1914"
question: "循环轮转矩阵"
problem_url: "https://leetcode.cn/problems/cyclically-rotating-a-grid/"
difficulty: "Medium"
created: "2022-03-19T15:11:41+08:00"
updated: "2022-03-19T15:11:42+08:00"
upvotes: 1
comments: 0
---

# 1914. 循环轮转矩阵

> **[yiduobo的每日leetcode 1914.循环轮转矩阵](https://zhuanlan.zhihu.com/p/483726993) · 知乎 · 2022-03-19 · 赞同 1**
> 力扣：[1914. 循环轮转矩阵](https://leetcode.cn/problems/cyclically-rotating-a-grid/) · Medium · 灵茶山艾府：[利用方向向量简化代码，O(1) 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1914.循环轮转矩阵

[力扣](https://leetcode-cn.com/problems/cyclically-rotating-a-grid/)

按照题目要求，最直观的做法是从外向内一层一层拎出来，轮转完之后再填充到最后答案中。

设矩阵一共有m行n列，如果统计层数从0开始计数，那么对于第i层，其左上角、左下角、右上角以及右下角的坐标分别为(i, i)、(m - i - 1, i)、(i, n - i - 1)以及(m - i - 1, n - i - 1)。接下来只需要按照题目要求的逆时针方向，从左上角开始向下走到左下角，然后向右走到右下角，然后向上走到右上角，最后向左走回到左上角。

这样一来，就收集到了一层的所有数字。设这个层中数字的个数为l，那么轮转k次之后每个数字将会往后移动k % l个位置，此时只需要根据移动后的位置将数字填充进答案的对应位置即可。

最后附上python代码：

```python
class Solution(object):
    def rotateGrid(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """

        m = len(grid)
        n = len(grid[0])

        res = [[0] * n for _ in range(m)]

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for level in range(min(m / 2, n / 2)):
            tx = level
            bx = m - 1 - level
            ly = level
            ry = n - 1 - level

            level_list = []
            nowx = tx
            nowy = ly
            d = 0
            while True:
                level_list.append([nowx, nowy])
                if nowx == bx and nowy == ly:
                    d = 1
                elif nowx == bx and nowy == ry:
                    d = 2
                elif nowx == tx and nowy == ry:
                    d = 3
                
                nowx += dx[d]
                nowy += dy[d]
                if nowx == tx and nowy == ly:
                    break
            
            l = len(level_list)
            step = k % l
            for index in range(l):
                target = (index + step) % l
                res[level_list[target][0]][level_list[target][1]] = grid[level_list[index][0]][level_list[index][1]]

        return res
```
