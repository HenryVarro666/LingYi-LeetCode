---
title: "36. 有效的数独"
aliases: ["yiduobo的每日leetcode 36.有效的数独"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/bian-li", "题单/面试经典-150-题", "题单/面试经典-150-题/矩阵"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/121125182"
zhihu_id: "121125182"
zhihu_title: "yiduobo的每日leetcode 36.有效的数独"
question_id: "36"
question: "有效的数独"
problem_url: "https://leetcode.cn/problems/valid-sudoku/"
difficulty: "Medium"
created: "2020-03-30T22:59:01+08:00"
updated: "2020-03-30T22:59:01+08:00"
upvotes: 0
comments: 0
---

# 36. 有效的数独

> **[yiduobo的每日leetcode 36.有效的数独](https://zhuanlan.zhihu.com/p/121125182) · 知乎 · 2020-03-30 · 赞同 0**
> 力扣：[36. 有效的数独](https://leetcode.cn/problems/valid-sudoku/) · Medium · 灵茶山艾府：[记录每行每列每宫中的数字是否出现（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

36.有效的数独<https://leetcode-cn.com/problems/valid-sudoku/>

数独要求有四点：

1、每个格子上只能填一个数

2、每一行上同样的数字只能出现一次

3、每一列上同样的数字只能出现一次

4、每个小矩阵中同样的数字只能出现一次

首先题目的输入保证了要求1肯定成立。那么对于要求2、3、4，观察后可以发现一个n\*n的数独一定是n行，n列，n个小矩阵的，且其中填写的数字正好是1到n。那么可以维护三个n\*n的二维list，分别表示行、列以及小矩阵中数字的填充情况。接下来遍历所有的格子，然后更新这三个list即可。

例如对于第m行，第n列人的格子，设其中的数为x，那么

其所在行为m，因此将row[m][x - 1]置为True，表示第m行已经出现过了x。

其所在列为n，因此将column[n][x - 1]置为True，表示第n列已经出现过了x。

其所在小矩阵k \= m / 3 \* 3 + n / 3，因此将matrix[k][x - 1]置为True，表示第k个小矩阵中已经出现过了x。

如果在过程中发现要置为True的地方已经是True了，那么说明先前在这一行或这一列或这个小矩阵中已经填过了x，不能再填x进去了，那么返回False。

如果每个格子都没有与之前的冲突，那么返回True。

实际上，将数独转化为精确覆盖类问题，然后使用dacing-link求解是效率更高的做法。其主要思想是使用十字链表来表示行、列、小矩阵的填充情况，不过在这里就先不展开了。

最后附上python代码：

```python
class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """

        column = [[False for index in range(9)] for index in range(9)]
        row = [[False for index in range(9)] for index in range(9)]
        matrix = [[False for index in range(9)] for index in range(9)]

        for i, line in enumerate(board):
            for j, num in enumerate(line):
                if num != '.':
                    if column[j][int(num) - 1]:
                        return False
                    column[j][int(num) - 1] = True

                    if row[i][int(num) - 1]:
                        return False
                    row[i][int(num) - 1] = True

                    matrix_pos = i / 3 * 3 + j / 3
                    if matrix[matrix_pos][int(num) - 1]:
                        return False
                    matrix[matrix_pos][int(num) - 1] = True

        return True
```
