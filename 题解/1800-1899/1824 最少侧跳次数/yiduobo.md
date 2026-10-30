---
title: "1824. 最少侧跳次数"
aliases: ["yiduobo的每日leetcode 1824.最少侧跳次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/queue", "leetcode/shortest-path", "leetcode/shuang-duan-dui-lie", "题单/网格图", "题单/动态规划", "题单/网格图/三-网格图-0-1-BFS", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466706977"
zhihu_id: "466706977"
zhihu_title: "yiduobo的每日leetcode 1824.最少侧跳次数"
question_id: "1824"
question: "最少侧跳次数"
problem_url: "https://leetcode.cn/problems/minimum-sideway-jumps/"
difficulty: "Medium"
rating: 1778
created: "2022-02-12T21:30:42+08:00"
updated: "2022-02-12T21:30:43+08:00"
upvotes: 0
comments: 0
---

# 1824. 最少侧跳次数

> **[yiduobo的每日leetcode 1824.最少侧跳次数](https://zhuanlan.zhihu.com/p/466706977) · 知乎 · 2022-02-12 · 赞同 0**
> 力扣：[1824. 最少侧跳次数](https://leetcode.cn/problems/minimum-sideway-jumps/) · Medium · 灵茶山艾府：[从 0 到 1 的 0-1 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1824.最少侧跳次数

[力扣](https://leetcode-cn.com/problems/minimum-sideway-jumps/)

题目应该是存在某种贪心算法的，我在这里没有细想，还是用的动态规划。

令f[index][p]表示跳到第index列，第p行所需的最少侧跳次数，那么：

1、若第index列p这第一行恰好是石头，那么置f[index][p]为n + 1，表示不能通过

2、否则枚举上一步的所有位置prev_p。尝试从上一轮的f[index - 1][prev_p]跳到f[index][prev_p]，再跳到f[index][p]。对于这个二段跳而言，前半部分需要满足index列prev_p这一行不是石头，而后半部分则需要考察特殊情况，即prev_p就等于p，此时并不需要后半部分的跳跃，否则需要将横跳的次数加上1。

于是就有

f[index][p] \= min(f[index][p], f[index - 1][prev_p] + delta

其中index列prev_p这一行不能是石头，而delta在prev_p \= p时为0，其他情况下为1

动态规划结束后，min(f[-1])就是最终答案。

注意到这里每一轮的状态只与上一轮有关，因此可以优化掉index这一维。

最后附上python代码：

```python
class Solution(object):
    def minSideJumps(self, obstacles):
        """
        :type obstacles: List[int]
        :rtype: int
        """

        n = len(obstacles)
        f = [1, 0, 1]
        if obstacles[0] != 0:
            f[obstacles[0] - 1] = n + 1
        
        g = [None] * 3
        for index in range(1, n):
            for pos in range(3):
                g[pos] = n + 1
                if obstacles[index] - 1 == pos:
                    continue
                
                for prev_pos in range(3):
                    if obstacles[index] - 1 == prev_pos:
                        continue
                    if prev_pos == pos:
                        delta = 0
                    else:
                        delta = 1
                    g[pos] = min(g[pos], f[prev_pos] + delta)
            
            f = g[:]
        
        return min(f)
```
