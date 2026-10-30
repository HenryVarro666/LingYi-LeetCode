---
title: "1970. 你能穿过矩阵的最后一天"
aliases: ["yiduobo的每日leetcode 1970.你能穿过矩阵的最后一天"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/union-find", "leetcode/recursion", "题单/常用数据结构", "题单/网格图", "题单/贪心算法", "题单/常用数据结构/七-并查集", "题单/网格图/一-网格图-DFS", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/495823455"
zhihu_id: "495823455"
zhihu_title: "yiduobo的每日leetcode 1970.你能穿过矩阵的最后一天"
question_id: "1970"
question: "你能穿过矩阵的最后一天"
problem_url: "https://leetcode.cn/problems/last-day-where-you-can-still-cross/"
difficulty: "Hard"
rating: 2124
created: "2022-04-09T20:24:01+08:00"
updated: "2022-04-09T20:24:01+08:00"
upvotes: 0
comments: 0
---

# 1970. 你能穿过矩阵的最后一天

> **[yiduobo的每日leetcode 1970.你能穿过矩阵的最后一天](https://zhuanlan.zhihu.com/p/495823455) · 知乎 · 2022-04-09 · 赞同 0**
> 力扣：[1970. 你能穿过矩阵的最后一天](https://leetcode.cn/problems/last-day-where-you-can-still-cross/) · Hard · 灵茶山艾府：[两种方法：逆序 / 正序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1970.你能穿过矩阵的最后一天

[力扣](https://leetcode-cn.com/problems/last-day-where-you-can-still-cross/)

看到问题最直观的想法就是二分，道理也很简单，时间越长，走过去的可能性就越低，因此可以直接二分答案，然后根据二分到的天数调整地图，从最上层开始向最下层进行bfs，判断当前情况下能否走通。这种做法的时间复杂度是O(mn \* log(mn))，前面的mn是bfs的复杂度，后面是二分的复杂度。

除此之外，还有一种倒推的做法，之前也有一题是类似的情况。具体思路就是一开始认为地图上全是水域，然后按照输入相反的顺序，将某些水域变成陆地。若某一块水域变成陆地之后可以走通了，那么反过来说明在这块陆地变成水域之前，这是最后一次走通的机会。

对于连通性的判断，在这里则可以使用并查集。当一个格子变成陆地时，枚举其相邻的格子，并通过并查集将这些格子合并到一起。

有一个需要注意的地方时，即使使用了并查集，如果每次判断连通性还是要枚举最上层每个格子和最小层每个格子的话，性能依然不过关。一种常见的处理方法是设置两个超级节点s和t。当最上层由水域变成陆地时，将s与对应的格子连通。同样的，当最下层由水域变成陆地时，将t与对应的格子连通，那么最终就只需要校验s和t是否连通。如果认为并查集的复杂度为O(1)的话，这种做法的时间复杂度就是O(mn)，比上面二分的做法要更好。

最后附上python代码：

```python
class Solution(object):
    def latestDayToCross(self, row, col, cells):
        """
        :type row: int
        :type col: int
        :type cells: List[List[int]]
        :rtype: int
        """

        self.fa = range(row * col + 2)
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        cells.reverse()
        used = set()
        res = row * col
        for nowx, nowy in cells:
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x <= row and y > 0 and y <= col and (x - 1) * col + y in used:
                    self.union((x - 1) * col + y, (nowx - 1) * col + nowy)
            
            if nowx == 1:
                self.union(0, (nowx - 1) * col + nowy)
            
            if nowx == row:
                self.union((nowx - 1) * col + nowy, row * col + 1)
            
            res -= 1
            if self.find(0) == row * col + 1:
                return res
    
            used.add((nowx - 1) * col + nowy)

    def find(self, x):
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        
        return self.fa[x]
    
    def union(self, x, y):
        fa_x = self.find(x)
        fa_y = self.find(y)
        if fa_x < fa_y:
            self.fa[fa_x] = fa_y
        else:
            self.fa[fa_y] = fa_x
```
