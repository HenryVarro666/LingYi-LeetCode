---
title: "54. 螺旋矩阵"
aliases: ["yiduobo的每日leetcode 54.螺旋矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/matrix", "leetcode/simulation", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/LeetCode-热题-100/矩阵", "题单/面试经典-150-题/矩阵"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/127382668"
zhihu_id: "127382668"
zhihu_title: "yiduobo的每日leetcode 54.螺旋矩阵"
question_id: "54"
question: "螺旋矩阵"
problem_url: "https://leetcode.cn/problems/spiral-matrix/"
difficulty: "Medium"
created: "2020-04-08T23:06:42+08:00"
updated: "2020-04-08T23:06:42+08:00"
upvotes: 0
comments: 0
---

# 54. 螺旋矩阵

> **[yiduobo的每日leetcode 54.螺旋矩阵](https://zhuanlan.zhihu.com/p/127382668) · 知乎 · 2020-04-08 · 赞同 0**
> 力扣：[54. 螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/) · Medium · 灵茶山艾府：[两种方法，简洁高效（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

54.螺旋矩阵<https://leetcode-cn.com/problems/spiral-matrix/>

这个题目思路与48题类似（传送门在此[yiduobo：yiduobo的每日leetcode 48.旋转图像](https://zhuanlan.zhihu.com/p/125769995)），同样是从外往内一层一层切分成上边、右边、下边、左边，然后依次输出。

需要特别注意的是由于这里不再是正方形，那么可能出现切分到某一层的长为一或者宽为一的情况，此时上边与下边或者左边与右边是重叠的，只能输出一次。

最后附上python代码：

```python
class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """

        if not matrix:
            return []

        res = []

        m = len(matrix)
        n = len(matrix[0])

        for index in range(min((m + 1) / 2, (n + 1) / 2)):
            x1 = y1 = index
            x2 = m - index - 1
            y2 = n - index - 1

            if x1 == x2:
                for pos in range(y1, y2 + 1):
                    res.append(matrix[x1][pos])
            elif y1 == y2:
                for pos in range(x1, x2 + 1):
                    res.append(matrix[pos][y1])
            else:

                for pos in range(y1, y2):
                    res.append(matrix[x1][pos])
                for pos in range(x1, x2):
                    res.append(matrix[pos][y2])
                for pos in range(y2, y1, -1):
                    res.append(matrix[x2][pos])
                for pos in range(x2, x1, -1):
                    res.append(matrix[pos][y1])

        return res
```
