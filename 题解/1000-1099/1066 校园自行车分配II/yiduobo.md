---
title: "1066. 校园自行车分配II"
aliases: ["yiduobo的每日leetcode 1066.校园自行车分配II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608330821"
zhihu_id: "608330821"
zhihu_title: "yiduobo的每日leetcode 1066.校园自行车分配II"
question_id: "1066"
question: "校园自行车分配II"
problem_url: "https://leetcode.cn/problems/campus-bikes-ii/"
created: "2023-02-21T22:51:01+08:00"
updated: "2023-02-21T22:51:01+08:00"
upvotes: 0
comments: 0
---

# 1066. 校园自行车分配II

> **[yiduobo的每日leetcode 1066.校园自行车分配II](https://zhuanlan.zhihu.com/p/608330821) · 知乎 · 2023-02-21 · 赞同 0**
> 力扣：[1066. 校园自行车分配II](https://leetcode.cn/problems/campus-bikes-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1066.校园自行车分配II

[力扣](https://leetcode.cn/problems/campus-bikes-ii/)

从题目的数据规模来看应该是想要用状态压缩动态规划来实现，不过在这里使用km算法或网络流是更好的选择。我在这里使用的是费用流。

具体建图方法为：

1、将每个工人以及每辆自行车视为网络中的一个点，同时额外设置源点s以及汇点t

2、从s向每个工人发出一条容量为1，费用为0的边

3、从每辆自行车向t发出一条容量为1，费用为0的边

4、从每个工人向每辆自行车发出一条容量为1，费用为二者曼哈顿距离的边。同时需要额外设置一条反向的边，反向边的容量为0，费用为正向边的相反数

接下来执行一趟最小费用最大流，得到的最小费用即为最终答案。

关于费用流的一些简单知识可以参考

[yiduobo：yiduobo的每日leetcode 1595.连通两组点的最小成本](https://zhuanlan.zhihu.com/p/432304203)

最后附上python代码：

```python
class Solution(object):
    def assignBikes(self, workers, bikes):
        """
        :type workers: List[List[int]]
        :type bikes: List[List[int]]
        :rtype: int
        """

        n = len(workers)
        m = len(bikes)

        s = 0
        t = m + n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(1, n + 1):
            c[s][i] = 1
        for i in range(n + 1, m + n + 1):
            c[i][t] = 1
        
        for i in range(n):
            for j in range(m):
                v = abs(workers[i][0] - bikes[j][0]) + abs(workers[i][1] - bikes[j][1])
                c[i + 1][j + n + 1] = 1
                cost[i + 1][j + n + 1] = v
                cost[j + n + 1][i + 1] = -v
        
        res = 0
        for _ in range(n):
            heap = [[0, s, None]]
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            while heap:
                d, now, last = heapq.heappop(heap)
                if dis[now] is None:
                    dis[now] = d
                    prev[now] = last
                    for next in range(t + 1):
                        if c[now][next] > 0:
                            heapq.heappush(heap, [d + cost[now][next], next, now])
                
            res += dis[t]
            now = t
            while now != s:
                last = prev[now]
                c[last][now] -= 1
                c[now][last] += 1
                now = last
        
        return res
```
