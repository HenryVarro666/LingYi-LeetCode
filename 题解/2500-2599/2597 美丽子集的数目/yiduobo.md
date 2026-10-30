---
title: "2597. 美丽子集的数目"
aliases: ["yiduobo的每日leetcode 2597.美丽子集的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/backtracking", "leetcode/ordered-set", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643960046"
zhihu_id: "643960046"
zhihu_title: "yiduobo的每日leetcode 2597.美丽子集的数目"
question_id: "2597"
question: "美丽子集的数目"
problem_url: "https://leetcode.cn/problems/the-number-of-beautiful-subsets/"
difficulty: "Medium"
rating: 2023
created: "2023-07-17T02:10:54+08:00"
updated: "2023-07-17T02:10:54+08:00"
upvotes: 0
comments: 0
---

# 2597. 美丽子集的数目

> **[yiduobo的每日leetcode 2597.美丽子集的数目](https://zhuanlan.zhihu.com/p/643960046) · 知乎 · 2023-07-17 · 赞同 0**
> 力扣：[2597. 美丽子集的数目](https://leetcode.cn/problems/the-number-of-beautiful-subsets/) · Medium · 灵茶山艾府：[三种方法：回溯 / 动态规划 / O(n) 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2597.美丽子集的数目

[力扣](https://leetcode.cn/problems/the-number-of-beautiful-subsets/)

题目的数据规模很小，因此可以直接暴力dfs，不过还存在更好的做法。

题目要求子集中的任意两数之差不等于k，那么可以在一开始根据这些数对k取模的结果，将这些数分为k类。可以发现，不同类直接的数之差必然不是k的倍数，因此也必然不会等于k，因此在这里只需分别讨论每一类可以得到的合法子集数目，然后相乘就得到了最终答案。

考虑模k余r的这一类数。对于这类数，若子集中选择了某个值为xk + r的数，那么(x - 1)k + r以及(x + 1)k + r就不能选择。换言之，如果将这些数按整除k的结果排序的话，问题就变成了给出一个数组，从中选出一个子序列，要求不能选择两个值相邻的数，问最终可以得到的子序列数目。

对于这个问题，与之前的打家劫舍非常像，同样可以利用动态规划求解。令f[i]表示对于取值范围在0到i - 1时可以得到的子序列数目，那么对于f[i]：

1、首先边界情况。当i \= 0时，有f[i] \= 1，表示一个数都不选

2、接下来，当i \= 1时，有f[1] \= 2^cnt[0]，这里的cnt[i]表示i在数组中出现的次数，那么2^cnt[i]就是这cnt[i]个i可以任意选或者不选。需要注意，题目只是要求不能选择值相邻的数，但是可以选择值相同的数。

3、最后是i > 1的情况。此时可以不选择i - 1，那么就可以初始化f[i] \= f[i - 1]。另一方面，如果要选择i - 1，那么其必须跳过i - 2，因此就有f[i] +\= f[i - 2] \* ((2^cnt[i - 1]) - 1)，这里的2的幂次含义与上面相同，而减1则表示在这里需要去掉一个都不选的情况，因为这种情况以及被包含在了初始的f[i] \= f[i - 1]中。

计算完成后，将f[-1]累乘到答案中即可。

另外需要特别注意的是，最终答案需要额外减去1，因为在上面的计算中始终是包含空集的，那么最终通过乘法原理计算出来的方案数中也包含了空集这种情况，而题目要求的是非空集合，因此需要额外减去1。

最后附上python代码：

```python
class Solution(object):
    def beautifulSubsets(self, nums, k):
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
        
        return res - 1
```
