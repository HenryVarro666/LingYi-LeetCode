---
title: "213. 打家劫舍II"
aliases: ["yiduobo的每日leetcode 213.打家劫舍II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147954363"
zhihu_id: "147954363"
zhihu_title: "yiduobo的每日leetcode 213.打家劫舍II"
question_id: "213"
question: "打家劫舍 II"
problem_url: "https://leetcode.cn/problems/house-robber-ii/"
difficulty: "Medium"
created: "2020-06-12T21:49:01+08:00"
updated: "2020-06-12T21:49:01+08:00"
upvotes: 0
comments: 0
---

# 213. 打家劫舍II

> **[yiduobo的每日leetcode 213.打家劫舍II](https://zhuanlan.zhihu.com/p/147954363) · 知乎 · 2020-06-12 · 赞同 0**
> 力扣：[213. 打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/) · Medium · 灵茶山艾府：[简洁写法，直接调用 198 题代码（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

213.打家劫舍II<https://leetcode-cn.com/problems/house-robber-ii/>

198题打家劫舍的升级版（传送门在这里[yiduobo：yiduobo的每日leetcode 198.打家劫舍](https://zhuanlan.zhihu.com/p/145933856)），做法基本相同。

相比198题，这里所有的房屋排成环状，那么第一家与最后一家就不能同时选取，于是可以选择放弃第一家，计算第二家到最后一家的最大收益，然后选择放弃最后一家，计算第一家到倒数第二家的最大收益，最后取其中较大的值作为答案即可。实际上就是198题的做法在1到n - 1以及2到n上分别跑一次然后取较大值。

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

        if len(nums) <= 2:
            return max(nums)

        last_two = last_one = 0
        for num in nums[:-1]:
            last_one, last_two = max(last_two + num, last_one), last_one

        res = last_one

        last_two = last_one = 0
        for num in nums[1:]:
            last_one, last_two = max(last_two + num, last_one), last_one

        return max(res, last_one)
```
