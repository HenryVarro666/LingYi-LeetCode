---
title: "3540. 访问所有房屋的最短时间"
aliases: ["yiduobo的每日leetcode 3540.访问所有房屋的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907574139033752193"
zhihu_id: "1907574139033752193"
zhihu_title: "yiduobo的每日leetcode 3540.访问所有房屋的最短时间"
question_id: "3540"
question: "访问所有房屋的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-visit-all-houses/"
created: "2025-05-18T23:33:42+08:00"
updated: "2025-05-18T23:33:42+08:00"
upvotes: 1
comments: 0
---

# 3540. 访问所有房屋的最短时间

> **[yiduobo的每日leetcode 3540.访问所有房屋的最短时间](https://zhuanlan.zhihu.com/p/1907574139033752193) · 知乎 · 2025-05-18 · 赞同 1**
> 力扣：[3540. 访问所有房屋的最短时间](https://leetcode.cn/problems/minimum-time-to-visit-all-houses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3540.访问所有房屋的最短时间

[3540. 访问所有房屋的最短时间 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-time-to-visit-all-houses/description/)

题目给出两个整数数组forward和backward，长度都为n。另外给出一个整数数组queries。

现在有n个按环状排列的房屋，这些房屋的连接方式很特殊：

对于在0到n - 2之间的房屋index，有一条长度为forward[index]的单行线连接到房屋index + 1，另外位于n - 1处的房屋则有一条长度为forward[n - 1]的单行线连接到房屋0。

对于在1到n - 1之间的房屋index，有一条长度为backward[index]的单行线连接到房屋index - 1，另外位于0处的房屋则有一条长度为forward[0]的单行线连接到房屋n - 1。

现在要求从房屋0开始，按顺序依次访问queries中的房屋，问访问完所有房屋所需的最小时间。

由于必须按顺序进行访问，那么queries实际上可以拆分为若干组询问，每个询问都是计算两个房屋间的最短距离，累加起来即为最终答案。

对于任意两个房屋间的最短距离，基于本题中道路的情况，只能选择正序或者逆序然后套圈这两种走法。具体来说，对于当前位置now以及目标位置nxt：

1、若now \< nxt：

可以沿着forward的方向走到nxt，所需的代价就是

forward[now] + forward[now + 1] + ... + forward[nxt - 1]

也可以沿着backward的方向走到0，然后套圈到n - 1，再从n - 1开始沿着backward的方向走到nxt，所需的代价分别为

backward[1] + backward[2] + ... backward[now]

backward[0]

backward[n - 1] + backward[n - 2] + ... backward[nxt + 1]

对于这类区间和问题，还是可以转化为前缀和或者后缀和来求解。在这里令ps_f和ss_b分别表示forward的前缀和以及backward的后缀和。为了方便计算，对这两个数组都额外设置一个值为0的下标0元素，也就是说

ps_f[0] \= 0，而对于index > 0时，有

ps_f[index] \= forward[0] + forward[1] + ... + forward[index - 1]

同样的，ss_b[n - 1] \= 0，而对于index \< n - 1时，有

ss_b[index] \= backward[n - 1] + backward[n - 2] + ... + backward[index + 1]

这样一来，上面两种走法的代价就可以写作

ps_f[nxt] - ps_f[now]

以及

(ss_b[0] - ss_b[now]) + backward[0] + ss_b[nxt]

综合起来，所需的最小代价就是min(ps_f[nxt] - ps_f[now], (ss_b[0] - ss_b[now]) + backward[0] + ss_b[nxt])

2、若now > nxt：

与情况1类似，如果沿着backward方向走到nxt，所需的代价就是

backward[now] + backward[now - 1] + ... + backward[nxt + 1] \= ss_b[nxt] - ss_b[now]

另一方面，如果沿着forward方向走到n - 1，然后套圈到0，再从0开始沿着forward方向走到nxt，所需的分别为

forward[now] + forward[now + 1] + ... + forward[n - 2] \= ps_f[n - 1] - ps_f[now]

forward[n - 1]

forward[0] + forward[1] + ... + forward[nxt - 1] \= ps_f[nxt]

综合起来，所需的最小代价就是min(ss_b[nxt] - ss_b[now], ps_f[n - 1] - ps_f[now] + forward[n - 1] + ps_f[nxt])

最后附上python代码：

```python
class Solution(object):
    def minTotalTime(self, forward, backward, queries):
        """
        :type forward: List[int]
        :type backward: List[int]
        :type queries: List[int]
        :rtype: int
        """
        
        n = len(forward)

        ps_f = [0]
        for v in forward[:n - 1]:
            ps_f.append(ps_f[-1] + v)
        
        ss_b = [0]
        for v in backward[n - 1: 0: -1]:
            ss_b.append(ss_b[-1] + v)
        ss_b.reverse()

        res = 0
        now = 0
        for nxt in queries:
            if now < nxt:
                res += min(ps_f[nxt] - ps_f[now], ss_b[0] - ss_b[now] + backward[0] + ss_b[nxt])
            else:
                res += min(ss_b[nxt] - ss_b[now], ps_f[-1] - ps_f[now] + forward[-1] + ps_f[nxt])
            
            now = nxt
        
        return res
```
