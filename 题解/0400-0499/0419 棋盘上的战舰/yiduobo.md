---
title: "419. 甲板上的战舰"
aliases: ["yiduobo的每日leetcode 419.甲板上的战舰"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/191626227"
zhihu_id: "191626227"
zhihu_title: "yiduobo的每日leetcode 419.甲板上的战舰"
question_id: "419"
question: "棋盘上的战舰"
problem_url: "https://leetcode.cn/problems/battleships-in-a-board/"
difficulty: "Medium"
created: "2020-08-20T22:14:44+08:00"
updated: "2020-08-20T22:14:44+08:00"
upvotes: 0
comments: 0
---

# 419. 甲板上的战舰

> **[yiduobo的每日leetcode 419.甲板上的战舰](https://zhuanlan.zhihu.com/p/191626227) · 知乎 · 2020-08-20 · 赞同 0**
> 力扣：[419. 棋盘上的战舰](https://leetcode.cn/problems/battleships-in-a-board/) · Medium · 灵茶山艾府：[一次遍历，枚举战舰起点（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

419.甲板上的战舰<https://leetcode-cn.com/problems/battleships-in-a-board/>

题目要求一趟扫描就找出所有的战舰，那么对于每艘战舰都只能计算一次，因此需要对每艘战舰都找到一个标志点，只有碰到标志点时才计数。由于题目保证战舰是水平或竖直摆放，且战舰不会相交，那么可以将竖直战舰的顶部以及水平战舰的左侧作为标志点。

于是现在的做法就是一趟扫描，对于每个点，若该点为X，说明其为战舰上的一点。若该点的左侧也是X，那么说明该点是水平战舰上的某个点，且不是标志点。若该点上面也是X，那么说明该点是竖直战舰上的某个点，且不是标志点。这两种情况下都直接跳过，否则的话这个点必然是水平或竖直战舰的顶部。

最后附上python代码：

```python
class Solution(object):
    def countBattleships(self, board):
        """
        :type board: List[List[str]]
        :rtype: int
        """

        res = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 'X':
                    if i > 0 and board[i - 1][j] == 'X':
                        continue
                    if j > 0 and board[i][j - 1] == 'X':
                        continue
                    res += 1

        return res
```
