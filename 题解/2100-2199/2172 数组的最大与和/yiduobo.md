---
title: "2172. 数组的最大与和"
aliases: ["yiduobo的每日leetcode 2172.数组的最大与和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/graph", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/534077386"
zhihu_id: "534077386"
zhihu_title: "yiduobo的每日leetcode 2172.数组的最大与和"
question_id: "2172"
question: "数组的最大与和"
problem_url: "https://leetcode.cn/problems/maximum-and-sum-of-array/"
difficulty: "Hard"
rating: 2392
created: "2022-06-26T20:24:47+08:00"
updated: "2022-06-26T20:24:47+08:00"
upvotes: 0
comments: 0
---

# 2172. 数组的最大与和

> **[yiduobo的每日leetcode 2172.数组的最大与和](https://zhuanlan.zhihu.com/p/534077386) · 知乎 · 2022-06-26 · 赞同 0**
> 力扣：[2172. 数组的最大与和](https://leetcode.cn/problems/maximum-and-sum-of-array/) · Hard · 灵茶山艾府：[状态压缩 DP（附最小费用最大流做法）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2172.数组的最大与和

[力扣](https://leetcode.cn/problems/maximum-and-sum-of-array/)

从题目的数据规模来看可以使用状态压缩动态规划，但是更好的做法是将其转化为网络流来求解。

将nums中的每个数以及每个篮子视为图中的点，然后设置源点s以及汇点t，接下来：

1、从s向nums中的每个数连一条容量为1，费用为0的边，表示每个数字都需要被使用一次

2、从nums中的每个数向每个篮子连一条容量为1的边，其中第i个数向第j个篮子的边的费用为nums[i] - nums[i] & (j + 1)

这里写成nums[i] - nums[i] & (j + 1)的目的是将最大与和转化为最小损失，方便最短路的运算。由于是与运算，因此nums[i] & (j + 1)必然是小于等于nums[i]的。题目要求得到最大与和，在这里可以转化成一开始的总收益为上限sum(nums)，然后在放置一个数之后会产生一些损失，如何放置使得收益最大，也就是总的损失最小。

3、从每个篮子向t连一条容量为2，费用为0的边，表示每个篮子中最多只能放两个数

接下来执行最小费用最大流，计算得到最终的最小损失，然后使用sum(nums)减去这个损失就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def maximumANDSum(self, nums, numSlots):
        """
        :type nums: List[int]
        :type numSlots: int
        :rtype: int
        """

        n = len(nums)
        s = n + numSlots
        t = s + 1
        c = [[0] * (t + 1) for _ in range(t + 1)]
        v = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(n):
            c[s][i] = 1
        for j in range(n, n + numSlots):
            c[j][t] = 2
        for i in range(n):
            for j in range(n, n + numSlots):
                c[i][j] = 1
                v[i][j] = nums[i] - (nums[i] & (j - n + 1))
                v[j][i] = -v[i][j]
        
        res = sum(nums)
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
