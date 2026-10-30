---
title: "2638. 统计K-Free子集的总数"
aliases: ["yiduobo的每日leetcode 2638.统计K-Free子集的总数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/sorting", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646401269"
zhihu_id: "646401269"
zhihu_title: "yiduobo的每日leetcode 2638.统计K-Free子集的总数"
question_id: "2638"
question: "统计 K-Free 子集的总数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-k-free-subsets/"
difficulty: "Medium"
created: "2023-07-27T23:35:52+08:00"
updated: "2023-07-27T23:35:52+08:00"
upvotes: 0
comments: 0
---

# 2638. 统计K-Free子集的总数

> **[yiduobo的每日leetcode 2638.统计K-Free子集的总数](https://zhuanlan.zhihu.com/p/646401269) · 知乎 · 2023-07-27 · 赞同 0**
> 力扣：[2638. 统计 K-Free 子集的总数](https://leetcode.cn/problems/count-the-number-of-k-free-subsets/) · Medium · 灵茶山艾府：[同余分组+打家劫舍（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2638.统计K-Free子集的总数

[力扣](https://leetcode.cn/problems/count-the-number-of-k-free-subsets/)

之前好像遇到过一个类似的题，但是记不清楚题号了，不过处理思路还是一样的，首先将所有数按照对k取模的余数分组。不同组的数之差的绝对值必然不会是k的倍数，也就意味着不同组之间的数可以分开处理，然后使用乘法原理计算最终合法的子集数目。

对于同一组内的数，不妨设这一组数对K取模的余数都为r，那么组内的数就可以写成xk + r的形式，其中x为自然数。当组内的两个数满足v1 \= x1 \* k + r，v2 \= (x1 + 1) \* k + r时，这两个数之差的绝对值就是k，也就是说这两个数不能同时加入到子集中，问题到了这里就转化成了类似打家劫舍的动态规划问题。

由于nums中的最大值为1000，因此上面的x最多也只能取到1000，于是可以令f[i]表示对于当前分组中，所有对应的x取值在0到i - 1之间的数可以选出的合法子集数目。

那么对于f[i]，首先边界条件有f[0] \= 1，f[1] \= 2^cnt[0]，这里的cnt[i]表示x取值为i的数的个数，那么2^cnt[i]就表示这cnt[i]个数可选可不选，一共有2^cnt[i]种方案。

对于i >\= 2的情况，则存在两种选择。第一种是完全放弃x \= i - 1，于是可以初始化f[i] \= f[i - 1]。而如果选择x \= i - 1，那么就不能选择x \= i - 2，于是就有f[i] +\= f[i - 2] \* (2^cnt[i - 1] - 1)。这里减一的理由是2^cnt[i - 1]里面存在一种空集的情况，这不符合选择x \= i - 1的前提。

计算完f后，将f[-1]累乘到答案中，然后继续按同样的方式处理下一组余数相同的数即可。

最后附上python代码：

```python
class Solution(object):
    def countTheNumOfKFreeSubsets(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        r_dict = {}
        for v in nums:
            r = v % k
            v /= k
            if r not in r_dict:
                r_dict[r] = []
            r_dict[r].append(v)
        
        res = 1
        for r in r_dict:
            cnt = [0] * 1001
            for v in r_dict[r]:
                cnt[v] += 1
                
            f = [1, 1 << (cnt[0])]
            for v in range(1, 1001):
                f.append(f[-1] + f[v - 1] * ((1 << cnt[v]) - 1))

            res *= f[-1]

        return res
```
