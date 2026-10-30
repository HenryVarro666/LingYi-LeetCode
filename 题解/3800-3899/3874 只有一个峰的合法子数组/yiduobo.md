---
title: "3874. 只有一个峰的合法子数组"
aliases: ["yiduobo的每日leetcode 3874.只有一个峰的合法子数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019541242728443911"
zhihu_id: "2019541242728443911"
zhihu_title: "yiduobo的每日leetcode 3874.只有一个峰的合法子数组"
question_id: "3874"
question: "只有一个峰的合法子数组"
problem_url: "https://leetcode.cn/problems/valid-subarrays-with-exactly-one-peak/"
created: "2026-03-23T22:48:40+08:00"
updated: "2026-03-23T22:48:59+08:00"
upvotes: 1
comments: 0
---

# 3874. 只有一个峰的合法子数组

> **[yiduobo的每日leetcode 3874.只有一个峰的合法子数组](https://zhuanlan.zhihu.com/p/2019541242728443911) · 知乎 · 2026-03-23 · 赞同 1**
> 力扣：[3874. 只有一个峰的合法子数组](https://leetcode.cn/problems/valid-subarrays-with-exactly-one-peak/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3874.只有一个峰的合法子数组

<https://leetcode.cn/problems/valid-subarrays-with-exactly-one-peak/>

题目给出一个长度为n的整数数组nums，以及一个整数k。

对于一个1到n - 2之间的下标index，若nums[index]大于其两侧相邻的元素，即nums[index]满足nums[index] > nums[index - 1]，且nums[index] > nums[index + 1]，那么就称index为一个峰。

对于一个从l到r的子数组，若其中恰好包含一个峰，且这个峰的下标index满足index - l \<\= k，同时r - index \<\= k，那么就称这个子数组是合法的。

问nums中一共有多少个合法子数组。

由于题目中的合法子数组中只能恰好包含一个峰，同时峰的判断也很简单，那么不妨先对nums进行一趟遍历，找出哪些下标是峰，记为数组peak。

接下来，对于peak中的某个峰peak[index]，包含peak[index]的合法子数组左边界left_bound最多延伸到peak[index - 1] + 1，同时还需要满足peak[index] - left_bound \<\= k。也就是说left_bound最小只能取到min(peak[index - 1] + 1, peak[index] - k)。更进一步的，左边界的取值范围在left_bound到peak[index]之间，因此一共有peak[index] - min(peak[index - 1] + 1, peak[index - k]) + 1种合法的取值，化简之后就是min(peak[index] - peak[index - 1], k + 1)。

同样的，对于其右边界right_bound，则最多延伸到peak[index + 1] - 1，同时还需要满足right_bound - peak[index] \<\= k，因此右边界一共有min(peak[index + 1] - peak[index], k + 1)种合法的取值。

接下来，将左右边界合法取值的方案数相乘，即为包含peak[index]的合法子数组数量，依照这个方式遍历所有的峰并计算答案即可。

需要注意第一个峰没有左侧峰的限制，因此可以将前一个峰的下标设置为-1，而最后一个峰没有右侧峰的限制，可以将后一个峰的下标设置为n。

最后附上python代码：

```python
class Solution(object):
    def validSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        peak = []
        for index in range(1, len(nums) - 1):
            if nums[index] > nums[index - 1] and nums[index] > nums[index + 1]:
                peak.append(index)

        res = 0
        for index in range(len(peak)):
            if index == 0:
                pre = -1
            else:
                pre = peak[index - 1]
            
            left = min(peak[index] - pre, k + 1)
        
            if index == len(peak) - 1:
                nxt = len(nums)
            else:
                nxt = peak[index + 1]
            
            right = min(nxt - peak[index], k + 1)

            res += left * right
        
        return res
```
