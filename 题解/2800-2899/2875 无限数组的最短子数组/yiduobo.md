---
title: "2875. 无限数组的最短子数组"
aliases: ["yiduobo的每日leetcode 2875.无限数组的最短子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662627706"
zhihu_id: "662627706"
zhihu_title: "yiduobo的每日leetcode 2875.无限数组的最短子数组"
question_id: "2875"
question: "无限数组的最短子数组"
problem_url: "https://leetcode.cn/problems/minimum-size-subarray-in-infinite-array/"
difficulty: "Medium"
rating: 1914
created: "2023-10-21T20:23:52+08:00"
updated: "2023-10-21T20:23:52+08:00"
upvotes: 0
comments: 0
---

# 2875. 无限数组的最短子数组

> **[yiduobo的每日leetcode 2875.无限数组的最短子数组](https://zhuanlan.zhihu.com/p/662627706) · 知乎 · 2023-10-21 · 赞同 0**
> 力扣：[2875. 无限数组的最短子数组](https://leetcode.cn/problems/minimum-size-subarray-in-infinite-array/) · Medium · 灵茶山艾府：[【图解】滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2875.无限数组的最短子数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-size-subarray-in-infinite-array/)

题目要求在一个无限循环的数组里面找出一个最短的子数组，使得这个子数组之和等于target。看上去是一个很明确的滑动窗口的问题，但是本题的数组长度无限，同时target的取值范围很大，因此不能直接使用滑动窗口求解。

可以发现，这个子数组可以拆分成三个部分，分别是左侧的某个nums的后缀，中部的若干个完整的nums，以及右侧的某个nums的前缀，当然，这三个部分的长度都可以为0。

中间部分的值是最容易计算的，直接使用target整除nums的和，就得到了中间nums的重复次数，然后乘以nums的长度就是中间部分的长度。而对于左右两个部分，则可以认为是在nums重复一次的数组中寻找一个最短子数组，使得这个子数组之和等于target模nums的和的结果，这样一来就可以在长度为两倍nums长度的数组中使用滑动窗口求解。

具体实现上，使用一个变量now记录当前窗口内的元素和，同时使用两个变量left和right来维护窗口的左右边界。

当now小于取模后的target，那么就不断向右移动right并将对应的元素累加到now中，直到now大于等于取模后的target或者right来到数组边界。若最终right来到了数组边界，说明当前窗口内的元素和不足，可以直接跳出循环。接下来若now大于取模后的target，那么就不断将left向右移动并将被移出窗口的元素从now中减去，直到now小于等于取模后的target。若此时now等于取模后的target，就是用当前窗口大小来更新答案。

另外在返回结果时不要忘了最开始计算的中间部分的长度。

最后附上python代码：

```python
class Solution(object):
    def minSizeSubarray(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        s = sum(nums)
        n = len(nums)
        res = target / s * n
        target %= s
        if target == 0:
            return res
        
        left = 0
        right = 0
        now = 0
        need_fill = None
        while right < n + n:
            while right < n + n and now < target:
                now += nums[right % n]
                right += 1

            if now < target:
                break
            
            while now > target:
                now -= nums[left % n]
                left += 1
            
            if now == target:
                if need_fill is None or need_fill > right - left:
                    need_fill = right - left
                now -= nums[left % n]
                left += 1
        
        if need_fill is None:
            return -1
        
        return need_fill + res
```
