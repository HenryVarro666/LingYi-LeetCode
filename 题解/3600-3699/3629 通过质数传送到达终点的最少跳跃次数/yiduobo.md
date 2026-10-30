---
title: "3629. 通过质数传送达到终点的最少跳跃次数"
aliases: ["yiduobo的每日leetcode 3629.通过质数传送达到终点的最少跳跃次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "题单/图论算法", "题单/数学算法", "题单/图论算法/一-图的遍历", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945945238708396856"
zhihu_id: "1945945238708396856"
zhihu_title: "yiduobo的每日leetcode 3629.通过质数传送达到终点的最少跳跃次数"
question_id: "3629"
question: "通过质数传送到达终点的最少跳跃次数"
problem_url: "https://leetcode.cn/problems/minimum-jumps-to-reach-end-via-prime-teleportation/"
difficulty: "Medium"
rating: 2139
created: "2025-09-01T20:45:58+08:00"
updated: "2025-09-01T20:45:58+08:00"
upvotes: 0
comments: 0
---

# 3629. 通过质数传送达到终点的最少跳跃次数

> **[yiduobo的每日leetcode 3629.通过质数传送达到终点的最少跳跃次数](https://zhuanlan.zhihu.com/p/1945945238708396856) · 知乎 · 2025-09-01 · 赞同 0**
> 力扣：[3629. 通过质数传送到达终点的最少跳跃次数](https://leetcode.cn/problems/minimum-jumps-to-reach-end-via-prime-teleportation/) · Medium · 灵茶山艾府：[两种方法：正向 BFS / 逆向 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3629.通过质数传送到达终点的最少跳跃次数

[3629. 通过质数传送到达终点的最少跳跃次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-jumps-to-reach-end-via-prime-teleportation/description/)

题目给出一个长度为n的整数数组nums，要求从下标0出发到达下标n - 1。当处于下标i，可以执行一下操作之一：

1、移动到相邻格子：也就是移动到i - 1或者i + 1，前提是目标下标没有越界

2、质数传送：若nums[i]是一个质数p，那么可以立刻跳跃到任意满足nums[j] % p \= 0的下标j处，且j不等于i

问到达下标n - 1所需的最少跳跃次数

如果把每种下标都视为图中的点，那么对于每个点，其与前后相邻的两个点之间有一边，若其对应的数值是质数，其与所有是该元素倍数的下标点之间都有一条有向边，而问题则变成了求0到n - 1的最短路。由于边没有权重，因此在这里可以直接使用bfs来计算。

再具体实现时，不需要真的建立有向边，而是可以使用哈希表记录每种数值对应的所有下标。在bfs的过程中，如果碰到了质数p，那么就可以从p开始，以p为步长循环，对于当前遍历到的x，通过哈希表找到值为x的那些下标。

值得一提的是，除了常规的访问过的下标去重之外，还可以增加一项访问过的数值去重，也就是在上面执行质数传送时，若x对应的下标已经都被访问过了，那么接下来就没有必要再向x对应的下标进行质数传送了。

最后附上python代码：

```python
class Solution(object):
    def minJumps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = max(nums)
        n = len(nums)
        vis_num = [False] * (ma + 1)
        vis_index = [False] * n
        index_list = [[] for _ in range(ma + 1)]
        for index, v in enumerate(nums):
            index_list[v].append(index)
        
        prime = [True] * (ma + 1)
        prime[0] = False
        prime[1] = False
        v = 2
        while v <= ma:
            if prime[v]:
                for x in range(v + v, ma + 1, v):
                    prime[x] = False
            v += 1

        q = [0]
        head, tail = 0, 1
        vis_index[0] = True
        res = 0
        while head < tail:
            if vis_index[n - 1]:
                return res
            res += 1
            for index in q[head : tail]:
                v = nums[index]
                if prime[v]:
                    for x in range(v, ma + 1, v):
                        if not vis_num[x]:
                            for nxt_index in index_list[x]:
                                if not vis_index[nxt_index]:
                                    q.append(nxt_index)
                                    vis_index[nxt_index] = True
                            vis_num[x] = True

                if index > 0 and not vis_index[index - 1] and not vis_num[nums[index - 1]]:
                    q.append(index - 1)
                    vis_index[index - 1] = True
                if index < n - 1 and not vis_index[index + 1] and not vis_num[nums[index + 1]]:
                    q.append(index + 1)
                    vis_index[index + 1] = True
        
            head, tail = tail, len(q)

        return res
```
