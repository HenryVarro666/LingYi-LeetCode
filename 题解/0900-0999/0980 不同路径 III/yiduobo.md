---
title: "980. 不同路径III"
aliases: ["yiduobo的每日leetcode 980.不同路径III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363368096"
zhihu_id: "363368096"
zhihu_title: "yiduobo的每日leetcode 980.不同路径III"
question_id: "980"
question: "不同路径 III"
problem_url: "https://leetcode.cn/problems/unique-paths-iii/"
difficulty: "Hard"
rating: 1830
created: "2021-04-08T23:28:20+08:00"
updated: "2021-04-08T23:28:20+08:00"
upvotes: 0
comments: 0
---

# 980. 不同路径III

> **[yiduobo的每日leetcode 980.不同路径III](https://zhuanlan.zhihu.com/p/363368096) · 知乎 · 2021-04-08 · 赞同 0**
> 力扣：[980. 不同路径 III](https://leetcode.cn/problems/unique-paths-iii/) · Hard · 灵茶山艾府：[两种方法：回溯/状态压缩+记忆化搜索（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

980.不同路径III

[力扣](https://leetcode-cn.com/problems/unique-paths-iii/)

好家伙我直接好家伙，leetcode上居然还有这种难度的题目。

如果按一般做法来做，这题是在无向图上找出所有指定起点和终点的汉密尔顿路径的问题，应该是np难的。不过这题最多只有20个格子，也就是说图中最多只有20个节点，使用传统的状态压缩动态规划可以得到O(K \* 2^K)的算法，其中K为图中节点数量。具体来说就是使用状态f[state][x]表示当前已经经过了state中的网格，最后停留在x这个格子一共有多少种方案，那么对于f[state][x]，其必然是从f[state - 1\<\<x][y]移动过来的，其中y必须与x相邻同时y必须也出现在state当中。

不过，这里网格之间的连通性其实有很大的限制，那么如果回到网格本身，还存在更好的状态压缩方案，具体可以参考陈丹琦的《基于连通性的状态压缩动态规划》，非常巧妙但是理解起来并不容易，这里就不再展开了。

最后附上python代码，这里贴出来的是朴素的状态压缩算法：

```python
class Solution(object):
    def uniquePathsIII(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        g = {}
        start = end = None
        final_state = 0

        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if grid[i][j] != -1:
                    num = i * n + j
                    if grid[i][j] == 1:
                        start = num
                    elif grid[i][j] == 2:
                        end = num
                    
                    final_state |= 1 << num

                    if num not in g:
                        g[num] = set()

                    if i + 1 < m and grid[i + 1][j] != -1:
                        tmp = (i + 1) * n + j
                        if tmp not in g:
                            g[tmp] = set()
                        
                        g[num].add(tmp)
                        g[tmp].add(num)
                    
                    if j + 1 < n and grid[i][j + 1] != -1:
                        tmp = i * n + j + 1
                        if tmp not in g:
                            g[tmp] = set()
                        
                        g[num].add(tmp)
                        g[tmp].add(num)

        f = [[None] * (m * n) for _ in range(final_state + 1)]
        f[1 << start][start] = 1

        return self.dfs(final_state, end, g, start, f)
    
    def dfs(self, state, last, g, start, f):
        if f[state][last] is None:
            f[state][last] = 0
            if last == start:
                return 0 

            prev_state = state ^ (1 << last)

            for prev in g[last]:
                if prev_state & (1 << prev):
                    f[state][last] += self.dfs(prev_state, prev, g, start, f)
        
        return f[state][last]
```
