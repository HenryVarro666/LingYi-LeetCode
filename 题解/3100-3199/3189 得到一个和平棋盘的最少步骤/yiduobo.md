---
title: "3189. 得到一个和平棋盘的最少步骤"
aliases: ["yiduobo的每日leetcode 3189.得到一个和平棋盘的最少步骤"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706305461"
zhihu_id: "706305461"
zhihu_title: "yiduobo的每日leetcode 3189.得到一个和平棋盘的最少步骤"
question_id: "3189"
question: "得到一个和平棋盘的最少步骤"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-get-a-peaceful-board/"
created: "2024-07-01T00:34:06+08:00"
updated: "2024-07-01T00:34:06+08:00"
upvotes: 1
comments: 0
---

# 3189. 得到一个和平棋盘的最少步骤

> **[yiduobo的每日leetcode 3189.得到一个和平棋盘的最少步骤](https://zhuanlan.zhihu.com/p/706305461) · 知乎 · 2024-07-01 · 赞同 1**
> 力扣：[3189. 得到一个和平棋盘的最少步骤](https://leetcode.cn/problems/minimum-moves-to-get-a-peaceful-board/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3189.得到一个和平棋盘的最少步骤

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-moves-to-get-a-peaceful-board/description/)

题目给出一块大小为n \* n的棋盘以及棋盘上n个车的坐标，每一次操作可以将任意一个车在水平或竖直方向上移动一格，问最少需要多少次移动才能使得每行每列上仅有一个车。

首先可以明确的是，行和列之间是不会互相影响的，因此可以将行和列分开考虑。在这里不妨从行入手。

对于第0行，有三种情况：

1、第0行目前没有车。此时需要从第1行移动一个过来

2、第0行目前恰好有1个车。此时不需要针对第0行进行任何操作

3、第0行目前有超过1个车。此时需要将多出的车都移动到第1行

无论是哪种情况，都可以认为是第0行一开始有x个车，将其中x - 1个移动到第1行，如果是负数则表示从第1行借车。接下来只需按照相同的处理方式完成第1行到第n - 1行的移动即可。

对于列也可以如法炮制，于是只需遍历所有的车，计算初始情况下每一行和每一列有多少个车。接下来从第0行遍历到第n - 1行，从第0列遍历到第n - 1列，计算当前行/列与下一行/列交互产生的操作数，累加到答案中即可。

值得一提的是，这种算法实际上计算的是操作数的下限，而对于本题，由于移动是一步一步进行的，同时没有额外的限制，那么就必然有办法构造出想要的状态，即达到这个下限。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, rooks):
        """
        :type rooks: List[List[int]]
        :rtype: int
        """

        n = len(rooks)
        row = [0] * n
        col = [0] * n
        for x, y in rooks:
            row[x] += 1
            col[y] += 1
        
        res = 0
        for index in range(n - 1):
            row[index] -= 1
            res += abs(row[index])
            row[index + 1] += row[index]
            
            col[index] -= 1
            res += abs(col[index])
            col[index + 1] += col[index]
        
        return res
```
