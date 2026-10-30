---
title: "240. 搜索二维矩阵 II"
aliases: ["yiduobo的每日leetcode 240.搜索二维矩阵 II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/matrix", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/矩阵"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150721621"
zhihu_id: "150721621"
zhihu_title: "yiduobo的每日leetcode 240.搜索二维矩阵 II"
question_id: "240"
question: "搜索二维矩阵 II"
problem_url: "https://leetcode.cn/problems/search-a-2d-matrix-ii/"
difficulty: "Medium"
created: "2020-06-25T21:40:07+08:00"
updated: "2020-06-25T21:40:07+08:00"
upvotes: 0
comments: 0
---

# 240. 搜索二维矩阵 II

> **[yiduobo的每日leetcode 240.搜索二维矩阵 II](https://zhuanlan.zhihu.com/p/150721621) · 知乎 · 2020-06-25 · 赞同 0**
> 力扣：[240. 搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/) · Medium · 灵茶山艾府：[【图解】排除法，一图秒懂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

240.搜索二维矩阵II <https://leetcode-cn.com/problems/search-a-2d-matrix-ii/>

拿到题目第一时间想到的是行列二分，但是需要注意的是，这里不满足前一行的元素都小于后一行的元素，于是二分在这里可能会出现问题。

比如样例中的5，对行的二分会找到3那一行，但是答案实际上位于2那一行，是有问题的，需要另想办法。

根据题目中行和列的性质，对于位于x行y列的数，其一定满足：

1、以(0, 0)为左上角，(x, y)为右下角的矩阵中，最大值就是(x, y)

2、以(x, y)为左上角，(m - 1, n - 1)为右下角的矩阵中，最小是就是(x, y)

那么如果从左下角(m - 1, 0)开始进行查找，就可以利用起上面这两个性质。

1、若target小于(m - 1, 0)，那么根据上面的第二条性质，最后一行都不可能是正确答案，于是我们排除最后一行，继续查找此时的左下角(m - 2, 0)。

2、若target大于(m - 1, 0)，那么根据上面的第一条性质，第一列都不可能是正确答案，于是我们排除第一列，继续查找此时的左下角(m - 1, 1)。

通过上面的方法不断排除左侧的行以及下方的列，最终就能找到target。

由于每次能排除掉一行或者一列，那么至多进行m + n就能找到答案，或者排除掉所有的行和列，于是最后的时间复杂度为O(m + n)。

最后附上python代码：

```python
class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """

        x = len(matrix) - 1
        y = 0

        while x >= 0 and y < len(matrix[0]):
            if matrix[x][y] == target:
                return True
            elif matrix[x][y] > target:
                x -= 1
            else:
                y += 1

        return False
```
