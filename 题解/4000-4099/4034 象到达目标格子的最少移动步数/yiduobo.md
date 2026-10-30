---
title: "4034. 象到达目标格子的最少移动步数"
aliases: ["yiduobo的每日leetcode 4034.象到达目标格子的最少移动步数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078258579346290027"
zhihu_id: "2078258579346290027"
zhihu_title: "yiduobo的每日leetcode 4034.象到达目标格子的最少移动步数"
question_id: "4034"
question: "象到达目标格子的最少移动步数"
problem_url: "https://leetcode.cn/problems/minimum-bishop-moves-to-reach-target/"
difficulty: "Medium"
created: "2026-09-02T00:58:29+08:00"
updated: "2026-09-02T00:58:29+08:00"
upvotes: 1
comments: 0
---

# 4034. 象到达目标格子的最少移动步数

> **[yiduobo的每日leetcode 4034.象到达目标格子的最少移动步数](https://zhuanlan.zhihu.com/p/2078258579346290027) · 知乎 · 2026-09-02 · 赞同 1**
> 力扣：[4034. 象到达目标格子的最少移动步数](https://leetcode.cn/problems/minimum-bishop-moves-to-reach-target/) · Medium · 灵茶山艾府：[至多走两步（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4034.象到达目标格子的最少移动步数

<https://leetcode.cn/problems/minimum-bishop-moves-to-reach-target/description/>

题目给出一个8 \* 8的棋盘，行和列的下标从1开始。

另外给出一个数组source \= [sr, sc]，表示象的起始位置，以及一个数组target \= [tr, tc]。在一步移动中，象可以在棋盘范围内沿着单个对角线方向移动任意数量的格子。

问象恰好到达target所需的最少移动次数。若无法到达，则返回-1。

从题目给出的样例可以看出来，若象一开始在白色格子上，那么无论怎么走，还是只能落在白色格子上，反之亦然。更形式化的说，就是无论象怎样行走，其坐标之和的奇偶性是不会产生变化的。理由也很直观，当象沿着左对角线走动时，横纵坐标每次都会同时加上k或者减去k，而沿着右对角线走动时，横纵坐标则是一个加上k，另一个减去k。

另一方面，对于同色的格子，则可以在不超过两步的操作内互相到达。若二者一开始就位于同一条左对角线或者右对角线上，那么就可以一步到位，否则的话也可以通过先左后右或者先右后左的顺序走到目标位置。

基于上面的结论，就可以先判断起点和终点下标之和的奇偶性是否相同，不同则直接返回-1。若相同，再判断是否处于同一对角线，在这里可以通过下标之和是否相等或者下标之差是否相等来进行判断。若处于，那么答案就是1，否则答案就是2。

最后附上python代码：

```python
class Solution(object):
    def minBishopMoves(self, source, target):
        """
        :type source: List[int]
        :type target: List[int]
        :rtype: int
        """
        
        if (source[0] + source[1]) % 2 != (target[0] + target[1]) % 2:
            return -1
        
        if source[0] + source[1] == target[0] + target[1] or source[0] - source[1] == target[0] - target[1]:
            return 1
        
        return 2
```
