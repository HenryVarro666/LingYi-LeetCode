---
title: "2018. 判断单词是否能放入填字游戏内"
aliases: ["yiduobo的每日leetcode 2018.判断单词是否能放入填字游戏内"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/506279770"
zhihu_id: "506279770"
zhihu_title: "yiduobo的每日leetcode 2018.判断单词是否能放入填字游戏内"
question_id: "2018"
question: "判断单词是否能放入填字游戏内"
problem_url: "https://leetcode.cn/problems/check-if-word-can-be-placed-in-crossword/"
difficulty: "Medium"
created: "2022-04-27T23:09:21+08:00"
updated: "2022-04-27T23:09:21+08:00"
upvotes: 0
comments: 0
---

# 2018. 判断单词是否能放入填字游戏内

> **[yiduobo的每日leetcode 2018.判断单词是否能放入填字游戏内](https://zhuanlan.zhihu.com/p/506279770) · 知乎 · 2022-04-27 · 赞同 0**
> 力扣：[2018. 判断单词是否能放入填字游戏内](https://leetcode.cn/problems/check-if-word-can-be-placed-in-crossword/) · Medium · 灵茶山艾府：[遍历两个 # 之间的字符](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2018.判断单词是否能放入填字游戏内

[力扣](https://leetcode-cn.com/problems/check-if-word-can-be-placed-in-crossword/)

没有想到什么特别好的做法，只能老老实实按行按列来进行匹配。

首先是按行。枚举每一行，对于当前行，从行首开始找到第一个不是障碍的字符。接下来从这个字符开始尝试与word进行匹配，这里需要注意的是题目准许正序或者逆序匹配。

若匹配成功，则还需要检测当前是否来到了该行的末尾，或者下一个字符是障碍。如果满足，那么说明找到了答案。对于其他不满足条件的情况，由于前面这些字符已经没有用了，题目又要求是恰好填进去，因此接下来就可以直接跳过这些字符，找到下一个障碍所在的位置，然后从这个障碍开始向后找到第一个不是障碍的字符，然后重复此过程，直到匹配成功或者来的行末。

对于列的情况，做法也类似，只需将坐标转换一下即可。

最后附上python代码：

```python
class Solution(object):
    def placeWordInCrossword(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """

        m = len(board)
        n = len(board[0])
        l = len(word)

        for i in range(m):
            j = 0
            while j + l - 1 < n:
                while j + l - 1 < n and board[i][j] == '#':
                    j += 1
                if j + l - 1 >= n:
                    break

                flag1 = flag2 = True
                for p in range(l):
                    if board[i][j + p] == ' ':
                        continue
                    if board[i][j + p] != word[p]:
                        flag1 = False
                    if board[i][j + p] != word[l - p - 1]:
                        flag2 = False
                    if not flag1 and not flag2:
                        break

                
                if (flag1 or flag2) and (j + l == n or board[i][j + l] == '#'):
                    return True
                
                j += p
                while j + l - 1 < n and board[i][j] != '#':
                    j += 1
        
        for j in range(n):
            i = 0
            while i + l - 1 < m:
                while i + l - 1 < m and board[i][j] == '#':
                    i += 1
                if i + l - 1 >= m:
                    break

                flag1 = flag2 = True
                for p in range(l):
                    if board[i + p][j] == ' ':
                        continue
                    if board[i + p][j] != word[p]:
                        flag1 = False
                    if board[i + p][j] != word[l - p - 1]:
                        flag2 = False
                    if not flag1 and not flag2:
                        break
                
                if (flag1 or flag2) and (i + l == m or board[i + l][j] == '#'):
                    return True
                
                i += p
                while i + l - 1 < m and board[i][j] != '#':
                    i += 1
        
        return False
```
