---
title: "1391. 检查网络中是否存在有效路径"
aliases: ["yiduobo的每日leetcode 1391.检查网络中是否存在有效路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/recursion", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403983933"
zhihu_id: "403983933"
zhihu_title: "yiduobo的每日leetcode 1391.检查网络中是否存在有效路径"
question_id: "1391"
question: "检查网格中是否存在有效路径"
problem_url: "https://leetcode.cn/problems/check-if-there-is-a-valid-path-in-a-grid/"
difficulty: "Medium"
rating: 1746
created: "2021-08-26T23:25:55+08:00"
updated: "2021-08-26T23:25:55+08:00"
upvotes: 0
comments: 0
---

# 1391. 检查网络中是否存在有效路径

> **[yiduobo的每日leetcode 1391.检查网络中是否存在有效路径](https://zhuanlan.zhihu.com/p/403983933) · 知乎 · 2021-08-26 · 赞同 0**
> 力扣：[1391. 检查网格中是否存在有效路径](https://leetcode.cn/problems/check-if-there-is-a-valid-path-in-a-grid/) · Medium · 灵茶山艾府：[利用方向向量简化代码逻辑（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1391.检查网络中是否存在有效路径

[力扣](https://leetcode-cn.com/problems/check-if-there-is-a-valid-path-in-a-grid/)

没有什么特别好的思路，只好使用模拟法。需要注意的是，在模拟过程中除了常规的维护当前位置(x, y)之外，还需要额外维护方向，表示上一步是从哪个方向走到当前格子的。

接下来，对于6种道路，构造三个数组dx、dy以及dd，其中index对应的是走过第index种道路后状态的变化，具体来说就是对于状态(x, y, d)，走过第index种道路后将变为

(x + dx[index], y + dy[index], dd[index])

需要注意的是，这里的新位置不能走出地图，同时不应该走回到原来走过的位置。另外，道路的方向必须与当前状态的方向匹配。

最后附上python代码：

```python
class Solution(object):
    def hasValidPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        if m == 1 and n == 1:
            return True
            
        used = [[False] * n for _ in range(m)]
        used[0][0] = True
        q = []
        if (grid[0][0] == 1 or grid[0][0] == 4 or grid[0][0] == 6) and n > 1:
            q.append([0, 1, 0])
            used[0][1] = True
        if (grid[0][0] == 2 or grid[0][0] == 3 or grid[0][0] == 4) and m > 1:
            q.append([1, 0, 1])
            used[1][0] = True
        
        l, r = 0, len(q)
        dx = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 1, 0, -1],
              [1, 0, 0, 0],
              [0, 0, 1, 0],
              [-1, 0, 0, 0],
              [0, 0, -1, 0]]
        dy = [[0, 0, 0, 0],
              [1, 0, -1, 0],
              [0, 0, 0, 0],
              [0, 0, 0, -1],
              [0, 0, 0, 1],
              [0, -1, 0, 0],
              [0, 1, 0, 0]]
        dd = [[0, 0, 0, 0],
              [0, -1, 2, -1],
              [-1, 1, -1, 3],
              [1, -1, -1, 3],
              [-1, -1, 1, 0],
              [3, 2, -1, -1],
              [-1, 0, 3, -1]]

        while l < r:
            nowx, nowy, nowd = q[l]
            l += 1
            index = grid[nowx][nowy]
            x = nowx + dx[index][nowd]
            y = nowy + dy[index][nowd]
            d = dd[index][nowd]
            if d >= 0 and x >= 0 and x < m and y >= 0 and y < n and not used[x][y]:
                q.append([x, y, d])
                used[x][y] = True
                r += 1
                if x == m - 1 and y == n - 1 and dd[grid[x][y]][d] >= 0:
                    return True
        
        return False
```
