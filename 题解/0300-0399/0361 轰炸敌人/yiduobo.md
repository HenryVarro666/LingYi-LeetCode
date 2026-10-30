---
title: "361. 轰炸敌人"
aliases: ["yiduobo的每日leetcode 361.轰炸敌人"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597861507"
zhihu_id: "597861507"
zhihu_title: "yiduobo的每日leetcode 361.轰炸敌人"
question_id: "361"
question: "轰炸敌人"
problem_url: "https://leetcode.cn/problems/bomb-enemy/"
created: "2023-01-10T00:47:04+08:00"
updated: "2023-01-10T00:47:04+08:00"
upvotes: 0
comments: 0
---

# 361. 轰炸敌人

> **[yiduobo的每日leetcode 361.轰炸敌人](https://zhuanlan.zhihu.com/p/597861507) · 知乎 · 2023-01-10 · 赞同 0**
> 力扣：[361. 轰炸敌人](https://leetcode.cn/problems/bomb-enemy/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

361.轰炸敌人

[力扣](https://leetcode.cn/problems/bomb-enemy/)

最直观的思路自然是枚举每个空地，然后计算将炸弹放在当前空地上最多可以杀伤的敌人。需要注意的是，如果每次从这个位置开始向四个方向遍历，计算可以杀伤的敌人的话，时间复杂度会比较吃紧。

另一种思路则是一开始先分别预处理出在每个格子放置炸弹时，在四个方向上可以杀伤的敌人。具体实现上，可以使用类似动态规划的处理方式。

以杀伤左侧的敌人举例。cnt表示当前单元格左侧没有被墙壁阻隔的敌人数量，那么对于当前单元格grid[i][j]：

1、若grid[i][j]是墙壁，那么之前左侧的敌人都被这堵墙壁阻隔开了，因此需要将cnt清零。另外，当前单元格不允许放置炸弹

2、若grid[i][j]是敌人，那么应该将cnt加上1。同样的，当前单元格也不允许放置炸弹

3、若grid[i][j]是空格，那么就有left[i][j] \= cnt，这里的left[i][j]表示在单元格(i, j)放置炸弹时可以杀伤的左侧敌人的数量

按照与计算左侧相同的方式计算右侧、上方、下方的情况，最后再枚举放置炸弹的地点，通过预处理的结果计算最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxKilledEnemies(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        left = [[0] * n for _ in range(m)]
        right = [[0] * n for _ in range(m)]
        up = [[0] * n for _ in range(m)]
        down = [[0] * n for _ in range(m)]

        for i in range(m):
            cnt = 0
            for j in range(n):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    left[i][j] = cnt
            
            cnt = 0
            for j in range(n - 1, -1, -1):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    right[i][j] = cnt
        
        for j in range(n):
            cnt = 0
            for i in range(m):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    up[i][j] = cnt
            
            cnt = 0
            for i in range(m - 1, -1, -1):
                if grid[i][j] == 'W':
                    cnt = 0
                elif grid[i][j] == 'E':
                    cnt += 1
                else:
                    down[i][j] = cnt
        
        res = 0
        for i in range(m):
            for j in range(n):
                res = max(res, left[i][j] + right[i][j] + up[i][j] + down[i][j])
        return res
```
