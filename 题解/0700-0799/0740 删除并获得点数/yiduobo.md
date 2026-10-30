---
title: "740. 删除与获得点数"
aliases: ["yiduobo的每日leetcode 740.删除与获得点数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336936958"
zhihu_id: "336936958"
zhihu_title: "yiduobo的每日leetcode 740.删除与获得点数"
question_id: "740"
question: "删除并获得点数"
problem_url: "https://leetcode.cn/problems/delete-and-earn/"
difficulty: "Medium"
created: "2020-12-14T22:49:51+08:00"
updated: "2020-12-14T22:49:51+08:00"
upvotes: 1
comments: 0
---

# 740. 删除与获得点数

> **[yiduobo的每日leetcode 740.删除与获得点数](https://zhuanlan.zhihu.com/p/336936958) · 知乎 · 2020-12-14 · 赞同 1**
> 力扣：[740. 删除并获得点数](https://leetcode.cn/problems/delete-and-earn/) · Medium · 灵茶山艾府：[值域打家劫舍（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

740.删除与获得点数

[力扣](https://leetcode-cn.com/problems/delete-and-earn/)

首先，我们可以统计出每个数字出现的次数，然后将其转化为（数值，权重值）这种形式的数对，那么问题就变成了从中选出一些数对，要求数值不能相邻，且权重之和最大。

对于数值不能相邻，一个很自然的想法就是按数值从小到大进行排序，得到数值数组num以及权重数组value，然后设f[i]为前i个数值对可以选出的最大结果。对于f[i]：

1、若num[i - 1]恰好等于num[i]减一，那么我们此时不能直接在f[i - 1]的基础上选择第i个数对，于是有f[i] \= max(f[i - 1]，f[ii - 2] + value[i])。即不选择第i个数对，直接继承f[i - 1]的值，或者选择第i个数对，那么此时需要从f[i - 2]过来

2、若num[i - 1]不等于num[i]减一，那么此时就可以在f[i - 1]的基础上选择第i个数对，于是有f[i] \= f[i - 1] + value[i]

一趟扫描过后，最终的f[-1]就是答案。

注意到这里的状态转移只涉及到f[i]、f[i - 1]以及f[i - 2]，因此可以使用省去f数组，转而使用三个变量滚动来节省空间。

最后附上python代码：

```python
class Solution(object):
    def deleteAndEarn(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        value_dict = {}
        for num in nums:
            value_dict[num] = value_dict.get(num, 0) + num
        
        res = 0
        res_prev = 0
        last = None
        for num, value in sorted(value_dict.items(), key=lambda d:d[0]):
            if last == num - 1:
                now = res_prev + value
            else:
                now = res + value

            res_prev = res
            res = max(res, now)
            last = num

        return res
```
