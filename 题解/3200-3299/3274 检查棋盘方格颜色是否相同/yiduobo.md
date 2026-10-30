---
title: "3274. 检查棋盘方格颜色是否相同"
aliases: ["yiduobo的每日leetcode 3274.检查棋盘方格颜色是否相同"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794177912"
zhihu_id: "794177912"
zhihu_title: "yiduobo的每日leetcode 3274.检查棋盘方格颜色是否相同"
question_id: "3274"
question: "检查棋盘方格颜色是否相同"
problem_url: "https://leetcode.cn/problems/check-if-two-chessboard-squares-have-the-same-color/"
difficulty: "Easy"
created: "2024-10-02T04:18:02+08:00"
updated: "2024-10-02T04:18:02+08:00"
upvotes: 0
comments: 0
---

# 3274. 检查棋盘方格颜色是否相同

> **[yiduobo的每日leetcode 3274.检查棋盘方格颜色是否相同](https://zhuanlan.zhihu.com/p/794177912) · 知乎 · 2024-10-02 · 赞同 0**
> 力扣：[3274. 检查棋盘方格颜色是否相同](https://leetcode.cn/problems/check-if-two-chessboard-squares-have-the-same-color/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3274.检查棋盘方格颜色是否相同

[. - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-two-chessboard-squares-have-the-same-color/description/)

题目给出8 \* 8的国际象棋棋盘以及两个坐标，国际象棋棋盘由黑白两种颜色构成，其中左下角的颜色为黑色，且所有相邻位置的颜色都互不相同。问给出的两个坐标的颜色是否相同。

棋盘是奇偶性问题常见的背景板，棋盘中行列坐标之和为偶数的单元格都是同一种颜色，而和为奇数的单元格则是另一种颜色。

接下来对于本题，若两组坐标的坐标之和的奇偶性相同，那么这两个坐标就同色，否则就不同。更进一步的，坐标之和的奇偶性是否相同，则又可以通过坐标之和的和的奇偶性来进行判断，也就是说，只需累加四个坐标，判断是否为偶数，若为偶数则颜色相同，否则不同。

最后附上python代码：

```python
class Solution(object):
    def checkTwoChessboards(self, coordinate1, coordinate2):
        """
        :type coordinate1: str
        :type coordinate2: str
        :rtype: bool
        """

        x1 = ord(coordinate1[0]) - 96
        y1 = int(coordinate1[1])

        x2 = ord(coordinate2[0]) - 96
        y2 = int(coordinate2[1])

        return (x1 + y1 + x2 + y2) % 2 == 0
```
