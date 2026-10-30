---
title: "2258. 逃离火灾"
aliases: ["yiduobo的每日leetcode 2258.逃离火灾"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/binary-search", "题单/二分算法", "题单/网格图", "题单/二分算法/二-二分答案", "题单/网格图/五-综合应用"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/547825554"
zhihu_id: "547825554"
zhihu_title: "yiduobo的每日leetcode 2258.逃离火灾"
question_id: "2258"
question: "逃离火灾"
problem_url: "https://leetcode.cn/problems/escape-the-spreading-fire/"
difficulty: "Hard"
rating: 2347
created: "2022-07-30T01:24:49+08:00"
updated: "2022-07-30T01:24:49+08:00"
upvotes: 1
comments: 0
---

# 2258. 逃离火灾

> **[yiduobo的每日leetcode 2258.逃离火灾](https://zhuanlan.zhihu.com/p/547825554) · 知乎 · 2022-07-30 · 赞同 1**
> 力扣：[2258. 逃离火灾](https://leetcode.cn/problems/escape-the-spreading-fire/) · Hard · 灵茶山艾府：[【图解】两种方法：二分答案 / 直接计算（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2258.逃离火灾

[力扣](https://leetcode.cn/problems/escape-the-spreading-fire/)

题目已经明确提到了可能出现怎么都走不到安全屋，或者无论等多久都可以走到安全屋这两种特殊情况，那么首先就需要想办法判断当前的情况是否属于其中之一。

首先是无论如何都走不到安全屋。这种情况可以认为是人不经过等待直接开始逃生，但是也无法到达安全屋，那么可以直接先bfs一趟来模拟人能否走到安全屋。本题的bfs与常规的bfs有所区别的是需要让火和人交替地走，而根据样例2的提示，应该按照火先走人后走的顺序来进行bfs。但是需要注意有一种特殊情况是如果火和人同一轮走到了安全屋，那么也算人成功到达。

另外，与常规bfs的去重逻辑不同，本题火的去重逻辑是不能走回火走过的地方，但是可以走到人走过的地方，而相对的，人的去重逻辑是既不能走回人走过的地方，也不能走到火走过的地方。

一趟bfs过后，就可以知道人是否可能走到安全屋。如果不行，那么直接返回-1，否则继续考虑第二种情况，是不是人无论等多久都没问题。在这里只需要单独对火进行bfs，考察火最终能否走到安全屋就行了。如果火最终走不到安全屋，那么人无论等多久都没关系。

这里有一个问题是，是否可能出现火走不到安全屋，但是依然阻断了人到安全屋的路径呢？答案是不可能的。因为经过了最开始的bfs可以明确人是一定可以走到安全屋的，那么如果火能走到人能到达的地方，火也必然可以到达安全屋，这与一开始火走不到安全屋的假设矛盾了。

到了这里，就已经排除了两种特殊情况。此时则需要考虑人最多可以在原地耽误多久。一个直观的想法是，耽误的越久，出事的概率就越大，因此可以二分这个耽误的时间mid。二分的初始下界自然是0，而上界就是第二步中计算的火走到安全屋的时间。

对于当前二分到的mid，需要让火先走mid轮，然后再按照最开始火走一步人走一步的方式进行bfs，判断人最终能否到达安全屋。如果能到达，那么就更新二分的下界为mid，否则更新二分我的上界为mid - 1。

最后附上python代码：

```python
class Solution(object):
    def maximumMinutes(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        m = len(grid)
        n = len(grid[0])

        fire_list = []

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fire_list.append([i, j])
        
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        def bfs(person_pos, fire_pos, wait_time):
            fire_q = fire_pos[:]
            fire_l = 0
            fire_r = len(fire_q)

            fire_used = set()
            for x, y in fire_pos:
                fire_used.add(x * n + y)

            for _ in range(wait_time):
                for nowx, nowy in fire_q[fire_l : fire_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in fire_used:
                            fire_q.append([x, y])
                            fire_used.add(x * n + y)
            
                fire_l, fire_r = fire_r, len(fire_q)

            if m * n - 1 in fire_used:
                return -1

            person_q = person_pos[:]
            person_l = 0
            person_r = len(person_q)

            person_used = set()
            for x, y in person_pos:
                person_used.add(x * n + y)
            
            step = 0
            while person_l < person_r:
                step += 1
                for nowx, nowy in fire_q[fire_l : fire_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0 and x * n + y not in fire_used:
                            fire_q.append([x, y])
                            fire_used.add(x * n + y)
                
                fire_l, fire_r = fire_r, len(fire_q)

                for nowx, nowy in person_q[person_l : person_r]:
                    for index in range(4):
                        x = nowx + dx[index]
                        y = nowy + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 0:
                            next_key = x * n + y
                            if next_key == m * n - 1:
                                return step
                            
                            if next_key not in person_used and next_key not in fire_used:
                                person_q.append([x, y])
                                person_used.add(next_key)
                
                person_l, person_r = person_r, len(person_q)

                if m * n - 1 in fire_used:
                    break

            return -1

        g = grid[:]
        if bfs([[0, 0]], fire_list, 0) == -1:
            return -1
        
        fire_time = bfs(fire_list, [], 0)

        if fire_time == -1:
            return 10 ** 9
        
        l = 0
        r = fire_time
        while l < r:
            mid = (l + r + 1) >> 1
            if bfs([[0, 0]], fire_list, mid) != -1:
                l = mid
            else:
                r = mid - 1
        
        return l
```
