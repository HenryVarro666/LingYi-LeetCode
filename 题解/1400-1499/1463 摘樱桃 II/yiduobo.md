---
title: "1463. 摘樱桃II"
aliases: ["yiduobo的每日leetcode 1463.摘樱桃II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413286849"
zhihu_id: "413286849"
zhihu_title: "yiduobo的每日leetcode 1463.摘樱桃II"
question_id: "1463"
question: "摘樱桃 II"
problem_url: "https://leetcode.cn/problems/cherry-pickup-ii/"
difficulty: "Hard"
created: "2021-09-23T22:11:36+08:00"
updated: "2021-09-23T22:11:36+08:00"
upvotes: 0
comments: 0
---

# 1463. 摘樱桃II

> **[yiduobo的每日leetcode 1463.摘樱桃II](https://zhuanlan.zhihu.com/p/413286849) · 知乎 · 2021-09-23 · 赞同 0**
> 力扣：[1463. 摘樱桃 II](https://leetcode.cn/problems/cherry-pickup-ii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1463.摘樱桃II

[力扣](https://leetcode-cn.com/problems/cherry-pickup-ii/)

经典的动态规划问题，令f[i][j][k]表示前i步，一号机器人在第j行，二号机器人在第k行时可以拿到的最大樱桃数目。由于地图中不存在负数，那么可以证明最终答案中两个机器人的路线是不相交的，于是此时只需要考虑j \< k的这些状态。

对于f[i - 1][j][k]，一号机器人可以走到下一行的第j - 1、j、j + 1列，二号机器人则可以走到下一行的第k - 1、k、k + 1列，枚举各种可能，记为j'以及k'。若j'和k'没有走出地图，且j'\<k'，那么就有f[i][j'][k'] \= max(f[i][j'][k'], f[i - 1][j][k] + grid[i][j'] + grid[i][k'])。

动态规划完成后，最后一行中所有状态的最大值就是最终答案。

注意到这里每一轮的状态只与上一轮有关，因此可以使用滑动数组，优化掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def cherryPickup(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        f = {}
        f[n - 1] = grid[0][0] + grid[0][-1]
        for i in range(1, m):
            g = {}
            for state in f:
                j = state / n
                k = state % n
                for next_j in range(j - 1, j + 2):
                    if next_j >= 0 and next_j < n - 1:
                        for next_k in range(k - 1, k + 2):
                            if next_k < n and next_k > next_j:
                                next_state = next_j * n + next_k
                                if next_state not in g or g[next_state] < f[state] + grid[i][next_j] + grid[i][next_k]:
                                    g[next_state] = f[state] + grid[i][next_j] + grid[i][next_k]
            
            f = g
        
        return max(g.values())
```
