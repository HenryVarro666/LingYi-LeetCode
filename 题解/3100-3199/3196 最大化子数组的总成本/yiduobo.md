---
title: "3196. 最大化子数组的总成本"
aliases: ["yiduobo的每日leetcode 3196.最大化子数组的总成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707113239"
zhihu_id: "707113239"
zhihu_title: "yiduobo的每日leetcode 3196.最大化子数组的总成本"
question_id: "3196"
question: "最大化子数组的总成本"
problem_url: "https://leetcode.cn/problems/maximize-total-cost-of-alternating-subarrays/"
difficulty: "Medium"
rating: 1847
created: "2024-07-05T00:11:27+08:00"
updated: "2024-07-05T00:11:27+08:00"
upvotes: 0
comments: 0
---

# 3196. 最大化子数组的总成本

> **[yiduobo的每日leetcode 3196.最大化子数组的总成本](https://zhuanlan.zhihu.com/p/707113239) · 知乎 · 2024-07-05 · 赞同 0**
> 力扣：[3196. 最大化子数组的总成本](https://leetcode.cn/problems/maximize-total-cost-of-alternating-subarrays/) · Medium · 灵茶山艾府：[两种思考方式：划分型 DP / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3196.最大化子数组的总成本

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-total-cost-of-alternating-subarrays/description/)

题目给出一个整数数组nums，要求将其划分为若干个子数组。对于每个子数组nums[l : r + 1]，其成本cost[l][r] \= nums[l] - nums[l + 1] + nums[l + 2] - ... + nums[r] \* (-1)^(r - l)，问可以得到的最大总成本是多少。

经典的动态规划问题，令f[i]表示前i个数进行划分，且最后一项是加号时的最大总成本，g[i]则表示前i个数进行划分，且最后一项是减号时的最大总成本，那么对于f[i]，可以将nums[i]接在f[i - 1]后面，表示另起一个子数组，也可以将nums[i]接在g[i - 1]后面，表示将nums[i]加入到g[i - 1]的最后一个子数组中，于是有f[i] \= max(f[i - 1], g[i - 1]) + nums[i]；而对于g[i]，则只能将-nums[i]接在f[i - 1]后面，于是有g[i] \= f[i - 1] - nums[i]。

注意到f和g每一轮都只和上一轮有关，因此可以直接使用变量迭代来节省空间。

最后附上python代码：

```python
class Solution(object):
    def maximumTotalCost(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        f, g = nums[0], None
        for v in nums[1:]:
            new_f = f + v
            if g is not None:
                new_f = max(new_f, g + v)
            
            g = f - v
            f = new_f
        
        return max(f, g)
```
