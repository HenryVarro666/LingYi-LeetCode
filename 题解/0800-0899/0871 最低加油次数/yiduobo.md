---
title: "871. 最低加油次数"
aliases: ["yiduobo的每日leetcode 871.最低加油次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/动态规划", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350430545"
zhihu_id: "350430545"
zhihu_title: "yiduobo的每日leetcode 871.最低加油次数"
question_id: "871"
question: "最低加油次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-refueling-stops/"
difficulty: "Hard"
rating: 2074
created: "2021-02-12T20:14:37+08:00"
updated: "2021-02-12T20:14:37+08:00"
upvotes: 2
comments: 0
---

# 871. 最低加油次数

> **[yiduobo的每日leetcode 871.最低加油次数](https://zhuanlan.zhihu.com/p/350430545) · 知乎 · 2021-02-12 · 赞同 2**
> 力扣：[871. 最低加油次数](https://leetcode.cn/problems/minimum-number-of-refueling-stops/) · Hard · 灵茶山艾府：[最大堆贪心（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

871.最低加油次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-refueling-stops/)

由于加油除了需要达到对应的加油站之外并没有任何额外的前置条件，因此在这里我们并不需要在到达一个加油站时就急着判断是否需要加油，而是可以在无法继续前进时选择当前已经到达，且油最多的加油站进行加油。

在这里需要选择油量最多的加油站，因此可以使用堆来维护当前可用的加油站。那么现在的做法为：

1、初始化now为初始油量，station_pos为0，表示当前可到达的最远的加油站下标，res为0

2、若now小于target，说明需要进行加油，于是可以在当前station_pos的基础上继续向后推进，将可到达的加油站加入到堆中。若此时堆为空，说明没有可用的加油站，直接返回-1；若此时堆不为空，那么选择其中剩余油量最多的加油站进行加油，同时res加上1表示进行了一次加油。重复此过程直到now大于等于target为止。

最后附上python代码：

```python
class Solution(object):
    def minRefuelStops(self, target, startFuel, stations):
        """
        :type target: int
        :type startFuel: int
        :type stations: List[List[int]]
        :rtype: int
        """

        now = startFuel
        station_pos = 0
        heap = []
        n = len(stations)
        res = 0
        while now < target:
            while station_pos < n and now >= stations[station_pos][0]:
                heapq.heappush(heap, -stations[station_pos][1])
                station_pos += 1
            res += 1
            if heap:
                now += -heapq.heappop(heap)
            else:
                return -1
        
        return res
```
