---
title: "3377. 使两个整数相等的数位操作"
aliases: ["yiduobo的每日leetcode 3377.使两个整数相等的数位操作"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/math", "leetcode/number-theory", "leetcode/shortest-path", "leetcode/heap-priority-queue", "题单/图论算法", "题单/图论算法/三-最短路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28911524034"
zhihu_id: "28911524034"
zhihu_title: "yiduobo的每日leetcode 3377.使两个整数相等的数位操作"
question_id: "3377"
question: "使两个整数相等的数位操作"
problem_url: "https://leetcode.cn/problems/digit-operations-to-make-two-integers-equal/"
difficulty: "Medium"
rating: 2186
created: "2025-03-09T00:51:18+08:00"
updated: "2025-03-09T00:51:18+08:00"
upvotes: 1
comments: 0
---

# 3377. 使两个整数相等的数位操作

> **[yiduobo的每日leetcode 3377.使两个整数相等的数位操作](https://zhuanlan.zhihu.com/p/28911524034) · 知乎 · 2025-03-09 · 赞同 1**
> 力扣：[3377. 使两个整数相等的数位操作](https://leetcode.cn/problems/digit-operations-to-make-two-integers-equal/) · Medium · 灵茶山艾府：[Dijkstra 最短路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3377.使两个整数相等的数位操作

[3377. 使两个整数相等的数位操作 - 力扣（LeetCode）](https://leetcode.cn/problems/digit-operations-to-make-two-integers-equal/description/)

题目给出两个整数n和m，n和m都不超过10000，且这两个整数的数位相同。

接下来需要对n执行若干次操作，使得n变为m。每次操作，都可以将n中任意不为9的数位增加1，或者将任意部位0的数位减去1。另外要求任意时刻n都不能为质数，也就是一开始以及每次操作后n都不能为质数。

进行这一系列操作的代价为n在变化过程中所有值之和，问将n变为m的最小代价。若无法变化，则返回-1。

首先考察特殊情况。如果n或者m为质数，那么可以直接返回-1，因为题目要求任意时刻n不能为质数。

接下来处理一般情况。由于n和m都不超过10000，且变换过程中还有非质数的限制，因此可以将每个非质数都视为图中的点，而如果x经过操作可以变为y，那么设置一条从x出发到y的边，这条边的权重就是y。接下来只需从n开始做dijkstra，到达m的最短距离即为最终答案。

具体实现上，不需要真的建图，只需对于当前的x，实时计算其可以变换得到的且不为质数的y，然后使用y来更新dijkstra算法使用的堆即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        
        def check(x, prime):
            if x not in prime:
                if x <= 1:
                    prime[x] = False
                else:
                    prime[x] = True
                y = 2
                while y * y <= x:
                    if x % y == 0:
                        prime[x] = False
                        break
                    y += 1
            
            return not prime[x]

        prime = {}
        if not check(n, prime):
            return -1

        dis = {}
        heap = [(n, n)]
        

        while m not in dis and heap:
            d, x = heapq.heappop(heap)
            if x in dis:
                continue
            
            dis[x] = d

            tmp = x
            delta = 1
            while tmp:
                v = tmp % 10
                tmp //= 10
                if v > 0:
                    y = x - delta
                    if y not in dis and check(y, prime):
                        heapq.heappush(heap, (d + y, y))
                if v < 9:
                    y = x + delta
                    if y not in dis and check(y, prime):
                        heapq.heappush(heap, (d + y, y))
                
                delta *= 10

        return dis.get(m, -1)
```
