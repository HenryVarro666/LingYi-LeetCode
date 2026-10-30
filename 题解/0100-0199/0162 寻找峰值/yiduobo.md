---
title: "162. 寻找峰值"
aliases: ["yiduobo的每日leetcode 162.寻找峰值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/binary-search", "题单/二分算法", "题单/面试经典-150-题", "题单/二分算法/四-其他", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144068745"
zhihu_id: "144068745"
zhihu_title: "yiduobo的每日leetcode 162.寻找峰值"
question_id: "162"
question: "寻找峰值"
problem_url: "https://leetcode.cn/problems/find-peak-element/"
difficulty: "Medium"
created: "2020-05-27T22:21:29+08:00"
updated: "2020-05-27T22:21:29+08:00"
upvotes: 0
comments: 0
---

# 162. 寻找峰值

> **[yiduobo的每日leetcode 162.寻找峰值](https://zhuanlan.zhihu.com/p/144068745) · 知乎 · 2020-05-27 · 赞同 0**
> 力扣：[162. 寻找峰值](https://leetcode.cn/problems/find-peak-element/) · Medium · 灵茶山艾府：[严格证明，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

162.寻找峰值<https://leetcode-cn.com/problems/find-peak-element/>

题目要求在O(logn)的时间内解决问题，因此自然能想到二分。又因为题目保证了nums[i] !\= nums[i +1]，于是我们可以在每轮二分时比较nums[mid]与nums[mid + 1]：

若nums[mid]较大，那么答案位于l到mid之间，那么有r \= mid。

若nums[mid + 1]较大，那么答案位于mid + 1到r之间，那么有l \= mid + 1。

于是逐步缩小范围直到l等于r即可。

最后附上python代码：

```python
class Solution(object):
    def findPeakElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        l = 0
        r = len(nums) - 1
        while l < r:
            mid = (l + r) / 2
            if nums[mid] > nums[mid + 1]:
                r = mid
            else:
                l = mid + 1

        return l
```
