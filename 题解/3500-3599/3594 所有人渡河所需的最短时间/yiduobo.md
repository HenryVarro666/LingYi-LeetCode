---
title: "3594. 所有人渡河所需的最短时间"
aliases: ["yiduobo的每日leetcode 3594.所有人渡河所需的最短时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/graph", "leetcode/bitmask", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940205881976398180"
zhihu_id: "1940205881976398180"
zhihu_title: "yiduobo的每日leetcode 3594.所有人渡河所需的最短时间"
question_id: "3594"
question: "所有人渡河所需的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-transport-all-individuals/"
difficulty: "Hard"
rating: 2604
created: "2025-08-17T00:40:28+08:00"
updated: "2025-08-17T00:40:29+08:00"
upvotes: 0
comments: 0
---

# 3594. 所有人渡河所需的最短时间

> **[yiduobo的每日leetcode 3594.所有人渡河所需的最短时间](https://zhuanlan.zhihu.com/p/1940205881976398180) · 知乎 · 2025-08-17 · 赞同 0**
> 力扣：[3594. 所有人渡河所需的最短时间](https://leetcode.cn/problems/minimum-time-to-transport-all-individuals/) · Hard · 灵茶山艾府：[子集状压 + Dijkstra，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3594.所有人渡河所需的最短时间

[3594. 所有人渡河所需的最短时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-transport-all-individuals/description/)

有n名人员处于一个营地，他们需要使用一艘船过河到的目的地，n的规模不超过12。这艘船一次最多可以承载k个人，渡河过程受到环境条件的影响，这些条件以周期性的方式在m个阶段内变化，k和m都不超过5。

对于每个阶段j，都有一个速率倍率mul[j]，当mul[j] > 1时，渡河的时间将变长，反之将缩短。

另外对于每个人i，都有一个划船能力time[i]，表示在不考虑速率倍率的情况下渡河所需的时间，单位为分钟。

假设从阶段j有一组人出发渡河，所需的时间就是组能成员最大的time[i]，乘以mul[j]。若渡河的时间为d，那么阶段将会向前推进floor(d) % m步。若此时还有人留在营地，就需要一个人把船开回去。若这个人的索引为r，那么所需的时间就是time[r] \* mul[curr]，需要注意这里的curr就是j往后推进floor(d) % m得到的新阶段。船开回去之后，若所需的时间为rt_time，那么阶段还会推进floor(rt_time) % m步。

返回所有人都过河所需的最少时间，若没有可行的方案，则直接返回-1。

直观看来，应该让最快的人当摆渡人，每次带最慢的几个人过河，但是这个策略明显是有问题的。即使抛开速率倍率的变化不看，也可能出现第一次由最快的人开回来，第二次由第二快的人开回来，最后这两个人再一起过河这种情况。例如time \= [1, 2, 9, 10]，船上可以坐两个人这种情况，如果按照

[1, 10]过河 -> 1回来 -> [1, 9]过河 -> 1回来 -> [1, 2]过河

所需的时间为10 + 1 + 9 + 1 + 2 \= 23

但是如果按照

[1, 2]过河 -> 1回来 -> [9, 10]过河 -> 2回来 -> [1, 2]过河

所需的时间为2 + 1 + 10 + 2 + 2 \= 17

也就是说，在这里很难找到通用的贪心策略。不过本题中需要过河的人数n较小，因此可以使用状态压缩来处理。需要注意的是，本题中的阶段j是轮动的，因此执行动态规划的顺序不好确定，需要转而改为最短路来进行处理。使用一个堆储存当前所有已经扩展得到的状态以及代价三元组(cost, state, step)，表示让state中的人已经过河，且此时的阶段为step时所需的最小时间，那么堆顶的(cost, state, step)：

1、先枚举所有可行的子状态sub，合法的sub满足state和sub的按位与为0，也就是sub中的所有人都还没有过河

2、通过state | sub计算得到新的状态nxt_state，然后使用sub中最慢的人对应的过河时间sub_cost[sub]，乘以阶段系数mul[step]，得到此次过河需要的时间d

3、通过(int(d) + step) % m得到新的阶段nxt_step

4、此时需要分为两种情况：

若nxt_state为(1 \<\< n) - 1，说明这次过河所有人都过去了，无需再开船回去，因此可以直接将(cost + d, nxt_state, nxt_step)加入堆中

反之，则需要从河对岸的人中选出一个开船回来，也就是从nxt_state中选出一个人作为rt，此时过河的人状态变为nxt_state ^ (1 \<\< rt)，同时还需要计算这个人开船回去的时间，也就是rt_d \= time[rt] \* mul[nxt_step]，最后计算开船回去后的阶段(int(rt_d) + nxt_step) % m，将新的状态三元组加入到堆中

重复以上过程，直到state首次变为(1 \<\< n) - 1，此时对应的cost即为最终答案。若始终没有这样的state，则返回-1。

另外本题对常数卡得比较严，在具体实现上需要做一些常数优化，例如先预处理出所有的1个人到k个人坐船可能构成的子状态表示以及对应的代价。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, n, k, m, time, mul):
        """
        :type n: int
        :type k: int
        :type m: int
        :type time: List[int]
        :type mul: List[float]
        :rtype: float
        """
        
        max_state = (1 << n) - 1
        sub_contain = {}
        sub_cost = {}

        for state in range(1, max_state + 1):
            contain = []
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    contain.append(index)
            
            sub_contain[state] = contain[:]
            if len(contain) <= k:
                sub_cost[state] = max([time[index] for index in contain])
        

        heap = [(0, 0, 0)]
        f = [[None] * m for _ in range(max_state + 1)]
        f[0][0] = 0.0
        while heap:
            cost, state, step = heapq.heappop(heap)
            if cost > f[state][step]:
                continue
            if state == max_state:
                return cost
            for sub in sub_cost:
                if state & sub == 0:
                    nxt_state = state | sub
                    d = sub_cost[sub] * mul[step]
                    nxt_step = (step + int(d)) % m

                    if nxt_state == max_state:
                        if f[nxt_state][nxt_step] is None or f[nxt_state][nxt_step] > cost + d:
                            f[nxt_state][nxt_step] = cost + d
                            heapq.heappush(heap, (cost + d, nxt_state, nxt_step))
                    else:
                        for rt in sub_contain[nxt_state]:
                            state_with_rt = nxt_state ^ (1 << rt)
                            rt_d = time[rt] * mul[nxt_step]
                            step_with_rt = (nxt_step + int(rt_d)) % m

                            if f[state_with_rt][step_with_rt] is None or f[state_with_rt][step_with_rt] > cost + d + rt_d:
                                f[state_with_rt][step_with_rt] = cost + d + rt_d
                                heapq.heappush(heap, (cost + d + rt_d, state_with_rt, step_with_rt))

        return -1
```
