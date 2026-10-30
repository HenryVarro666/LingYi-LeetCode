---
title: "2403. 杀死所有怪物的最短时间"
aliases: ["yiduobo的每日leetcode 2403.杀死所有怪物的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630959994"
zhihu_id: "630959994"
zhihu_title: "yiduobo的每日leetcode 2403.杀死所有怪物的最短时间"
question_id: "2403"
question: "杀死所有怪物的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-kill-all-monsters/"
created: "2023-05-21T01:12:04+08:00"
updated: "2023-05-21T01:12:04+08:00"
upvotes: 0
comments: 0
---

# 2403. 杀死所有怪物的最短时间

> **[yiduobo的每日leetcode 2403.杀死所有怪物的最短时间](https://zhuanlan.zhihu.com/p/630959994) · 知乎 · 2023-05-21 · 赞同 0**
> 力扣：[2403. 杀死所有怪物的最短时间](https://leetcode.cn/problems/minimum-time-to-kill-all-monsters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2403.杀死所有怪物的最短时间

[力扣](https://leetcode.cn/problems/minimum-time-to-kill-all-monsters/)

按题目给出的数据规模可以用状态压缩动态规划来求解，不过在这里使用匹配或者网络流是更好的选择。

题目实际上是需要找出power的一个排列，也就是将power[i]对应到i + 1，使得power[i] / (i + 1)向上取整后的和最小。这是一个非常标准的二分图最优匹配问题，可以使用km算法或者费用流求解，我在这里采用的是费用流。

首先将power中的每个数以及1到n都视为图中的点，然后设置源点s以及汇点t，接下来：

1、从s向每个power中的每个数发射一条容量为1，费用为0的边，表示每个power都只能被使用一次。

2、从1到n这些点想t发射一条容量为1，费用为0的边，表示1到n中的每个数都只能被使用一次。

3、从每个power向1到n的每个数字发射一条边，容量为1，费用为power值除以目标点的数值，向上取整。

接下来执行一次最小费用最大流就行了。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, power):
        """
        :type power: List[int]
        :rtype: int
        """

        n = len(power)
        s = 0
        c = [[0] * (n + n + 2) for _ in range(n + n + 2)]
        w = [[0] * (n + n + 2) for _ in range(n + n + 2)]
        t = n + n + 1

        for i in range(1, n + 1):
            c[s][i] = 1
        
        for i in range(n + 1, n + n + 1):
            c[i][t] = 1
        
        for i in range(1, n + 1):
            for j in range(n + 1, n + n + 1):
                c[i][j] = 1
                w[i][j] = power[i - 1] / (j - n)
                if power[i - 1] % (j - n) > 0:
                    w[i][j] += 1
                w[j][i] = -w[i][j]

        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                next = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + w[now][index]):
                        dis[index] = dis[now] + w[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        next = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(next)
                now = next

            res += dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]

        return res
```
