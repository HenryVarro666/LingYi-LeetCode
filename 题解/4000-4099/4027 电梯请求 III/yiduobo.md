---
title: "4027. 电梯请求III"
aliases: ["yiduobo的每日leetcode 4027.电梯请求III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2073916695496888651"
zhihu_id: "2073916695496888651"
zhihu_title: "yiduobo的每日leetcode 4027.电梯请求III"
question_id: "4027"
question: "电梯请求 III"
problem_url: "https://leetcode.cn/problems/elevator-requests-iii/"
difficulty: "Hard"
created: "2026-08-20T23:52:47+08:00"
updated: "2026-08-20T23:52:51+08:00"
upvotes: 0
comments: 0
---

# 4027. 电梯请求III

> **[yiduobo的每日leetcode 4027.电梯请求III](https://zhuanlan.zhihu.com/p/2073916695496888651) · 知乎 · 2026-08-20 · 赞同 0**
> 力扣：[4027. 电梯请求 III](https://leetcode.cn/problems/elevator-requests-iii/) · Hard · 灵茶山艾府：[两种方法：状压 DP / 区间 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4027.电梯请求III

<https://leetcode.cn/problems/elevator-requests-iii/description/>

题目给出一个整数n，表示一栋建筑的楼层数，楼层编号从0到n - 1。

同时给出一个整数start，表示电梯的起始层数，以及一个二维整数数组requests，其中requests\[index\] \= \[arrival\[index\], floor\[index\]\]，表示在时间arrival\[index\]发出一个前往楼层floor\[index\]的请求。requests的长度不超过16。

在时间0，电梯在楼层start。

每一秒，电梯可以向上移动一层、向下移动一层，或者停留在当前楼层。

一个请求只能在其到达时间后之后被处理。从请求到达时起，只要电梯在任意时刻位于该请求对应的楼层，那么该请求将被立即处理。

问处理所有请求所需的最短时间。

与之前的版本相比，这次有了arrival这一项，因此之前的做法就不再使用了，因为可能出现远端的请求先来需要先过去满足，然后再满足中间的请求。

好在本题的数据规模较小，因此可以使用状态压缩。令f[state][last]表示已经完成了state中的请求，且停留在last这个请求所在的楼层所需的最短时间，那么对于f[state][last]，可以先通过state ^ (1 \<\< last)找出前置状态pre_state。

若pre_state为0，那么就说明当前是处理的首个请求，所需的时间就是max(arrival[last], abs(floor[last] - start))，即至少需要花费start移动到floor[last]所需的时间，如果到了地方请求还没来，则需要在原地停留等到请求来为止。

若pre_state非0，则需要从0到len(request) - 1进行遍历，寻找pre_state对应的pre_last，要求满足pre_state在pre_last这一位上为1。接下来，考虑从f[pre_state][pre_last]转移到f[state][last]。

首先是移动的时间，为abs(floor[last] - floor[pre_last])，也就是说最早可以在f[pre_state][pre_last] + abs(floor[last] - floor[pre_last])。

另一方面，如果到地方了请求还没来，则必须等到请求来为止。

综合起来，就有f[state][last] \= max(arr[last], f[pre_state][pre_last] + abs(floor[last] - floor[pre_last]))。

全部计算完成后，min(f[-1])即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        """
        :type n: int
        :type start: int
        :type requests: List[List[int]]
        :rtype: int
        """
        
        m = len(requests)
        max_state = 1 << m
        f = [[None] * m for _ in range(max_state)]
        

        for state in range(1, max_state):
            for last in range(m):
                if (state & (1 << last)) == (1 << last):
                    arr, floor = requests[last]
                    pre_state = state ^ (1 << last)
                    if pre_state == 0:
                        f[state][last] = max(abs(floor - start), arr)
                    else:
                        for pre_last in range(m):
                            if (pre_state & (1 << pre_last)) == (1 << pre_last):
                                pre_floor = requests[pre_last][1]
                                cost = max(arr, f[pre_state][pre_last] + abs(floor - pre_floor))
                                if f[state][last] is None or f[state][last] > cost:
                                    f[state][last] = cost
        
        return min(f[-1])
```
