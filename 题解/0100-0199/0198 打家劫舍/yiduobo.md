---
title: "198. 打家劫舍"
aliases: ["yiduobo的每日leetcode 198.打家劫舍"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/一-入门-DP", "题单/动态规划/六-状态机-DP", "题单/LeetCode-热题-100/动态规划", "题单/面试经典-150-题/一维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145933856"
zhihu_id: "145933856"
zhihu_title: "yiduobo的每日leetcode 198.打家劫舍"
question_id: "198"
question: "打家劫舍"
problem_url: "https://leetcode.cn/problems/house-robber/"
difficulty: "Medium"
created: "2020-06-04T21:36:54+08:00"
updated: "2020-06-04T21:36:54+08:00"
upvotes: 0
comments: 0
---

# 198. 打家劫舍

> **[yiduobo的每日leetcode 198.打家劫舍](https://zhuanlan.zhihu.com/p/145933856) · 知乎 · 2020-06-04 · 赞同 0**
> 力扣：[198. 打家劫舍](https://leetcode.cn/problems/house-robber/) · Medium · 灵茶山艾府：[【视频讲解】动态规划入门：从记忆化搜索到递推（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

198.打家劫舍<https://leetcode-cn.com/problems/house-robber/>

动态规划的题目，f[i]表示前i家能偷到的最大金额。那么对于第i家：

1、如果要偷第i家，那么就不能偷第i - 1家，于是f[i]可以从f[i - 2] + nums[i]过来

2、如果不偷第i家，那么f[i]就是从前i - 1家偷的最大金额

于是就有f[i] \= max(f[i - 2] + nums[i]，f[i - 1])

边界条件f[0] \= nums[0]，f[1] \= max(nums[0], nums[1])

由于这里状态转移只与前两个数有关，于是可以滚动起来。需要注意的是滚动时要么需要记录其中一个状态，要么使用python同时赋值的写法。

最后附上python代码：

```python
class Solution(object):
    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        last_two = last_one = 0
        for num in nums:
            last_one, last_two = max(last_two + num, last_one), last_one

        return last_one
```
