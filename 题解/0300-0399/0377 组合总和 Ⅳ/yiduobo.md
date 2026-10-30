---
title: "377. 组合总和IV"
aliases: ["yiduobo的每日leetcode 377.组合总和IV"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166039500"
zhihu_id: "166039500"
zhihu_title: "yiduobo的每日leetcode 377.组合总和IV"
question_id: "377"
question: "组合总和 Ⅳ"
problem_url: "https://leetcode.cn/problems/combination-sum-iv/"
difficulty: "Medium"
rating: 1600
created: "2020-08-02T00:19:19+08:00"
updated: "2020-08-02T00:19:19+08:00"
upvotes: 0
comments: 0
---

# 377. 组合总和IV

> **[yiduobo的每日leetcode 377.组合总和IV](https://zhuanlan.zhihu.com/p/166039500) · 知乎 · 2020-08-02 · 赞同 0**
> 力扣：[377. 组合总和 Ⅳ](https://leetcode.cn/problems/combination-sum-iv/) · Medium · 灵茶山艾府：[本质是爬楼梯：记忆化搜索 / 递推（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

377.组合总和IV <https://leetcode-cn.com/problems/combination-sum-iv/>

经典的动态规划问题。设f[i]表示组合达成i有多少种可能性，那么对于i，若i大于等于nums中的任意数nums[j]，那么就可以通过i - nums[j]再加上nums[j]达成i，于是有

f[i] \= sum(f[i - nums[j])

其中，边界条件为f[0] \= 1，表示达成0只有什么数都不选这一种情况。

另外，对于题目中提到的负数的情况，如果nums仅存在正数或者仅存在负数，那么与原题一样。而对于nums中同时存在正数a以及负数b的情况，一定有

a \* (-b) + b \* a \= 0

表示选择-b个a与a个b进行组合能得到0。更一般地，有

a \* (-kb) + b \* ka \= 0

其中k为任意整数，表示选择-kb个a与ka个b进行组合可以得到0。这意味着有无数种可能达成0，因此对于能通过nums组合出来的任意数，都存在无数种组合方式。

最后附上python代码：

```python
class Solution(object):
    def combinationSum4(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        f = [0] * (target + 1)
        f[0] = 1
        for i in range(1, target + 1):
            for num in nums:
                if i >= num:
                    f[i] += f[i - num]

        return f[target]
```
