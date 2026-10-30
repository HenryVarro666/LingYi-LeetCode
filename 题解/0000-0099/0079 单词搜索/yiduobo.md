---
title: "79. 单词搜索"
aliases: ["yiduobo的每日leetcode 79.单词搜索"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133840036"
zhihu_id: "133840036"
zhihu_title: "yiduobo的每日leetcode 79.单词搜索"
question_id: "79"
question: "单词搜索"
problem_url: "https://leetcode.cn/problems/word-search/"
difficulty: "Medium"
created: "2020-04-20T21:31:53+08:00"
updated: "2020-04-20T21:31:53+08:00"
upvotes: 0
comments: 0
---

# 79. 单词搜索

> **[yiduobo的每日leetcode 79.单词搜索](https://zhuanlan.zhihu.com/p/133840036) · 知乎 · 2020-04-20 · 赞同 0**
> 力扣：[79. 单词搜索](https://leetcode.cn/problems/word-search/) · Medium · 灵茶山艾府：[极致优化！代码击败接近 100%！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

79.单词搜索<https://leetcode-cn.com/problems/word-search/>

还是搜索回溯的题目。如果board中的词有长度限制，或者不可以拐弯的话（例如word puzzle之类的东西），也可以考虑用自动机来求解，但是这里没有这些限制，因此只能老老实实用搜索回溯了。

对于当前位置(x，y)，下一步可以选择(x - 1, y)，(x, y - 1)，(x + 1, y)，(x, y +1)这四个点。当然，需要满足这些点的字符能与word中的字符对上，且没有被使用过。我的做法是将使用过的点置为None，然后在判断字符是否能与word中的字符对上时就起到了去重的作用。

接下就是在board中枚举word的起点，然后开始搜索，每次探索四个方向上的点，如果合法则将其加入到now中，然后进行下一步探索。

最后附上python代码：

```python
class Solution(object):
    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """

        if not board:
            return False

        if not word:
            return True

        move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for i, line in enumerate(board):
            for j, char in enumerate(line):
                if char == word[0]:
                    tmp = board[i][j]
                    board[i][j] = None
                    if self.dfs(1, board, i, j, move, word):
                        return True
                    board[i][j] = tmp

        return False

    def dfs(self, level, board, x, y, move, word):
        if level == len(word):
            return True
        
        for index in range(len(move)):
            dx = x + move[index][0]
            dy = y + move[index][1]
            if dx >= 0 and dx < len(board) and dy >= 0 and dy < len(board[0]) and board[dx][dy] == word[level]:
                tmp = board[dx][dy]
                board[dx][dy] = None
                if self.dfs(level + 1, board, dx, dy, move, word):
                    return True
                board[dx][dy] = tmp
        
        return False
```
