---
title: "3429. 粉刷房子IV"
aliases: ["yiduobo的每日leetcode 3429.粉刷房子IV"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890192634468886491"
zhihu_id: "1890192634468886491"
zhihu_title: "yiduobo的每日leetcode 3429.粉刷房子IV"
question_id: "3429"
question: "粉刷房子 IV"
problem_url: "https://leetcode.cn/problems/paint-house-iv/"
difficulty: "Medium"
rating: 2166
created: "2025-04-01T00:12:31+08:00"
updated: "2025-04-01T00:12:31+08:00"
upvotes: 0
comments: 0
---

# 3429. 粉刷房子IV

> **[yiduobo的每日leetcode 3429.粉刷房子IV](https://zhuanlan.zhihu.com/p/1890192634468886491) · 知乎 · 2025-04-01 · 赞同 0**
> 力扣：[3429. 粉刷房子 IV](https://leetcode.cn/problems/paint-house-iv/) · Medium · 灵茶山艾府：[多维 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3429.粉刷房子IV

[3429. 粉刷房子 IV - 力扣（LeetCode）](https://leetcode.cn/problems/paint-house-iv/description/)

题目给出一个偶数n，表示沿直线排列的房屋数量。另外给出一个大小为n \* 3的二维数组cost，其中cost[i][j]表示将第i间房子涂成颜色j的成本。现在需要粉刷房子，要求相邻的房子颜色不能相同，且距离行两端等距的房子颜色也不能相同，例如当n \= 6时，位置(0, 5)、(1, 4)、(2, 3)的房屋是等距的。

问粉刷房子的最低的成本是多少。

之前好像碰到过类似的问题，但是题号忘记了。对于这类单行等距的问题，可以在正中间对折一下，变为两行，n // 2列的矩阵，那么问题就变成了保证矩阵所有单元格的颜色在水平和竖直方向下都不相同时的最低成本。

由于本题的颜色只有3种，那么可以直接枚举每一列可行的颜色组合，一共6种组合，分别是(0, 1)、(0, 2)、(1, 0)、(1, 2)、(2, 0)、(2, 1)。接下来令f\[index\]\[state\]表示粉刷完前index列，且最后这一列的颜色组合为state时的最低成本，那么对于f\[index\]\[state\]，可以枚举前一列的所有颜色组合pre，若state\[0\]不等于pre\[0\]，且state\[1\]不等于pre\[1\]，那么就可以从f\[index - 1\]\[pre\]转移到f\[index\]\[state\]，代价则为f\[index - 1\]\[pre\] + cost\[index\]\[state\[0\]\] + cost\[n - index - 1\]\[state\[1\]\]。

另外注意到每一轮的状态只与上一轮有关，以此可以省去index这一维，得到一种空间复杂度O(1)的算法。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, n, cost):
        """
        :type n: int
        :type cost: List[List[int]]
        :rtype: int
        """
        
        states = {0: (0, 1),
                  1: (0, 2),
                  2: (1, 0),
                  3: (1, 2),
                  4: (2, 0),
                  5: (2, 1)
        }
        f = [0] * 6
        for st in states:
            first, second = states[st]
            f[st] = cost[0][first] + cost[-1][second]
        
        for index in range(1, n // 2):
            g = f[:]
            f = [None] * 6
            for st in states:
                for pre in states:
                    if states[st][0] == states[pre][0] or states[st][1] == states[pre][1]:
                        continue
                    first, second = states[st]
                    c = g[pre] + cost[index][first] + cost[n - index - 1][second]
                    if f[st] is None or f[st] > c:
                        f[st] = c
        
        return min(f)
```
