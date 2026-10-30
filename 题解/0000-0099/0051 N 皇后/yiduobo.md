---
title: "51. N皇后 & 52. N皇后 II"
aliases: ["yiduobo的每日leetcode 51.N皇后 && 52.N皇后 II", "51. N皇后", "52. N皇后 II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/126742437"
zhihu_id: "126742437"
zhihu_title: "yiduobo的每日leetcode 51.N皇后 && 52.N皇后 II"
question_id: ["51", "52"]
question: ["N 皇后", "N 皇后 II"]
problem_url: ["https://leetcode.cn/problems/n-queens/", "https://leetcode.cn/problems/n-queens-ii/"]
difficulty: "Hard"
created: "2020-04-07T22:35:39+08:00"
updated: "2020-04-07T22:38:44+08:00"
upvotes: 0
comments: 0
---

# 51. N皇后 & 52. N皇后 II

> **[yiduobo的每日leetcode 51.N皇后 && 52.N皇后 II](https://zhuanlan.zhihu.com/p/126742437) · 知乎 · 2020-04-07 · 赞同 0**
> 力扣：[51. N 皇后](https://leetcode.cn/problems/n-queens/) · Hard · 灵茶山艾府：[【视频讲解】排列型回溯，简洁高效！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[52. N 皇后 II](https://leetcode.cn/problems/n-queens-ii/) · Hard · 灵茶山艾府：[【视频讲解】排列型回溯，简洁高效！附题单（Python/Java/C++/C/Go/JS/Rust）](../0052%20N%20皇后%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

51.N皇后<https://leetcode-cn.com/problems/n-queens/>

52.N皇后 II<https://leetcode-cn.com/problems/n-queens-ii/>

经典的递归回溯问题，一个求全部的解，一个求解的个数，本质做法是一样的。

对于放在第i行第j列的棋子，其覆盖掉了第i行，第j列，以及一条左斜线和一条右斜线。

观察同一左斜线上的点，例如(0, 2), (1, 1), (2, 0)，可以发现同一左斜线满足i+ j相等。

类似地，观察同一右斜线上的点可以发现满足i - j相等。需要注意的是这里的i - j可能小于0，那么在具体实现的时候需要统一加上n - 1，使其大于等于0。

于是可以按行搜索，枚举每一行中可以放皇后的位置，更新列、左斜线以及右斜线的覆盖情况，然后继续搜索下一行。这里还需要注意一个n \* n的棋盘存在2 \* n - 1条左斜线和右斜线。

最后附上51题求全部解得python代码，其中column、left_slash、right_slash分别代表列、左斜线以及右斜线的覆盖情况：

```python
class Solution(object):
    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """

        res_list = []

        column = [False] * n
        left_slash = [False] * (n + n - 1)
        right_slash = [False] * (n + n - 1)

        now = []

        self.dfs(n, 0, now, column, left_slash, right_slash, res_list)

        res_str_list = []
        for res in res_list:
            res_str = []
            for pos in res:
                res_str.append('.' * pos + 'Q' + '.' * (n - 1 - pos))
            res_str_list.append(res_str)
        return res_str_list

    def dfs(self, n, level, now, column, left_slash, right_slash, res_list):
        if n == level:
            res_list.append(now[:])
            return

        for index in range(n):
            if not (column[index] or left_slash[index + level] or right_slash[level - index + n - 1]):
                now.append(index)
                column[index] = True
                left_slash[index + level] = True
                right_slash[level - index + n - 1] = True
                self.dfs(n, level + 1, now, column, left_slash, right_slash, res_list)
                right_slash[level - index + n - 1] = False
                left_slash[index + level] = False
                column[index] = False
                now.pop()
```
