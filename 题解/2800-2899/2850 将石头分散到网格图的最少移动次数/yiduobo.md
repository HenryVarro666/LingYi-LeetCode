---
title: "2850. 将石头分散到网格图的最少移动次数"
aliases: ["yiduobo的每日leetcode 2850.将石头分散到网格图的最少移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/enumeration", "leetcode/shortest-path", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/图论算法", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660608373"
zhihu_id: "660608373"
zhihu_title: "yiduobo的每日leetcode 2850.将石头分散到网格图的最少移动次数"
question_id: "2850"
question: "将石头分散到网格图的最少移动次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-spread-stones-over-grid/"
difficulty: "Medium"
rating: 2001
created: "2023-10-11T03:00:05+08:00"
updated: "2023-10-11T03:00:05+08:00"
upvotes: 0
comments: 0
---

# 2850. 将石头分散到网格图的最少移动次数

> **[yiduobo的每日leetcode 2850.将石头分散到网格图的最少移动次数](https://zhuanlan.zhihu.com/p/660608373) · 知乎 · 2023-10-11 · 赞同 0**
> 力扣：[2850. 将石头分散到网格图的最少移动次数](https://leetcode.cn/problems/minimum-moves-to-spread-stones-over-grid/) · Medium · 灵茶山艾府：[两种方法：枚举全排列 / 最小费用最大流（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2850.将石头分散到网格图的最少移动次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-moves-to-spread-stones-over-grid/)

首先可以明确的是，初始值为1的单元格实际上是可以直接无视的，因此在这里实际上就只需要考虑如果从初始值大于1的单元格移动石头到初始值为0的单元格。由于题目的数据规模很小，因此可以将这两种单元格收集起来，然后暴力搜索回溯，寻找每个初始值为0的单元格应该接受哪个初始值大于1的单元格的石头。

如果是8个0接受1个大于1的单元格，那么就是1^8种可能性，而7个0接受2个大于1则为2^7种可能性，6-3则是3^6，5-4则是4^5，再往后不可能出现5个或更多单元格中初始值大于1的情况，因此最坏也就是1024种可能性，完全不需要担心时间复杂度。

最后附上python代码：

```python
class Solution(object):
    def minimumMoves(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        z = []
        g = []
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    z.append([i, j])
                elif grid[i][j] > 1:
                    g.append([i, j])
        
        global res
        res = 10000

        def dfs(level, s):
            if level == len(z):
                global res
                res = min(res, s)
                return
            
            for x, y in g:
                if grid[x][y] > 1:
                    grid[x][y] -= 1
                    s += abs(x - z[level][0]) + abs(y - z[level][1])
                    dfs(level + 1, s)
                    s -= abs(x - z[level][0]) + abs(y - z[level][1])
                    grid[x][y] += 1
        
        dfs(0, 0)
        return res
```
