---
title: "2596. 检查骑士巡视方案"
aliases: ["yiduobo的每日leetcode 2596.检查骑士巡视方案"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643959911"
zhihu_id: "643959911"
zhihu_title: "yiduobo的每日leetcode 2596.检查骑士巡视方案"
question_id: "2596"
question: "检查骑士巡视方案"
problem_url: "https://leetcode.cn/problems/check-knight-tour-configuration/"
difficulty: "Medium"
created: "2023-07-17T01:54:19+08:00"
updated: "2023-07-17T01:54:19+08:00"
upvotes: 0
comments: 0
---

# 2596. 检查骑士巡视方案

> **[yiduobo的每日leetcode 2596.检查骑士巡视方案](https://zhuanlan.zhihu.com/p/643959911) · 知乎 · 2023-07-17 · 赞同 0**
> 力扣：[2596. 检查骑士巡视方案](https://leetcode.cn/problems/check-knight-tour-configuration/) · Medium · 灵茶山艾府：[按题意模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2596.检查骑士巡视方案

[力扣](https://leetcode.cn/problems/check-knight-tour-configuration/)

由于题目的数据规模很小，那么完全可以遍历整个棋盘，将棋盘上的所有位置都收集起来，并按照其对应的数字从小到大排列。具体实现时，可以利用这个数组作为数组的下标省去排序这一步。

得到这个序列后，首先检测起点是否为(0, 0)。接下来，从下标1开始向后遍历，每次检测当前位置是否能从序列的上一个位置跳跃过来，也就是横坐标之差dx以及纵坐标之差dy中，有一个绝对值为1，另一个绝对值为2。若中途出现了不满足的情况，说明当前位置无法从上一个位置跳过来，此时直接false。若遍历完成，则返回true。

最后附上python代码：

```python
class Solution(object):
    def checkValidGrid(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """

        n = len(grid)
        path = [[None, None] for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                index = grid[i][j]
                path[index][0] = i
                path[index][1] = j

        if path[0][0] != 0 or path[0][1] != 0:
            return False

        for i in range(1, n * n):
            dx = path[i][0] - path[i - 1][0]
            dy = path[i][1] - path[i - 1][1]
            if (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2):
                continue
            return False
        
        return True
```
