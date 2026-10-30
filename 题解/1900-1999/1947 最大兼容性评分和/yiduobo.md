---
title: "1947. 最大兼容性评分和"
aliases: ["yiduobo的每日leetcode 1947.最大兼容性评分和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/491190131"
zhihu_id: "491190131"
zhihu_title: "yiduobo的每日leetcode 1947.最大兼容性评分和"
question_id: "1947"
question: "最大兼容性评分和"
problem_url: "https://leetcode.cn/problems/maximum-compatibility-score-sum/"
difficulty: "Medium"
rating: 1704
created: "2022-04-01T01:02:33+08:00"
updated: "2022-04-01T01:02:33+08:00"
upvotes: 0
comments: 0
---

# 1947. 最大兼容性评分和

> **[yiduobo的每日leetcode 1947.最大兼容性评分和](https://zhuanlan.zhihu.com/p/491190131) · 知乎 · 2022-04-01 · 赞同 0**
> 力扣：[1947. 最大兼容性评分和](https://leetcode.cn/problems/maximum-compatibility-score-sum/) · Medium · 灵茶山艾府：[O(m^3) 带权二分图最大完美匹配](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1947.最大兼容性评分和

[力扣](https://leetcode-cn.com/problems/maximum-compatibility-score-sum/)

按题目数据规模来看，使用状态压缩动态规划是可以做的，不过在这里使用网络流或者匹配算法是更优的选择。

题目给出的是一个标准的二分图，其中左侧节点为学生，右侧节点为老师，而每一对学生和老师之间存在一条边，权重为二人之间的兼容性评分。接下来的任务就是为每个学生找到配对的老师，使得最终的得分最大。实际上，这就是经典的最优匹配问题，可以使用KM算法来做。

我在这里还是采用的网络流。除学生和老师外设立源点s和汇点t，接下来建图：

1、从s往每个学生连一条边，容量为1费用为0

2、从每个老师往t连一条边，容量为1费用为0

3、从每个学生往每个老师连一条边，容量为1，费用为题目总数减去二人的兼容性得分，即二人不匹配的题目数

接下来在图中做一次最小费用最大流，得到的最小费用就是最终浪费掉的兼容性得分，此时的答案就是题目总数乘以人数，减去这个最小费用。

最后附上python代码：

```python
class Solution(object):
    def maxCompatibilitySum(self, students, mentors):
        """
        :type students: List[List[int]]
        :type mentors: List[List[int]]
        :rtype: int
        """

        n = len(students)
        s = n + n
        t = n + n + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]
        for i in range(n):
            c[s][i] = 1
            c[i + n][t] = 1

        m = len(students[0])
        for i in range(n):
            for j in range(n):
                cnt = m
                for index in range(m):
                    if students[i][index] == mentors[j][index]:
                        cnt -= 1
                
                c[i][j + n] = 1
                v[i][j + n] = cnt
                v[j + n][i] = -cnt

        res = m * n
        while True:
            dis = [-1] * (t + 1)
            prev = [-1] * (t + 1)
            dis[s] = 0
            heap = []
            for i in range(n):
                if c[s][i] > 0:
                    heapq.heappush(heap, [v[s][i], s, i])
            
            while heap:
                d, p, now = heapq.heappop(heap)
                if dis[now] != -1 and d >= dis[now]:
                    continue
                
                dis[now] = d
                prev[now] = p
                for next in range(t + 1):
                    if c[now][next] > 0:
                        heapq.heappush(heap, [d + v[now][next], now, next])
            
            if dis[t] == -1:
                break

            res -= dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]

        return res
```
