---
title: "3078. 矩阵中的字母数字模式匹配I"
aliases: ["yiduobo的每日leetcode 3078.矩阵中的字母数字模式匹配I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698215347"
zhihu_id: "698215347"
zhihu_title: "yiduobo的每日leetcode 3078.矩阵中的字母数字模式匹配I"
question_id: "3078"
question: "矩阵中的字母数字模式匹配I"
problem_url: "https://leetcode.cn/problems/match-alphanumerical-pattern-in-matrix-i/"
created: "2024-05-17T00:04:47+08:00"
updated: "2024-05-17T00:04:47+08:00"
upvotes: 0
comments: 0
---

# 3078. 矩阵中的字母数字模式匹配I

> **[yiduobo的每日leetcode 3078.矩阵中的字母数字模式匹配I](https://zhuanlan.zhihu.com/p/698215347) · 知乎 · 2024-05-17 · 赞同 0**
> 力扣：[3078. 矩阵中的字母数字模式匹配I](https://leetcode.cn/problems/match-alphanumerical-pattern-in-matrix-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3078.矩阵中的字母数组模式匹配I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/match-alphanumerical-pattern-in-matrix-i/description/)

题目的数据规模很小，完全可以直接暴力求解。从(0, 0)到(m - r, n - c)开始逐个枚举每个位置，检测以当前位置为左上角的子矩阵是否能形成匹配。

对于以(i, j)为左上角的子矩阵，遍历pattern中的每个字符，对于当前遍历到的pattern[x][y]，其在board中对应的字符应该是board[i + x][j + y]，接下来对于这两个字符：

1、pattern[x][y]是字符：

若pattern[x][y]没有建立过映射但board[x + i][y + j]已经被映射过，或者pattern[x][y]已建立的映射目标不是board[x + i][y + j]，那么就返回false，否则就建立pattern[x][y]到board[x + i][y + j]的映射。具体实现上，可以使用一个哈希表来建立映射，并使用另一个集合来储存已经被映射过的字符。

2、pattern[x][y]是数字：

此时只需检测pattern[x][y]和board[x + i][y + j]是否相等就行了

最后附上python代码：

```python
class Solution(object):
    def findPattern(self, board, pattern):
        """
        :type board: List[List[int]]
        :type pattern: List[str]
        :rtype: List[int]
        """

        m = len(board)
        n = len(board[0])

        r = len(pattern)
        c = len(pattern[0])

        def check(i, j):
            mapping = {}
            mapped = set()
            for x in range(r):
                for y in range(c):
                    if 'a' <= pattern[x][y] <= 'z':
                        if pattern[x][y] not in mapping:
                            if board[x + i][y + j] in mapped:
                                return False
                            mapping[pattern[x][y]] = board[x + i][y + j]
                            mapped.add(board[x + i][y + j])
                        elif mapping[pattern[x][y]] != board[x + i][y + j]:
                            return False
                    elif int(pattern[x][y]) != board[x + i][y + j]:
                        return False
            return True

        for i in range(m - r + 1):
            for j in range(n - c + 1):
                if check(i, j):
                    return [i, j]
        
        return [-1, -1]
```
