---
title: "2174. 通过翻转行或列来去除所有的1 II"
aliases: ["yiduobo的每日leetcode 2174.通过翻转行或列来去除所有的1 II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627400856"
zhihu_id: "627400856"
zhihu_title: "yiduobo的每日leetcode 2174.通过翻转行或列来去除所有的1 II"
question_id: "2174"
question: "通过翻转行或列来去除所有的1 II"
problem_url: "https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips-ii/"
created: "2023-05-07T02:14:22+08:00"
updated: "2023-05-07T02:14:22+08:00"
upvotes: 0
comments: 0
---

# 2174. 通过翻转行或列来去除所有的1 II

> **[yiduobo的每日leetcode 2174.通过翻转行或列来去除所有的1 II](https://zhuanlan.zhihu.com/p/627400856) · 知乎 · 2023-05-07 · 赞同 0**
> 力扣：[2174. 通过翻转行或列来去除所有的1 II](https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2174.通过翻转所有行或列来去除所有的1 II

[力扣](https://leetcode.cn/problems/remove-all-ones-with-row-and-column-flips-ii/)

没有什么特别好的思路，不过好在本题的数据规模比较小，可以使用状态压缩动态规划来求解。

对于矩阵中x行y列这个位置，可以认为是二进制数中的第x \* n + y位，这样一来就可以将这个01矩阵变为一个长度为m \* n的二进制数，从而使用状态压缩动态规划。

对于当前的状态state，首先将其中的1分离出来，并重新定位回原来矩阵中的位置。

接下来从这些1当中枚举当前这一轮准备翻转的1。对于其中的每个1，都需要枚举其所在的行和列，并将位于同行或同列的所有的1都整合到状态remove中，得到f[state] \= min(f[state], f[state ^ remove] + 1)。

最后附上python代码：

```python
class Solution(object):
    def removeOnes(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        f = [None] * (1 << (m * n))
        f[0] = 0

        def calc(now):
            if f[now] is None:
                f[now] = m * n
                one_set = set()
                for i in range(m):
                    for j in range(n):
                        state = 1 << (i * n + j)
                        if now & state == state:
                            one_set.add((i, j))

                for rx, ry in one_set:
                    remove = 1 << (rx * n + ry)
                    for i in range(m):
                        if (i, ry) in one_set:
                            remove |= 1 << (i * n + ry)
                    
                    for j in range(n):
                        if (rx, j) in one_set:
                            remove |= 1<< (rx * n + j)
                    
                    f[now] = min(f[now], calc(now ^ remove) + 1)
            
            return f[now]

        now = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    now |= 1 << (i * n + j)
        
        return calc(now)
```
