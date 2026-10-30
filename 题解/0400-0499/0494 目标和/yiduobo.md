---
title: "494. 目标和"
aliases: ["yiduobo的每日leetcode 494.目标和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/256368578"
zhihu_id: "256368578"
zhihu_title: "yiduobo的每日leetcode 494.目标和"
question_id: "494"
question: "目标和"
problem_url: "https://leetcode.cn/problems/target-sum/"
difficulty: "Medium"
created: "2020-09-20T18:26:54+08:00"
updated: "2020-09-20T18:26:54+08:00"
upvotes: 0
comments: 0
---

# 494. 目标和

> **[yiduobo的每日leetcode 494.目标和](https://zhuanlan.zhihu.com/p/256368578) · 知乎 · 2020-09-20 · 赞同 0**
> 力扣：[494. 目标和](https://leetcode.cn/problems/target-sum/) · Medium · 灵茶山艾府：[两种方法：0-1 背包 / 折半枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

494.目标和<https://leetcode-cn.com/problems/target-sum/>

注意到题目描述是只能在每个数字前面加上加号或者减号，那么实际上可以将每个数字看成独立的个体，于是题目就与背包问题很类似了，可以使用动态规划来解决。

令f\[i\]\[j\]表示前i个数能得到j的情况总数，那么对于f\[i\]\[j\]，当前这次操作要么是加上nums\[i\]，要么是减去nums\[i\]，于是就有f\[i\]\[j\] \= f\[i - 1\]\[j - nums\[i\]\] + f\[i - 1\]\[j + nums\[i\]\]。

虽然这里每一轮的转移只与上一轮有关，但是j的数值大小是杂乱的，因此只能使用01式滚动。另外，需要注意在初始化f[0]时需要判断nums[0] \= 0的情况。

为了方便判断边界，我实现的时候没有用二维数组，而是用一位数组套一维dict，最后附上python代码：

```python
class Solution(object):
    def findTargetSumWays(self, nums, S):
        """
        :type nums: List[int]
        :type S: int
        :rtype: int
        """

        sum_nums = sum(nums)

        f = []
        f.append({})
        if nums[0] == 0:
            f[0][0] = 2
        else:
            f[0][nums[0]] = 1
            f[0][-nums[0]] = 1

        for i in range(1, len(nums)):
            f.append({})
            for j in range(-sum_nums, sum_nums + 1):
                f[i][j] = f[i - 1].get(j - nums[i], 0) + f[i - 1].get(j + nums[i], 0)

        return f[len(nums) - 1].get(S, 0)
```
