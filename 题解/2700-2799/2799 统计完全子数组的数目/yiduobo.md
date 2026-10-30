---
title: "2799. 统计完全子数组的数目"
aliases: ["yiduobo的每日leetcode 2799.统计完全子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657277627"
zhihu_id: "657277627"
zhihu_title: "yiduobo的每日leetcode 2799.统计完全子数组的数目"
question_id: "2799"
question: "统计完全子数组的数目"
problem_url: "https://leetcode.cn/problems/count-complete-subarrays-in-an-array/"
difficulty: "Medium"
created: "2023-09-20T04:53:02+08:00"
updated: "2023-09-20T04:53:02+08:00"
upvotes: 0
comments: 0
---

# 2799. 统计完全子数组的数目

> **[yiduobo的每日leetcode 2799.统计完全子数组的数目](https://zhuanlan.zhihu.com/p/657277627) · 知乎 · 2023-09-20 · 赞同 0**
> 力扣：[2799. 统计完全子数组的数目](https://leetcode.cn/problems/count-complete-subarrays-in-an-array/) · Medium · 灵茶山艾府：[「越长越合法」型滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2799.统计完全子数组的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-complete-subarrays-in-an-array/)

首先可以通过集合来计算出数组中不同数字的数量k，那么问题就变成了数组中有多少个数组中存在k个不同的数字。这是一个经典的变长滑动窗口问题，使用一个哈希表统计窗口内每种数字出现的次数然后套用滑动窗口的那一套就行了。

当窗口的左边界left向右移动时，其对应的最小右边界right必然大于等于之前轮次的最小右边界，这样一来就可以在均摊O(1)的时间内找出所有当前left对应的right。得到right后，就可以利用数组长度n与right计算出以left为左边界的完全子数组的数目，然后继续向右移动left，直达left来到数组末尾或者找不到合法的right为止。

最后附上python代码：

```python
class Solution(object):
    def countCompleteSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        distinct = len(set(nums))
        cnt = {}
        left = 0
        right = 0
        res = 0
        while left < len(nums):
            while right < len(nums) and len(cnt) < distinct:
                cnt[nums[right]] = cnt.get(nums[right], 0) + 1
                right += 1

            if len(cnt) < distinct:
                break

            res += len(nums) - right + 1
            cnt[nums[left]] -= 1
            if cnt[nums[left]] == 0:
                cnt.pop(nums[left])
            left += 1
        
        return res
```
