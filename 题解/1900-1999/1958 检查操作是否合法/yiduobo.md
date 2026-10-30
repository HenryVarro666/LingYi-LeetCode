---
title: "1958. 检查操作是否合法"
aliases: ["yiduobo的每日leetcode 1958.检查操作是否合法"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/493103871"
zhihu_id: "493103871"
zhihu_title: "yiduobo的每日leetcode 1958.检查操作是否合法"
question_id: "1958"
question: "检查操作是否合法"
problem_url: "https://leetcode.cn/problems/check-if-move-is-legal/"
difficulty: "Medium"
created: "2022-04-04T22:01:32+08:00"
updated: "2022-04-04T22:01:32+08:00"
upvotes: 0
comments: 0
---

# 1958. 检查操作是否合法

> **[yiduobo的每日leetcode 1958.检查操作是否合法](https://zhuanlan.zhihu.com/p/493103871) · 知乎 · 2022-04-04 · 赞同 0**
> 力扣：[1958. 检查操作是否合法](https://leetcode.cn/problems/check-if-move-is-legal/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1958.检查操作是否合法

[力扣](https://leetcode-cn.com/problems/check-if-move-is-legal/)

题目要求涂色的方块是好线段的某一侧，那么可以从涂色的这一块开始，向八个方向延伸，直到抵达边界、抵达同色色块或者抵达空白色块停止。其中只有抵达同色色块这种情况才可能形成好线段。

另一方面，好线段需要两端同色快之间必须存在一个异色色块，因此只需要判断停止的色块位置是否与起始位置相邻，若不相邻，说明这是一个好线段。

最后附上python代码：

```python
class Solution(object):
    def checkMove(self, board, rMove, cMove, color):
        """
        :type board: List[List[str]]
        :type rMove: int
        :type cMove: int
        :type color: str
        :rtype: bool
        """

        dx = [-1, -1, 0, 1, 1, 1, 0, -1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
        m = len(board)
        n = len(board[0])
        for index in range(8):
            nowx, nowy = rMove + dx[index], cMove + dy[index]
            flag = False
            while nowx >= 0 and nowx < m and nowy >= 0 and nowy < n:
                if board[nowx][nowy] == '.':
                    break
                if board[nowx][nowy] == color:
                    flag = True
                    break
                nowx += dx[index]
                nowy += dy[index]
            
            if flag and ((nowx != rMove + dx[index]) or (nowy != cMove + dy[index])):
                return True
        
        return False
```
