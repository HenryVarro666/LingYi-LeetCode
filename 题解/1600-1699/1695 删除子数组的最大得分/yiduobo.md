---
title: "1695. 删除子数组的最大得分"
aliases: ["yiduobo的每日leetcode 1695.删除子数组的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/447233396"
zhihu_id: "447233396"
zhihu_title: "yiduobo的每日leetcode 1695.删除子数组的最大得分"
question_id: "1695"
question: "删除子数组的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-erasure-value/"
difficulty: "Medium"
rating: 1529
created: "2021-12-19T12:25:10+08:00"
updated: "2021-12-19T12:25:10+08:00"
upvotes: 0
comments: 0
---

# 1695. 删除子数组的最大得分

> **[yiduobo的每日leetcode 1695.删除子数组的最大得分](https://zhuanlan.zhihu.com/p/447233396) · 知乎 · 2021-12-19 · 赞同 0**
> 力扣：[1695. 删除子数组的最大得分](https://leetcode.cn/problems/maximum-erasure-value/) · Medium · 灵茶山艾府：[滑动窗口 + 数组 / 哈希集合（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1695.删除子数组的最大得分

[力扣](https://leetcode-cn.com/problems/maximum-erasure-value/)

经典的滑动窗口问题。从左向右枚举窗口的右边界r，那么随着右边界向右移动，左边界l必然也跟着向右移动。

对于当前的r' \= r + 1来说，需要在区间l到r之间新加入一个nums[r']，那么就需要判断nums[r']是否已经在l到r之间出现过。在这里可以使用一个dict记录下每个数字上一次出现的位置。

设nums[r']上一次出现的位置为p，若p >\= l，说明l到r之间已经有了nums[r']，此时就需要移动左边界l到p + 1的位置，否则l可以保持不变。

确定了r'对应的l'之后，此时就需要用l'到r'这个区间的和来更新答案。区间和问题当然是转化成前缀和来做了。

最后附上python代码：

```python
class Solution(object):
    def maximumUniqueSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last_pos = {}
        s = [nums[0]]
        l = 0
        r = 1
        now = 0
        res = nums[0]
        last_pos[nums[0]] = 0
        while r < len(nums):
            s.append(s[-1] + nums[r])
            pos = last_pos.get(nums[r], -1)
            if pos >= l:
                l = pos + 1
            
            if l > 0:
                res = max(res, s[-1] - s[l - 1])
            else:
                res = max(res, s[-1])
            last_pos[nums[r]] = r
            r += 1
        
        return res
```
