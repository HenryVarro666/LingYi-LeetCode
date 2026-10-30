---
title: "4061. 皇后到达目标格子的最少移动步数"
aliases: ["yiduobo的每日leetcode 4061.皇后到达目标格子的最少移动步数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088029749750900146"
zhihu_id: "2088029749750900146"
zhihu_title: "yiduobo的每日leetcode 4061.皇后到达目标格子的最少移动步数"
question_id: "4061"
question: "皇后到达目标格子的最少移动步数"
problem_url: "https://leetcode.cn/problems/minimum-queen-moves-to-reach-target/"
difficulty: "Easy"
created: "2026-09-28T22:22:58+08:00"
updated: "2026-09-28T22:22:58+08:00"
upvotes: 2
comments: 0
---

# 4061. 皇后到达目标格子的最少移动步数

> **[yiduobo的每日leetcode 4061.皇后到达目标格子的最少移动步数](https://zhuanlan.zhihu.com/p/2088029749750900146) · 知乎 · 2026-09-28 · 赞同 2**
> 力扣：[4061. 皇后到达目标格子的最少移动步数](https://leetcode.cn/problems/minimum-queen-moves-to-reach-target/) · Easy · 灵茶山艾府：[至多走两步（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4061.皇后到达目标格子的最少移动步数

<https://leetcode.cn/problems/minimum-queen-moves-to-reach-target/description/>

题目给出一个8 \* 8的空棋盘，其中行和列的下标从1开始。

另外给出一个数组source \= [sr, sc]，表示皇后的初始位置，以及一个数组target \= [tr, tc]，表示目标位置。

在一次移动中，皇后可以在棋盘范围内沿单条行、列或者对角线移动一个或多个格子。

问皇后落在target所需的最小移动次数。

首先，若source和target一开始就相同，那么答案显然就是0。

接下来，若source与target在同一行、列或者对角线上时，答案显然就是1。同行同列是非常容易判断的，而对于对角线，若为左上到右下的对角线，同一条对角线上横纵坐标之差相等，若为右上到左下的对角线，同一条对角线上横纵坐标之和相等。

若都不符合，那么答案就是2，最简单的走法自然是先走一步使得处于同一行，再走一步使得处于同一列。

最后附上python代码：

```python
class Solution(object):
    def minQueenMoves(self, source, target):
        """
        :type source: List[int]
        :type target: List[int]
        :rtype: int
        """
        
        if source == target:
            return 0
        
        if source[0] == target[0] or source[1] == target[1] or source[0] + source[1] == target[0] + target[1] or source[0] - source[1] == target[0] - target[1]:
            return 1
        
        return 2
```
