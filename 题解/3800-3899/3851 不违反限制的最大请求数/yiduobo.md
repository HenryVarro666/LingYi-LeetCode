---
title: "3851. 不违反限制的最大请求数"
aliases: ["yiduobo的每日leetcode 3851.不违反限制的最大请求数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011508585172079636"
zhihu_id: "2011508585172079636"
zhihu_title: "yiduobo的每日leetcode 3851.不违反限制的最大请求数"
question_id: "3851"
question: "不违反限制的最大请求数"
problem_url: "https://leetcode.cn/problems/maximum-requests-without-violating-the-limit/"
created: "2026-03-04T21:26:36+08:00"
updated: "2026-03-04T21:26:37+08:00"
upvotes: 1
comments: 0
---

# 3851. 不违反限制的最大请求数

> **[yiduobo的每日leetcode 3851.不违反限制的最大请求数](https://zhuanlan.zhihu.com/p/2011508585172079636) · 知乎 · 2026-03-04 · 赞同 1**
> 力扣：[3851. 不违反限制的最大请求数](https://leetcode.cn/problems/maximum-requests-without-violating-the-limit/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3851.不违反限制的最大请求数

<https://leetcode.cn/problems/maximum-requests-without-violating-the-limit/>

题目给出一个二维整数数组requests，其中requests\[index\] \= \[user\[index\], time\[index\]\]，表示user\[index\]在time\[index\]进行了一次请求。

另外给出两个整数k和window。

若存在某个时刻t，使得某个用户在时间区间[t, t + window]内的请求次数严格大于k次，那么这个用户就违反了限制。

现在可以丢弃任意数量的请求，问最多可以保留多少个请求，满足所有用户都没有违反限制。

为了方便计算，在这里可以先将所有请求按照时间从小到大进行排序，然后逐个处理。对于当前的请求[u, t]，若u在时间窗口[t - window, t]内的请求次数大于k次，那么就应该丢弃当前这次请求，理由是丢弃本次请求而不是丢弃前面的请求，能更有效的减轻后续窗口内的请求压力。

基于这一点，就可以对每个用户都维护一个队列，接下来按时间顺序遍历每个请求。对于当前请求[u, t]，先将u对应的队列中，请求时间在t - window之前的请求都从队首弹出，接下来，若队列的长度小于k，说明在时间窗口内[t - window, t]的请求次数小于k次，此时可以接受当前请求，于是可以将t加入到队列中并更新答案，反之，则需要丢弃当前请求，此时不需要执行任何操作。

最后附上python代码：

```python
class Solution(object):
    def maxRequests(self, requests, k, window):
        """
        :type requests: List[List[int]]
        :type k: int
        :type window: int
        :rtype: int
        """
        
        timestamp = {}
        res = 0
        for u, t in sorted(requests, key=lambda d:d[1]):
            if u not in timestamp:
                timestamp[u] = deque()
            
            while timestamp[u] and t - timestamp[u][0] > window:
                timestamp[u].popleft()
            
            if len(timestamp[u]) < k:
                timestamp[u].append(t)
                res += 1
        
        return res
```
