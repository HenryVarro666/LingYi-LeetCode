---
title: "2247. K条高速公路的最大旅行费用"
aliases: ["yiduobo的每日leetcode 2247.K条高速公路的最大旅行费用"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628455676"
zhihu_id: "628455676"
zhihu_title: "yiduobo的每日leetcode 2247.K条高速公路的最大旅行费用"
question_id: "2247"
question: "K条高速公路的最大旅行费用"
problem_url: "https://leetcode.cn/problems/maximum-cost-of-trip-with-k-highways/"
created: "2023-05-11T04:17:29+08:00"
updated: "2023-05-11T04:17:29+08:00"
upvotes: 0
comments: 0
---

# 2247. K条高速公路的最大旅行费用

> **[yiduobo的每日leetcode 2247.K条高速公路的最大旅行费用](https://zhuanlan.zhihu.com/p/628455676) · 知乎 · 2023-05-11 · 赞同 0**
> 力扣：[2247. K条高速公路的最大旅行费用](https://leetcode.cn/problems/maximum-cost-of-trip-with-k-highways/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2247.K条高速公路的最大旅行费用

[力扣](https://leetcode.cn/problems/maximum-cost-of-trip-with-k-highways/)

没有什么特别好的处理方法，不过好在本题的数据规模较小，可以使用状态压缩动态规划来求解。

首先还是需要考虑边界情况。经过K条告诉公路意味着经过K + 1个城市，若这里的K + 1 > n，那么必然无解，直接返回-1即可。

而对于一般情况，则可以令f[state][last]表示已经到达过了state中的城市，且最后停留在last这个城市时的最大旅行费用，那么对于f[state][last]，首先可以通过state ^ (1 \<\< last)得到上一个状态pre_state，然后枚举与last相邻的所有位置pre_pos，若当前的pre_pos在pre_state中出现过，那么就有f[state][last] \= max(f[state][last], f[pre_state] + dis[pre_pos][last])，表示当前状态是从pre_state开始，经过pre_pos到last的路径得到的。

计算完成得到f数组后，由于题目需要求解的是到达过K + 1个城市的路径，因此可以先进行一次dfs，找出所有K + 1个城市的组合并计算出其对应的状态表示，在得到f数组后就可以先枚举这些候选状态作为state，再枚举状态中包含的所有城市作为last，然后使用f[state][last]来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumCost(self, n, highways, k):
        """
        :type n: int
        :type highways: List[List[int]]
        :type k: int
        :rtype: int
        """

        if k + 1 > n:
            return -1

        g = {index : {} for index in range(n)}
        for x, y, v in highways:
            g[x][y] = g[y][x] = v

        candidate = []
        def dfs(level, now, cnt):
            if cnt == k + 1:
                candidate.append(now)
                return
            
            if level == n:
                return

            dfs(level + 1, now, cnt)
            dfs(level + 1, now | (1 << level), cnt + 1)

        dfs(0, 0, 0)

        max_state = 1 << n
        f = [[None] * n for _ in range(max_state)]
        for index in range(n):
            f[1 << index][index] = 0
        res = -1

        def calc(state, last_pos):
            if f[state][last_pos] is None:
                f[state][last_pos] = -1
                pre_state = state ^ (1 << last_pos)
                for pre_pos in g[last_pos]:
                    if pre_state & (1 << pre_pos) == (1 << pre_pos):
                        pre_dis = calc(pre_state, pre_pos)
                        if pre_dis != -1:
                            f[state][last_pos] = max(f[state][last_pos], pre_dis + g[last_pos][pre_pos])

            return f[state][last_pos]

        for state in candidate:
            for last_pos in range(n):
                if state & (1 << last_pos) == (1 << last_pos):
                    res = max(res, calc(state, last_pos))

        return res
```
