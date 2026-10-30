---
title: "53. 最大子序和"
aliases: ["yiduobo的每日leetcode 53.最大子序和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/一-前缀和", "题单/动态规划/一-入门-DP", "题单/动态规划/七-其他线性-DP", "题单/LeetCode-热题-100/普通数组", "题单/面试经典-150-题/Kadane-算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/126746511"
zhihu_id: "126746511"
zhihu_title: "yiduobo的每日leetcode 53.最大子序和"
question_id: "53"
question: "最大子数组和"
problem_url: "https://leetcode.cn/problems/maximum-subarray/"
difficulty: "Medium"
created: "2020-04-07T22:51:09+08:00"
updated: "2020-04-07T22:51:09+08:00"
upvotes: 0
comments: 0
---

# 53. 最大子序和

> **[yiduobo的每日leetcode 53.最大子序和](https://zhuanlan.zhihu.com/p/126746511) · 知乎 · 2020-04-07 · 赞同 0**
> 力扣：[53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/) · Medium · 灵茶山艾府：[两种方法：前缀和+贪心 / 动态规划，附变形题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

53.最大子序和<https://leetcode-cn.com/problems/maximum-subarray/>

经典的动态规划问题。至于题目中所说的更为精妙的分治法，时间复杂度为O(nlogn)，相比O(n)的贪心法，感觉并不见得哪里精妙了。。。

不妨设f[i]代表以nums[i]结束的最大的子序和，那么：

若f[i - 1] + nums[i]小于0，那么说明前面这个子序列还不如不要，直接从0开始，即f[i] \= 0

否则有f[i] \= f[i - 1] + nums[i]

然后取最大的f[i]作为答案即可。

需要注意如果nums全是负数，那么答案就是其中最大的那个数。另外由于f中每个位置就计算了一次然后在计算下一位时被使用了一次，因此不需要维护整个数组，只需要维护当前的子序和即可。

最后附上python代码：

```python
class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if max(nums) < 0:
            return max(nums)

        res = 0
        now = 0
        for index, num in enumerate(nums):
            if now + num < 0:
                now = 0
            else:
                now += num
                res = max(res, now)

        return res
```
