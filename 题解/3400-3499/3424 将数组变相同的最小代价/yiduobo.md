---
title: "3424. 将数组变相同的最小代价"
aliases: ["yiduobo的每日leetcode 3424.将数组变相同的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1888709510215997132"
zhihu_id: "1888709510215997132"
zhihu_title: "yiduobo的每日leetcode 3424.将数组变相同的最小代价"
question_id: "3424"
question: "将数组变相同的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-make-arrays-identical/"
difficulty: "Medium"
rating: 1503
created: "2025-03-27T22:01:44+08:00"
updated: "2025-03-27T22:01:44+08:00"
upvotes: 0
comments: 0
---

# 3424. 将数组变相同的最小代价

> **[yiduobo的每日leetcode 3424.将数组变相同的最小代价](https://zhuanlan.zhihu.com/p/1888709510215997132) · 知乎 · 2025-03-27 · 赞同 0**
> 力扣：[3424. 将数组变相同的最小代价](https://leetcode.cn/problems/minimum-cost-to-make-arrays-identical/) · Medium · 灵茶山艾府：[脑筋急转弯+贪心+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3424.将数组变相同的最小代价

[3424. 将数组变相同的最小代价 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-to-make-arrays-identical/description/)

题目给出两个长度都为n的整数数组arr和brr，以及一个整数k。现在可以对arr执行以下操作任意次：

1、将arr分割成若干个连续的子数组，然后将这些子数组按任意顺序重新排列。这个操作的代价为k

2、选择arr中的任意元素，将其增加或者减少一个正整数x。这个操作的代价为x

问将arr变为brr所需的最小代价。

如果不考虑分割后重新排列的操作，那么所需的代价是很容易计算的。只需一趟遍历，对于每个下标index，计算arr[index]与brr[index]的差的绝对值，累加起来就是需要的代价。

接下来考虑分割后重新排列的情况。注意到这里的分割以及重新排列是没有限制的，因此完全可以将arr分割成若干长度为1的子数组然后重新排列。换言之，实际上就是可以通过k的代价将arr任意排列。而对于可以任意排列的arr，为了使得变换的代价最小，就应该让arr的最小值对上brr的最小值，arr的次小值对上brr的次小值，以此类推。于是可以将arr和brr都从小到大进行排序，然后再一趟遍历，依次计算差的绝对值并累加，再加上k即为需要的代价。

取以上两种情况代价的较小值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, arr, brr, k):
        """
        :type arr: List[int]
        :type brr: List[int]
        :type k: int
        :rtype: int
        """
        
        def calc(arr, brr):
            cost = 0
            for a, b in zip(arr, brr):
                cost += abs(a - b)
            return cost

        res = min(calc(arr, brr), k + calc(sorted(arr), sorted(brr)))
        return res
```
