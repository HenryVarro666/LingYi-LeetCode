---
title: "3671. 子序列美丽值求和"
aliases: ["yiduobo的每日leetcode 3671.子序列美丽值求和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/math", "leetcode/dynamic-programming", "leetcode/number-theory", "题单/常用数据结构", "题单/动态规划", "题单/数学算法", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/十一-优化-DP", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950704955028666085"
zhihu_id: "1950704955028666085"
zhihu_title: "yiduobo的每日leetcode 3671.子序列美丽值求和"
question_id: "3671"
question: "子序列美丽值求和"
problem_url: "https://leetcode.cn/problems/sum-of-beautiful-subsequences/"
difficulty: "Hard"
rating: 2647
created: "2025-09-20T18:40:20+08:00"
updated: "2025-09-20T18:40:26+08:00"
upvotes: 2
comments: 0
---

# 3671. 子序列美丽值求和

> **[yiduobo的每日leetcode 3671.子序列美丽值求和](https://zhuanlan.zhihu.com/p/1950704955028666085) · 知乎 · 2025-09-20 · 赞同 2**
> 力扣：[3671. 子序列美丽值求和](https://leetcode.cn/problems/sum-of-beautiful-subsequences/) · Hard · 灵茶山艾府：[倍数容斥 + 值域树状数组优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3671.子序列美丽值求和

[3671. 子序列美丽值求和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-beautiful-subsequences/description/)

题目给出一个长度为n的整数数组nums。其中n不超过10000，nums中的元素值大小不超过70000。

对于每个正整数g，定义g的美丽值为g与nums中符合要求的子序列数量的乘积，符合要求的子序列指的是严格递增，且最大公约数恰好为g的子序列。

问所有正整数g的美丽值之和。

本题涉及到子序列的最大公约数，而涉及到最大公约数的问题，则可以参考之前3312题的处理方法，先计算出每种公约数对应的合法子序列数目，然后从大到小逆序遍历这些公约数，对于当前遍历到的v，使用以v为公约数的合法子序列数目，减去所有以2v、3v、...、kv为最大公约数的合法子序列数目，就是以v为最大公约数的合法子序列数目了。

[yiduobo的每日leetcode 3312.查询排序后的最大公约数](https://zhuanlan.zhihu.com/p/1709794890)

例如[2, 4, 6, 8]，所有的子序列都是公约数为2时的合法子序列，一共有15种，但是其中[4]、[8]、[4, 8]这三个子序列的最大公约数为4，另外[6]和[8]这两个子序列的最大公约数分别为6和8，因此最大公约数为2的子序列就应该是15 - 3 - 2 \= 10个。

基于这一点，就可以先枚举所有可能的约数v，将nums中不是v的倍数的元素剔除掉。方便期间，将剩下元素组成的数组记为arr，那么在这里就需要计算出arr中上升子序列的数目。

对于这个问题，如果使用常规的f[index]表示arr的前index个元素可以构成的上升子序列数目，那么就有f[index] \= sum(f[p]) + 1，其中0 \<\= p \< index且arr[index] > arr[p]。不过这个算法的时间复杂度为O(n^2)，需要进行优化。

一种可行的处理方法是从值域的角度出发，将状态表示改为f\[v\]表示以v为结尾的上升子序列的数目，那么对于当前遍历到的arr\[index\]，就有f\[arr\[index\]\] \= f\[0\] + f\[1\] + ... + f\[arr\[index\] - 1\]。这是一个动态前缀和问题，使用树状数组就可以将时间复杂度优化到O(nlogm)了，其中m是nums中的最大值。

直观来看，最终的时间复杂度为O(Rlogm)，其中R为nums中所有元素的约数总数。对于1到70000中的所有元素x，取55440时约数数量最大，为120。另外，寻找约数的部分也需要考虑进来，也就是O(n \* sqrt(m))。

在具体实现上，不需要针对每个约数v都构建对应的arr，而是只需要构建对应的树状数组，并记录这个约数对应的合法的子序列数量tot就行了。计算完成后，再从大到小遍历每种约数，使用最上面提到的方法计算每种最大公约数对应的合法子序列数目，将其与最大公约数相乘后累加到最终答案中即可。

最后附上python代码：

```python
class Solution(object):
    def totalBeauty(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = max(nums)
        f = [[] for _ in range(ma + 1)]
        for g in range(1, ma + 1):
            f[g] = [0] * (ma // g + 1)

        mod = 10 ** 9 + 7

        def get(g, x):
            s = 0
            while x > 0:
                s += f[g][x]
                if s >= mod:
                    s -= mod
                x -= x & -x
            return s
        
        def add(g, x, v):
            while x < len(f[g]):
                f[g][x] += v
                if f[g][x] >= mod:
                    f[g][x] -= mod
                x += x & -x

        tot = [0] * (ma + 1)
        for v in nums:
            x = 1
            while x * x <= v:
                if v % x == 0:
                    y = v // x
                    end_y = get(x, y - 1) + 1
                    add(x, y, end_y)
                    tot[x] += end_y
                    if tot[x] >= mod:
                        tot[x] -= mod
                    if x != y:
                        end_x = get(y, x - 1) + 1
                        add(y, x, end_x)
                        tot[y] += end_x
                        if tot[y] >= mod:
                            tot[y] -= mod
                x += 1
        
        res = 0
        for v in range(ma, 0, -1):
            for x in range(v + v, ma + 1, v):
                tot[v] -= tot[x]
                if tot[v] < 0:
                    tot[v] += mod
            delta = tot[v] * v % mod
            res += delta
            if res >= mod:
                res -= mod
        
        return res
```
