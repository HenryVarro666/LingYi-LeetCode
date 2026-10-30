---
title: "2257. 统计网格图中没有被保卫的格子数"
aliases: ["yiduobo的每日leetcode 2257.统计网格图中没有被保卫的格子数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/547824112"
zhihu_id: "547824112"
zhihu_title: "yiduobo的每日leetcode 2257.统计网格图中没有被保卫的格子数"
question_id: "2257"
question: "统计网格图中没有被保卫的格子数"
problem_url: "https://leetcode.cn/problems/count-unguarded-cells-in-the-grid/"
difficulty: "Medium"
created: "2022-07-30T01:11:16+08:00"
updated: "2022-07-30T01:11:16+08:00"
upvotes: 0
comments: 0
---

# 2257. 统计网格图中没有被保卫的格子数

> **[yiduobo的每日leetcode 2257.统计网格图中没有被保卫的格子数](https://zhuanlan.zhihu.com/p/547824112) · 知乎 · 2022-07-30 · 赞同 0**
> 力扣：[2257. 统计网格图中没有被保卫的格子数](https://leetcode.cn/problems/count-unguarded-cells-in-the-grid/) · Medium · 灵茶山艾府：[遍历警卫及其视线（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2257.统计网格图中没有被保卫的格子数

[力扣](https://leetcode.cn/problems/count-unguarded-cells-in-the-grid/)

方便起见，在这里称呼既不是墙也不是警卫的单元格为普通单元格，其他的为特殊单元格。那么对于一个普通单元格而言，如果某个方向上最近的特殊单元格是警卫，那么这个单元格就可以被这个警卫保护。反过来，如果四个方向上最近的特殊单元格都是墙，或者一直到边界都没有特殊单元格，那么这个普通单元格就不会被保卫。

于是在这里可以从四个方向上分开来考虑，对于每个普通单元格，尝试找出特定方向上离这个单元格最近的特殊单元格。例如要找某个普通单元格左侧最近的特殊单元格，就可以从这个普通单元格所在的行从左到右遍历，同时使用一个变量记录最后一次出现的特殊单元格是什么。

如果遍历到的是普通单元格，那么这里记录的最后一次出现的特殊单元格就是这个单元格左侧最近的特殊单元格，可以根据其是否是警卫来更新当前普通单元格是否受到保护。

如果遍历到的是特殊单元格，那么当前单元格就是新的最后出现的特殊单元格了。

这样一来，就可以在一次遍历的时间内得到某一行的所有普通单元格是否可能受到左侧警卫的保护。更进一步地，如果对每一行都这么做，就可以得到矩阵中所有普通单元格是否能收到左侧警卫的保护。

那么按照同样的做法对每一行从右向左遍历，就可以知道每个普通单元格能否受到右侧警卫的保护。同样地，分别从上到下、从下到上遍历每一列，就能得到上方和下方相关的保卫信息。

全部遍历完成后，再统计矩阵中有多少普通单元格最终是受保护状态就行了。

虽然看上去做了多次遍历，但是每次的时间复杂度都是O(mn)，因此最终的时间复杂度就是O(mn)。

最后附上python代码：

```python
class Solution(object):
    def countUnguarded(self, m, n, guards, walls):
        """
        :type m: int
        :type n: int
        :type guards: List[List[int]]
        :type walls: List[List[int]]
        :rtype: int
        """

        f = [[0] * n for _ in range(m)]

        for x, y in walls:
            f[x][y] = 1

        for x, y in guards:
            f[x][y] = 2
        
        for x in range(m):
            flag = False
            for y in range(n):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3

            flag = False
            for y in range(n - 1, -1, -1):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3
        
        for y in range(n):
            flag = False
            for x in range(m):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3
            
            flag = False
            for x in range(m - 1, -1, -1):
                if f[x][y] == 1:
                    flag = False
                elif f[x][y] == 2:
                    flag = True
                elif flag:
                    f[x][y] = 3

        res = 0
        for x in range(m):
            for y in range(n):
                if f[x][y] == 0:
                    res += 1

        return res
```
