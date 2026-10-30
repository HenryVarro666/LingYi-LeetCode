---
title: "2919. 使数组变美的最小增量运算数"
aliases: ["yiduobo的每日leetcode 2919.使数组变美的最小增量运算数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/665118142"
zhihu_id: "665118142"
zhihu_title: "yiduobo的每日leetcode 2919.使数组变美的最小增量运算数"
question_id: "2919"
question: "使数组变美的最小增量运算数"
problem_url: "https://leetcode.cn/problems/minimum-increment-operations-to-make-array-beautiful/"
difficulty: "Medium"
rating: 2031
created: "2023-11-05T04:41:15+08:00"
updated: "2023-11-05T04:41:15+08:00"
upvotes: 1
comments: 0
---

# 2919. 使数组变美的最小增量运算数

> **[yiduobo的每日leetcode 2919.使数组变美的最小增量运算数](https://zhuanlan.zhihu.com/p/665118142) · 知乎 · 2023-11-05 · 赞同 1**
> 力扣：[2919. 使数组变美的最小增量运算数](https://leetcode.cn/problems/minimum-increment-operations-to-make-array-beautiful/) · Medium · 灵茶山艾府：[巧妙设计状态+选或不选（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2919.使数组变美的最小增量运算数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-increment-operations-to-make-array-beautiful/description/)

题目要求数组中所有长度大于等于3的子数组中的最大值都大于等于k，那么实际上就是要求所有长度为3的子数组中至少存在一个大于等于k的数。理由是所有大于等于3的子数组至少包含了一个长度为3的子数组，而所有长度为3的子数组中存在一个大于等于k的数时，其中的最大值也必然大于等于k，因此就满足了所有长度大于等于3的子数组中的最大值都大于等于k。

对于这类问题，一种常见的状态表示为f[index]表示下标到index为止的前缀满足了题目要求，同时nums[index]如何如何。对于本题，就是当下标到index为止的前缀满足了题目要求，同时nums[index] >\= k时所需的最小修改次数。

首先考虑边界情况。对于数组中第一个长度为3的子数组，只要其中有一个数大于等于k就行了，那么为了适配f的定义，需要从下标0遍历到2，若当前的nums[index] >\= k，那么就有f[index] \= 0，否则f[index] \= k - nums[index]。

接下来是index >\= 3的情况。对于当前的nums[index]，若nums[index] >\= k，那么就有f[index] \= min(f[index - 1], f[index - 2], f[index - 3])，否则就有f[index] \= min(f[index - 1], f[index - 2], f[index - 3]) + k - nums[index]。理由是在这里保证了nums[index]一定大于等于k，因此nums[index - 2 : index + 1]这个子数组是满足题目要求的，而对于三个前置状态：

1、对于之前的f[index - 1]必然是可行的，无需讨论

2、对于f[index - 2]，由于nums[index - 2]在f[index - 2]对应的状态中是大于等于k，因此这种情况下nums[index - 3 : index]这个子数组也是满足条目要求的，而更前面的子数组则都包含在了f[index - 2]的定义中，因此也可以用f[index - 2]来更新f[index]

3、对于f[index - 3]，与情况2类似，nums[index - 3]可以覆盖住nums[index - 4: index - 1]以及nums[index - 3: index]这两个子数组，而起点在nums[index - 5]之前的长度为3的子数组则都被f[index - 3]包含住了，因此也可以用[index - 3]来更新f[index]

需要注意的是，计算完成后最终答案应该是min(f[-1], f[-2], f[-3])而不是传统的f[-1]。

另外，由于上面f的迭代只用到了最近的三个下标位置，因此可以使用三个变量迭代来省去f数组的空间。

最后附上python代码：

```python
class Solution(object):
    def minIncrementOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = k - min(k, nums[2])
        g = k - min(k, nums[1])
        h = k - min(k, nums[0])
        
        for v in nums[3:]:
            delta = k - min(k, v)
            f, g, h = min(f, g, h) + delta, f, g
        
        return min(f, g, h)
```
