---
title: "2735. 收集巧克力"
aliases: ["yiduobo的每日leetcode 2735.收集巧克力"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652703620"
zhihu_id: "652703620"
zhihu_title: "yiduobo的每日leetcode 2735.收集巧克力"
question_id: "2735"
question: "收集巧克力"
problem_url: "https://leetcode.cn/problems/collecting-chocolates/"
difficulty: "Medium"
created: "2023-08-28T01:09:06+08:00"
updated: "2023-08-28T01:09:06+08:00"
upvotes: 1
comments: 0
---

# 2735. 收集巧克力

> **[yiduobo的每日leetcode 2735.收集巧克力](https://zhuanlan.zhihu.com/p/652703620) · 知乎 · 2023-08-28 · 赞同 1**
> 力扣：[2735. 收集巧克力](https://leetcode.cn/problems/collecting-chocolates/) · Medium · 灵茶山艾府：[巧妙枚举（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2735.收集巧克力

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/collecting-chocolates/)

首先，类型替换的次数必然小于数组长度n，因为替换n次相当于没有进行任何操作。

接下来，对于下标为index的巧克力，在替换rnd轮之后其将变为下标为(index + rnd) % n的巧克力。需要注意的是，并不一定需要购买这个下标的巧克力，而是可以从下标index到下标(index + rnd) % n的巧克力中选择价格最便宜的购买，也就是说，这相当于一个前缀最小值问题，不过是对于每个巧克力都维护一个前缀最小值。更具体的，令f[i][j]表示在进行了i次交换后，下标为j的巧克力可以取到的最便宜价格，那么就有f[i][j] \= min(f[i - 1][j], nums[(i + j) % n])，而在第i轮交换后，所需的最小花费就是i \* x + sum(f[i])。

于是可以初始化最小花费为sum(nums)，接下来从1到n - 1遍历替换的轮次rnd，并计算每个巧克力在替换rnd轮之后可以得到的最小价格，然后用rnd \* x + sum(f[rnd])来更新最终答案。

另外，注意到f每一轮的值只与上一轮有关，因此可以利用滚动数组省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """

        n = len(nums)
        f = nums[:]
        res = sum(nums)
        for rnd in range(1, n):
            g = f[:]
            f = []
            for index in range(n):
                f.append(min(nums[(index + rnd) % n], g[index]))
        
            res = min(res, rnd * x + sum(f))
        
        return res
```
