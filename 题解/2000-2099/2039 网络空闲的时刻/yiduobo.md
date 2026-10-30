---
title: "2039. 网络空闲的时刻"
aliases: ["yiduobo的每日leetcode 2039.网络空闲的时刻"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/math", "leetcode/bfs", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/509866266"
zhihu_id: "509866266"
zhihu_title: "yiduobo的每日leetcode 2039.网络空闲的时刻"
question_id: "2039"
question: "网络空闲的时刻"
problem_url: "https://leetcode.cn/problems/the-time-when-the-network-becomes-idle/"
difficulty: "Medium"
rating: 1865
created: "2022-05-05T23:08:47+08:00"
updated: "2022-05-05T23:08:47+08:00"
upvotes: 1
comments: 0
---

# 2039. 网络空闲的时刻

> **[yiduobo的每日leetcode 2039.网络空闲的时刻](https://zhuanlan.zhihu.com/p/509866266) · 知乎 · 2022-05-05 · 赞同 1**
> 力扣：[2039. 网络空闲的时刻](https://leetcode.cn/problems/the-time-when-the-network-becomes-idle/) · Medium · 灵茶山艾府：[BFS + 统计每个点变为空闲状态的最早秒数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2039.网络空闲的时刻

[力扣](https://leetcode-cn.com/problems/the-time-when-the-network-becomes-idle/)

由于各个数据服务之间是互不影响的，因此只需要找出每个数据服务器接收最后一条回复的时间，其中的最大值就是网络中最后一个还有消息存在的时刻，那么这个时刻加上1就是最终答案了。

接下来考察每个数据服务器。

要想知道单条消息及回复需要在网络中走多久，就需要直到当前服务器距离主服务器的距离。对于这一点，可以通过从0开始的bfs，来找出每个数据服务器到主服务器的距离。

接下来，设当前考察的数据服务器到主服务器的距离为dis，那么当前服务器将在dis \* 2秒后收到第一次回复，也就是说在之前的dis \* 2 - 1秒内，当前数据服务器都会按间隔继续发送数据。

在dis \* 2 - 1秒内，将会发送(dis \* 2 - 1) / patience条额外的数据，因此当前数据服务器总共会发送query_cnt \= 1 + (dis \* 2 - 1) / patience条数据，其中这个1代表的是首次发送的数据。

现在需要知道最后一次收到回复的时间，该时间就等于最后一次发送数据的时间，再加上dis \* 2。最后一次发送数据的时间则可以通过(query_cnt - 1) \* patience计算得到，因此与当前数据服务器有关的消息最后一次出现在网络中的时间是(query_cnt - 1) \* patience + dis \* 2。

对每个服务器计算这个时间，取其中的最大值，然后加1返回即可。

最后附上python代码：

```python
class Solution(object):
    def networkBecomesIdle(self, edges, patience):
        """
        :type edges: List[List[int]]
        :type patience: List[int]
        :rtype: int
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        dis = {0: 0}
        q = [0]
        l = 0
        r = 1
        res = 0
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                if next not in dis:
                    dis[next] = dis[now] + 1
                    query_cnt = (dis[next] + dis[next] - 1) / patience[next] + 1
                    res = max(res, (query_cnt - 1) * patience[next] + dis[next] + dis[next])
                    q.append(next)
                    r += 1
        
        return res + 1
```
