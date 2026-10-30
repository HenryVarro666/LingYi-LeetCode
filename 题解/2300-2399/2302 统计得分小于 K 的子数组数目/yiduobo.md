---
title: "2302. 统计得分小于K的子数组数目"
aliases: ["yiduobo的每日leetcode 2302.统计得分小于K的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554570086"
zhihu_id: "554570086"
zhihu_title: "yiduobo的每日leetcode 2302.统计得分小于K的子数组数目"
question_id: "2302"
question: "统计得分小于 K 的子数组数目"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-score-less-than-k/"
difficulty: "Hard"
rating: 1808
created: "2022-08-16T23:56:25+08:00"
updated: "2022-08-16T23:56:25+08:00"
upvotes: 0
comments: 0
---

# 2302. 统计得分小于K的子数组数目

> **[yiduobo的每日leetcode 2302.统计得分小于K的子数组数目](https://zhuanlan.zhihu.com/p/554570086) · 知乎 · 2022-08-16 · 赞同 0**
> 力扣：[2302. 统计得分小于 K 的子数组数目](https://leetcode.cn/problems/count-subarrays-with-score-less-than-k/) · Hard · 灵茶山艾府：[「越短越合法」型滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2302.统计得分小于K的子数组数目

[力扣](https://leetcode.cn/problems/count-subarrays-with-score-less-than-k/)

题目中子数组得分的计算方式为子数组之和乘上子数组的长度，在知道了子数组的起点和终点后，利用前缀和就可以高效地求出子数组的得分。

由于题目保证了数组中所有的数都是正数，那么对于一个确定了起点的子数组而言，如果这个子数组的终点越靠后，那么最终的得分就越大。因此在这里的第一种做法就是一趟遍历，枚举子数组的起点left，然后二分计算出满足子数组得分小于K且最靠后的终点right，那么以left为起点的满足条件的子数组就有right - left + 1个，使用这个值更新答案并继续向后枚举即可。这种做法的时间复杂度为O(nlogn)。

既然说到了单调性，那么经典的双指针也是值得尝试的。对于一个确定了起点left的子数组，设其满足条件的最大的终点为right，那么对于起点为left' \= left + 1的子数组而言，其对应的终点right' 必然是大于等于right的，也就是说在这里并不需要二分right'，而是只需要在上一轮的基础上，根据当前的left跟着向后移动即可。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = [nums[0]]
        for num in nums[1:]:
            f.append(f[-1] + num)
        
        p = -1
        while p + 1 < len(nums) and f[p + 1] * (p + 2) < k:
            p += 1

        res = p + 1
        for index in range(1, len(nums)):
            p = max(p, index - 1)
            while p + 1 < len(nums) and (f[p + 1] - f[index - 1]) * (p - index + 2) < k:
                p += 1
            res += p - index + 1
        
        return res
```
