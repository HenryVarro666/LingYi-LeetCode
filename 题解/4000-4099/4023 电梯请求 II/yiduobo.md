---
title: "4023. 电梯请求II"
aliases: ["yiduobo的每日leetcode 4023.电梯请求II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073223631413498716"
zhihu_id: "2073223631413498716"
zhihu_title: "yiduobo的每日leetcode 4023.电梯请求II"
question_id: "4023"
question: "电梯请求 II"
problem_url: "https://leetcode.cn/problems/elevator-requests-ii/"
difficulty: "Hard"
created: "2026-08-19T02:06:00+08:00"
updated: "2026-08-19T02:06:00+08:00"
upvotes: 1
comments: 0
---

# 4023. 电梯请求II

> **[yiduobo的每日leetcode 4023.电梯请求II](https://zhuanlan.zhihu.com/p/2073223631413498716) · 知乎 · 2026-08-19 · 赞同 1**
> 力扣：[4023. 电梯请求 II](https://leetcode.cn/problems/elevator-requests-ii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4023.电梯请求II

<https://leetcode.cn/problems/elevator-requests-ii/description/>

题目给出一个整数n，表示一栋建筑的楼层数。楼层的编号从0到n - 1。n最大可达10^9。

同时给出一个整数start，表示电梯的起始楼层，以及一个整数数组requests，其中requests[index]是电梯需要到达的楼层。requests中所有楼层都是互不相同的，且requests的长度不超过1500。

在时刻0，电梯处于楼层start。requests中所有的请求都是同时发出的。

在所有请求被处理完之前的每一秒钟，电梯恰好移动一层，可以向上也可以向下。当电梯到达请求的楼层时，该请求会被立即处理。如果start出现在requests中，该请求将在时刻0处理。

对于每个未被处理的请求，每一秒钟都会收到1点惩罚。换言之，在时刻t处理一个请求，其对总惩罚的贡献是t。要求返回处理所有请求所需的最小总惩罚。

首先，基于题目的数据规模，令m \= len(requests)，那么O(m^2)的复杂度应该是比较理想的，也就是说这里的处理方法应该抛开n不谈，而是专注于处理requests中的请求。

基于这一点，同时requests中的请求都是同时到达的，因此在这里可以先将requests排序。这样一来，问题就可以转化为区间问题，因为电梯无论怎样移动，其经过的楼层必然是一个连续的区间，其对应到requests中也必然是连续的区间，因此在这里很自然想到一种动态规划的算法：令f[start][end]表示处理requests中start到end这一段请求，且电梯最终停留在requests[start]时的最小总惩罚，而g[start][end]则表示最终停留在requests[end]时的最小总惩罚。

直观感觉上，f[start][end]以及g[start][end]应该从f[start + 1][end]、g[start + 1][end]以及f[start][end - 1]、g[start][end - 1]转移过去，也就是向两侧扩展，完成requests[start]或者requests[end]。但是需要注意的是，基于状态的定义，此处的转移需要用到当前的总耗时，但这一点在状态没有、也不方便体现，因此在这里不妨换一种方法来思考，即当前这次行动对总惩罚的贡献：对于当前的f[start][end]以及g[start][end]，其区间长度length为end - start + 1，这也恰好是处理完的请求数量，也就是说还没有处理的请求数量就是n - length，这些请求都将会受到本次移动的耗时的惩罚，再加上本次行动自身收到的惩罚，因此在这里就相当于在前置状态的基础上，加上move_cost \* (n - length + 1)，其中move_cost表示f和g从前置状态转移过来时对应的端点在requests中的距离。

具体来说：

1、对于f[start][end]，可以从f[start + 1][end]或者g[start + 1][end]转移过来。

从f[start + 1][end]到f[start][end]，相当于从start + 1走到start，move_cost就是requests[start + 1] - requests[start]。

从g[start + 1][end]到f[start][end]，相当于从end走到start，move_cost就是requests[end] - requests[start]。

2、对于g[start][end]，可以从f[start][end - 1]或者g[start][end - 1]转移过来。

从f[start][end - 1]到g[start][end]，相当于从start走到end，move_cost就是requests[end] - requests[start]。

从g[start][end - 1]到g[start][end]，相当于从end - 1走到end，move_cost就是requests[end] - requests[end - 1]。

全部计算完成后，f[0][-1]和g[0][-1]中的较小值即为最终答案。

另外，在具体实现上，可以遵从常规区间动态规划的处理方法，即先从小到大枚举区间长度length，然后再枚举区间起点start，计算区间终点start + length - 1，然后再进行计算。

最后附上python代码：

```python
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        """
        :type n: int
        :type start: int
        :type requests: List[int]
        :rtype: int
        """
        
        if start not in requests:
            requests.append(start)
        requests.sort()
        index = requests.index(start)

        n = len(requests)
        f = [[None] * n for _ in range(n)]
        g = [[None] * n for _ in range(n)]
        f[index][index] = 0
        g[index][index] = 0

        for length in range(2, n + 1):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                
                if f[start + 1][end] is not None:
                    cost = f[start + 1][end] + (requests[start + 1] - requests[start]) * (n - length + 1)
                    if f[start][end] is None or f[start][end] > cost:
                        f[start][end] = cost
                if g[start + 1][end] is not None:
                    cost = g[start + 1][end] + (requests[end] - requests[start]) * (n - length + 1)
                    if f[start][end] is None or f[start][end] > cost:
                        f[start][end] = cost
                
                if f[start][end - 1] is not None:
                    cost = f[start][end - 1] + (requests[end] - requests[start]) * (n - length + 1)
                    if g[start][end] is None or g[start][end] > cost:
                        g[start][end] = cost
                if g[start][end - 1] is not None:
                    cost = g[start][end - 1] + (requests[end] - requests[end - 1]) * (n - length + 1)
                    if g[start][end] is None or g[start][end] > cost:
                        g[start][end] = cost

        res = None
        if f[0][-1] is not None and (res is None or res > f[0][-1]):
            res = f[0][-1]
        if g[0][-1] is not None and (res is None or res > g[0][-1]):
            res = g[0][-1]
        return res
```
