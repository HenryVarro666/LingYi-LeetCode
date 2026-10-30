---
title: "1815. 得到新鲜甜甜圈的最多组数"
aliases: ["yiduobo的每日leetcode 1815.得到新鲜甜甜圈的最多组数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465548071"
zhihu_id: "465548071"
zhihu_title: "yiduobo的每日leetcode 1815.得到新鲜甜甜圈的最多组数"
question_id: "1815"
question: "得到新鲜甜甜圈的最多组数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-groups-getting-fresh-donuts/"
difficulty: "Hard"
rating: 2559
created: "2022-02-09T23:49:42+08:00"
updated: "2022-02-09T23:49:42+08:00"
upvotes: 0
comments: 0
---

# 1815. 得到新鲜甜甜圈的最多组数

> **[yiduobo的每日leetcode 1815.得到新鲜甜甜圈的最多组数](https://zhuanlan.zhihu.com/p/465548071) · 知乎 · 2022-02-09 · 赞同 0**
> 力扣：[1815. 得到新鲜甜甜圈的最多组数](https://leetcode.cn/problems/maximum-number-of-groups-getting-fresh-donuts/) · Hard · 灵茶山艾府：[位运算的魔法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1815.得到新鲜甜甜圈的最多组数

[力扣](https://leetcode-cn.com/problems/maximum-number-of-groups-getting-fresh-donuts/)

题目要求将group中的数分成k组，其中前k - 1组中数之和必须是batchSize的倍数，问最大的k是多少。

对于这个问题，第一时间想到的就是状态压缩动态规划，不巧的是这里的数据规模达到了30，常规的2次幂形式的状态压缩肯定是不行的，只能另想办法。

注意到这里的batchSize规模较小，那么在这里可以将这些数先按照对batchSize取模的值分组。模batchSize等于0的这一组显然是自成一派的，不需要与其他数组合，那么实际上就有余1到余batchSize - 1这一共batchSize - 1组。

一个自然的想法就是将每个组中剩余数的个数收集起来，通过哈希或其他方法作为状态表示。虽然看起来规模很大，但是实际上极限情况就可以认为是将30分成8个整数，这些整数乘积最大。按照分3分4的方法来做，极限情况也就是6个4和2个3，所有可能情况数只有不到40000种，完全是可以接受的。

令f[state]表示模batchSize的各个余数组为state这种情况时，可以分成的最大组数。那么对于f[state]而言，可以枚举各个不为0的剩余组，选择一个数加入当前的组。设选择完这个数之后的状态变为了next_state，那么就有f[next_state] \= max(f[next_state], f[state] + delta)，其中delta为当前这次选择是否新开了一组。对于delta取值的判断，由于从初始状态到state这个状态使用了哪些数是已知的，因此可以通过这些数的和s模batchSize得到当前组的和对batchSize的余数。若余数为0，说明从state到next_state相当于新开了一组，此时的delta就等于1，否则delta等于0。

具体实现上，我直接用python的tuple来做的状态表示，同时采用的是类bfs的写法，因为每一步操作之后剩余的数都是变少的。在bfs的队列表示中，额外添加了s，这样一来就无须在状态转移时再去临时计算s了。

最后附上python代码：

```python
class Solution(object):
    def maxHappyGroups(self, batchSize, groups):
        """
        :type batchSize: int
        :type groups: List[int]
        :rtype: int
        """

        cnt_list = [0] * batchSize
        for num in groups:
            cnt_list[num % batchSize] += 1
        
        q = [[tuple(cnt_list[1:]), 0]]
        l = 0
        r = 1
        f = {}
        f[q[0][0]] = 0
        while l < r:
            now_tuple, now_rem = q[l]
            if now_rem == 0:
                delta = 1
            else:
                delta = 0
            l += 1
            now_list = list(now_tuple)
            for index in range(batchSize - 1):
                if now_list[index] > 0:
                    now_list[index] -= 1
                    next_tuple = tuple(now_list)
                    next_rem = (now_rem + index + 1) % batchSize
                    now_list[index] += 1
                    if next_tuple not in f:
                        f[next_tuple] = f[now_tuple] + delta
                        q.append([next_tuple, next_rem])
                        r += 1
                    else:
                        f[next_tuple] = max(f[next_tuple], f[now_tuple] + delta)
        
        return f[tuple([0] * (batchSize - 1))] + cnt_list[0]
```
