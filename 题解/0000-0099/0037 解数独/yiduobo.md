---
title: "37. 解数独"
aliases: ["yiduobo的每日leetcode 37.解数独"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/backtracking", "leetcode/heap-priority-queue", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/121812575"
zhihu_id: "121812575"
zhihu_title: "yiduobo的每日leetcode 37.解数独"
question_id: "37"
question: "解数独"
problem_url: "https://leetcode.cn/problems/sudoku-solver/"
difficulty: "Hard"
created: "2020-03-31T22:10:49+08:00"
updated: "2020-03-31T22:10:49+08:00"
upvotes: 0
comments: 0
---

# 37. 解数独

> **[yiduobo的每日leetcode 37.解数独](https://zhuanlan.zhihu.com/p/121812575) · 知乎 · 2020-03-31 · 赞同 0**
> 力扣：[37. 解数独](https://leetcode.cn/problems/sudoku-solver/) · Hard · 灵茶山艾府：[数独怎么玩，题目就怎么做：回溯+堆优化（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

37.解数独<https://leetcode-cn.com/problems/sudoku-solver/>

经典的搜索回溯问题。具体思路是每一轮先扫描整个数独：

(1)如果都填满了，那么当前的填法就是答案，直接返回。

(2)如果存在一个未填充的格子中已经无法填数字进去了，那么说明当前情况是错的，回溯。

(3)否则找出剩下可以填的数字最少的格子，选择一个数字填进去，并修正同一行、同一列、同一个小矩阵中其他未填充格子中可以填的数字，然后继续进行下一轮搜索。

当然，使用dancing links的话这里的操作就变成了链表的遍历以及删除节点，效率会更高，因为链表的规模实在不断缩小的。

由于dacing links实现起来比较麻烦，所以这里选择了基本的搜索回溯法。

最后附上python代码，其中dfs为搜索过程，dfs中的两重循环为寻找可以填的数字最少的格子，之后的循环则是枚举这个格子中填写的数字，并修正其他未填充格子中可以填的数字：

```python
class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """

        column = [[False for index in range(9)] for index in range(9)]
        row = [[False for index in range(9)] for index in range(9)]
        matrix = [[False for index in range(9)] for index in range(9)]
        finish_flag = True
        for i, line in enumerate(board):
            for j, num in enumerate(line):
                if num != '.':
                    num = int(num)
                    column[j][num - 1] = True
                    row[i][num - 1] = True
                    matrix_pos = i / 3 * 3 + j / 3
                    matrix[matrix_pos][num - 1] = True

        self.dfs(board, column, row, matrix)

    def dfs(self, board, column, row, matrix):
        min_choice = 10
        min_choice_row = -1
        min_choice_column = -1

        finish_flag = True
        for i, line in enumerate(board):
            for j, num in enumerate(line):
                matrix_pos = i / 3 * 3 + j / 3
                if num == '.':
                    finish_flag = False
                    choice = 0
                    for choice_num in range(9):
                        if not column[j][choice_num] and not row[i][choice_num] and not matrix[matrix_pos][choice_num]:
                            choice += 1
                    if choice == 0:
                        return False
                    if choice < min_choice:
                        min_choice = choice
                        min_choice_row = i
                        min_choice_column = j
                    
        if finish_flag:
            return True

        choice_matrix = min_choice_row / 3 * 3 + min_choice_column / 3
        for choice_num in range(9):
            if not column[min_choice_column][choice_num] and not row[min_choice_row][choice_num] and not matrix[choice_matrix][choice_num]:
                board[min_choice_row][min_choice_column] = str(choice_num + 1)
                column[min_choice_column][choice_num] = True
                row[min_choice_row][choice_num] = True
                matrix[choice_matrix][choice_num] = True
                finish_flag = self.dfs(board, column, row, matrix)
                if finish_flag:
                    return True
                board[min_choice_row][min_choice_column] = '.'
                column[min_choice_column][choice_num] = False
                row[min_choice_row][choice_num] = False
                matrix[choice_matrix][choice_num] = False
                
        return False
```
