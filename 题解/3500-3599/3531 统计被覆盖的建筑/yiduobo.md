---
title: "3531. 统计被覆盖的建筑"
aliases: ["yiduobo的每日leetcode 3531.统计被覆盖的建筑"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904716054166483461"
zhihu_id: "1904716054166483461"
zhihu_title: "yiduobo的每日leetcode 3531.统计被覆盖的建筑"
question_id: "3531"
question: "统计被覆盖的建筑"
problem_url: "https://leetcode.cn/problems/count-covered-buildings/"
difficulty: "Medium"
created: "2025-05-14T22:06:23+08:00"
updated: "2025-05-14T22:06:23+08:00"
upvotes: 1
comments: 0
---

# 3531. 统计被覆盖的建筑

> **[yiduobo的每日leetcode 3531.统计被覆盖的建筑](https://zhuanlan.zhihu.com/p/1904716054166483461) · 知乎 · 2025-05-14 · 赞同 1**
> 力扣：[3531. 统计被覆盖的建筑](https://leetcode.cn/problems/count-covered-buildings/) · Medium · 灵茶山艾府：[统计行列的最小值和最大值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3531.统计被覆盖的建筑

[3531. 统计被覆盖的建筑 - 力扣（LeetCode）](https://leetcode.cn/problems/count-covered-buildings/description/)

题目给出一个正整数n，表示一个n \* n的城市，同时给出一个二维数组buildings，其中buildings[index] \= [x, y]，表示在坐标(x, y)有一个唯一的建筑。

若某个建筑在上、下、左、右四个方向中每个方向都至少存在一个建筑，则称这个建筑被覆盖。

问有多少建筑被覆盖。

首先对buildings进行一趟遍历，使用两个哈希表row和col分别统计每一行最小和最大的纵坐标，以及每一列最小和最大的横坐标。接下来再进行一趟遍历，对于当前遍历到的(x, y)，若x处于col[y][0]和col[y][1]之间，且y处于row[x][0]以及row[x][1]之间，说明(x, y)被覆盖，更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countCoveredBuildings(self, n, buildings):
        """
        :type n: int
        :type buildings: List[List[int]]
        :rtype: int
        """
        
        row = {}
        col = {}

        for x, y in buildings:
            if x not in row:
                row[x] = [y, y]
            else:
                row[x][0] = min(row[x][0], y)
                row[x][1] = max(row[x][1], y)
            
            if y not in col:
                col[y] = [x, x]
            else:
                col[y][0] = min(col[y][0], x)
                col[y][1] = max(col[y][1], x)
        
        res = 0
        for x, y in buildings:
            if x != col[y][0] and x != col[y][1] and y != row[x][0] and y != row[x][1]:
                res += 1
        return res
```
