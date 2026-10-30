---
title: "3919. 在下标间移动的最小代价"
aliases: ["yiduobo的每日leetcode 3919.在下标间移动的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2034998027111379759"
zhihu_id: "2034998027111379759"
zhihu_title: "yiduobo的每日leetcode 3919.在下标间移动的最小代价"
question_id: "3919"
question: "在下标间移动的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-move-between-indices/"
difficulty: "Medium"
rating: 1777
created: "2026-05-05T14:48:48+08:00"
updated: "2026-05-05T14:48:52+08:00"
upvotes: 0
comments: 0
---

# 3919. 在下标间移动的最小代价

> **[yiduobo的每日leetcode 3919.在下标间移动的最小代价](https://zhuanlan.zhihu.com/p/2034998027111379759) · 知乎 · 2026-05-05 · 赞同 0**
> 力扣：[3919. 在下标间移动的最小代价](https://leetcode.cn/problems/minimum-cost-to-move-between-indices/) · Medium · 灵茶山艾府：[贪心 + 前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3919.在下标间移动的最小代价

<https://leetcode.cn/problems/minimum-cost-to-move-between-indices/description/>

题目给出一个单调递增的数组nums。

对于其中的每个下标x，令closest(x)表示使得abs(nums[x] - nums[y])最小的相邻下标。若两个相邻下标的差值相同，则选择较小的下标。

从任意下标x出发，可以通过一下两种方式移动：

- 移动到任意下标y，其代价为abs(nums[x] - nums[y])
- 移动到closest(x)，代价为1

另外给出一个二维数组queries，其中queries\[index\] \= \[l\[index\], r\[index\]\]，表示要求计算从l\[index\]移动到r\[index\]的最小总代价。

要求返回一个数组ans，其中ans[index]是第index个查询的答案。

首先，根据题目中移动的规则，再结合nums单调递增的特点，可以得到以下两个结论，以l \< r为例进行说明：

1、不走回头路：

从l出发，如果先走到某个小于l的位置p，再从p出发走到r，其所需的代价必然大于直接从l出发走到r的代价。理由是

- 若从p出发走到r的过程中经过了l，那么从l走到p，再从p走回l这一段就是无用功，是完全没有必要的。
- 若没有经过l，那么必然是从l左侧的某个位置x，直接使用第一种移动方式来到了l右侧的某个位置y，其代价为nums[y] - nums[x]，然而如果直接从l跳跃到y，其代价只需要nums[y] - nums[l]，即使不计算从l走到p再走到x的代价，单单只是走到y的代价就已经更小了。

综合起来，就可以得到的结论，不走回头路。

2、不进行跳跃操作：

由于nums单调递增，那么从x跳跃到y的总代价nums[y] - nums[x]，可以拆分为nums[y] - nums[y - 1] + nums[y - 1] - nums[y - 2] + ... + nums[x + 1] - nums[x]。在不考虑closest的前提下，其所需的代价就相当于从x一步一步走到y的代价。

另一方面，对于closest，其所需的代价为1，必然小于等于正常行走的代价，因此从x一步一步走到y，在不触发任何closest时所需的代价恰好等于直接从x跳跃到y的代价，而出发了closest，其所需代价只会更小不会更大。

基于上面的结论，对于每组询问最优的走法就是从l出发一步一步走到r。需要注意，由于closest的存在，在这里需要先进行一趟遍历，计算出从给每个位置向左走一步和向右走一步所需的代价，然后再正反两趟遍历，计算出正向行走的前缀和代价数组prefix，以及反向行走的后缀和代价数组suffix。最后再遍历所有询问，对于一组询问[l, r]，若l \< r，那么应该正向行走，答案就是prefix[r] - prefix[l]；若l \= r，那么答案为0；若l > r，那么应该反向行走，答案就是suffix[r] - suffix[l]。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(nums)
        to_left = [0] * n
        to_right = [0] * n

        for index in range(n):
            if index == 0:
                to_left[index] = 0
                to_right[index] = 1
            elif index == n - 1:
                to_right[index] = 0
                to_left[index] = 1
            else:
                left_dis = nums[index] - nums[index - 1]
                right_dis = nums[index + 1] - nums[index]
                if left_dis <= right_dis:
                    to_left[index] = 1
                    to_right[index] = right_dis
                else:
                    to_left[index] = left_dis
                    to_right[index] = 1
        
        suffix = [0]
        for index in range(n - 1, 0, -1):
            suffix.append(suffix[-1] + to_left[index])
        suffix.reverse()

        prefix = [0]
        for index in range(n - 1):
            prefix.append(prefix[-1] + to_right[index])
        
        res = []
        for x, y in queries:
            if x < y:
                res.append(prefix[y] - prefix[x])
            elif x == y:
                res.append(0)
            else:
                res.append(suffix[y] - suffix[x])
        
        return res
```
