---
title: "3987. 处理所有元素的成本"
aliases: ["yiduobo的每日leetcode 3987.处理所有元素的成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/math", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2059685765777561269"
zhihu_id: "2059685765777561269"
zhihu_title: "yiduobo的每日leetcode 3987.处理所有元素的成本"
question_id: "3987"
question: "处理所有元素的成本"
problem_url: "https://leetcode.cn/problems/minimum-total-cost-to-process-all-elements/"
difficulty: "Medium"
rating: 1550
created: "2026-07-12T17:21:03+08:00"
updated: "2026-07-12T17:21:04+08:00"
upvotes: 1
comments: 0
---

# 3987. 处理所有元素的成本

> **[yiduobo的每日leetcode 3987.处理所有元素的成本](https://zhuanlan.zhihu.com/p/2059685765777561269) · 知乎 · 2026-07-12 · 赞同 1**
> 力扣：[3987. 处理所有元素的成本](https://leetcode.cn/problems/minimum-total-cost-to-process-all-elements/) · Medium · 灵茶山艾府：[模拟 / 脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3987.处理所有元素的成本

<https://leetcode.cn/problems/minimum-total-cost-to-process-all-elements/description/>

题目给出一个整数数组nums以及一个整数k。

在一开始，拥有k单位的资源。

接下来，需要从左到右依次处理nums中的元素。处理第index个元素需要消耗nums[index]单位的资源。

若当前可用资源少于nums[index]，则需要执行一次操作，使得可用资源增加k。第一次执行操作的成本为1，第二次的成本为2，依次类推。

问处理完所有元素所需的最小总成本，最终答案对10^9 + 7取模。

根据题目的秒数，执行题目中的操作并不是很复杂，因此直接模拟计算是完全可行的。

具体来说，使用一个变量now记录当前剩余的资源，初始化为k，另外使用一个变量记录当前操作的代价，初始化为1。

接下遍历nums，对于当前遍历到的nums[index]：

- 若now大于等于nums[index]，那么无需操作，此时将now减去nums[index]即可。
- 若now小于nums[index]，那么就需要执行若干次操作，直到now大于等于nums[index]。在这里可以记需要补充的最少资源量need \= nums[index] - now，那么所需的操作次数就是t \= (need - 1) // k + 1。得到了t之后，执行这t次操作所需的代价就是cost + (cost + 1) + ... + (cost + t - 1) \= (cost + cost + t - 1) \* t // 2，将其累加到答案中，然后将now更新为now + t \* k - nums[index]，将cost加上t即可。

更进一步的，由于这里的资源是不会虚空消耗的，也就是说上一次补充的资源使用之后，还可以累加到之后使用，因此在这里完全可以将nums视为一个整体，先计算nums之和s，然后计算将初始的k补充到大于等于s所需的操作次数，然后计算总代价就行了。补充所需的次数和总代价的计算方式则与分步骤计算的方式完全相同。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        s = sum(nums)
        if s <= k:
            return 0
        
        need = s - k
        mod = 10 ** 9 + 7
        t = (need - 1) // k + 1
        return (1 + t) * t // 2 % mod
```
