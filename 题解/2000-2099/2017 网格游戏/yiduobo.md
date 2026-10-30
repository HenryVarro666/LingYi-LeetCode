---
title: "2017. 网格游戏"
aliases: ["yiduobo的每日leetcode 2017.网格游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/505641009"
zhihu_id: "505641009"
zhihu_title: "yiduobo的每日leetcode 2017.网格游戏"
question_id: "2017"
question: "网格游戏"
problem_url: "https://leetcode.cn/problems/grid-game/"
difficulty: "Medium"
created: "2022-04-26T23:52:00+08:00"
updated: "2022-04-26T23:52:00+08:00"
upvotes: 0
comments: 0
---

# 2017. 网格游戏

> **[yiduobo的每日leetcode 2017.网格游戏](https://zhuanlan.zhihu.com/p/505641009) · 知乎 · 2022-04-26 · 赞同 0**
> 力扣：[2017. 网格游戏](https://leetcode.cn/problems/grid-game/) · Medium · 灵茶山艾府：[枚举第一个机器人的拐弯位置](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2017.网格游戏

[力扣](https://leetcode-cn.com/problems/grid-game/)

注意到题目中的网格只有两行，那么第一个机器人必然是在第0行走到位置p，然后向下走到第1行，再从第1行的位置p走到末尾。由于网格中的分数都大于0，因此值得第二个机器人选择的路径还有两条：

1、第0行走到末尾然后向下。这种走法将得到第0行位置p + 1以及之后的分数

2、直接向下来到第1行，然后再向右走到末尾。这种走法将得到第1行位置p - 1以及之前的分数

第二个机器人显然会选择其中分数较大的那一条，因此当第一个机器人在位置p向下走到第1行时，第二个机器人的得分就是

max(grid[0][p + 1] + grid[0][p + 2] + ... + grid[0][n - 1], grid[1][0] + grid[1][1] + ... + grid[1][p - 1])

可以发现，式子的前半部分是第0行的后缀和，后半部分则是第1行的前缀和，那么完全可以优先预处理出这个后缀和以及前缀和，然后一趟遍历，枚举第一个机器人向下走的位置，通过上面的时间计算得到此时第二个机器人可以拿到的分数，取其中的最小值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def gridGame(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        n = len(grid[0])
        first = [0]
        for index in range(n - 1, 0, -1):
            first.append(first[-1] + grid[0][index])
        first.reverse()

        second = [0]
        for index in range(n - 1):
            second.append(second[-1] + grid[1][index])
        
        res = first[0]
        for index in range(1, n):
            res = min(res, max(first[index], second[index]))
        
        return res
```
