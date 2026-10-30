---
title: "152. 乘积最大子数组"
aliases: ["yiduobo的每日leetcode 152.乘积最大子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/LeetCode-热题-100", "题单/动态规划/一-入门-DP", "题单/动态规划/七-其他线性-DP", "题单/LeetCode-热题-100/动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143254780"
zhihu_id: "143254780"
zhihu_title: "yiduobo的每日leetcode 152.乘积最大子数组"
question_id: "152"
question: "乘积最大子数组"
problem_url: "https://leetcode.cn/problems/maximum-product-subarray/"
difficulty: "Medium"
created: "2020-05-24T19:53:30+08:00"
updated: "2020-05-24T19:53:30+08:00"
upvotes: 0
comments: 0
---

# 152. 乘积最大子数组

> **[yiduobo的每日leetcode 152.乘积最大子数组](https://zhuanlan.zhihu.com/p/143254780) · 知乎 · 2020-05-24 · 赞同 0**
> 力扣：[152. 乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/) · Medium · 灵茶山艾府：[动态规划，简洁高效！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

152.乘积最大子数组<https://leetcode-cn.com/problems/maximum-product-subarray/>

拿到题目的第一想法是直接参考最大子段和，设f[i]表示以nums[i]为结尾的最大乘积，但是在这里存在一些问题，因为会有负负得正的情况存在。举个简单的例子，

nums为[-2, 3, -4]，那么对应的f[0] \= -2, f[1] \= 3，但是此时f[2]理论上应该是24，但是已经无法从之前的状态中得到了。

于是我们可以再维护一个数组g，其中g[i]表示以nums[i]为结尾的最小乘积。

那么当nums[i]小于零时，就用g[i - 1]来更新f[i]，使用f[i - 1]来更新g[i]。否则还是老样子用f[i - 1]更新f[i]，用g[i - 1]更新g[i]即可。

由于f和g只与上一轮的状态有关，因此不需要维护整个数组，只需要用两个变量滚动起来。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0
        
        res = max_res = min_now = max_now = nums[0]
        for num in nums[1:]:
            if num >= 0:
                max_now, min_now = max(max_now * num, num), min(min_now * num, num)
            else:
                max_now, min_now = max(min_now * num, num), min(max_now * num, num)

            res = max(res, max_now)

        return res
```
