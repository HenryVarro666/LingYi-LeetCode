---
title: "153. 寻找旋转排序数组中的最小值"
aliases: ["yiduobo的每日leetcode 153.寻找旋转排序数组中的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/四-其他", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143530435"
zhihu_id: "143530435"
zhihu_title: "yiduobo的每日leetcode 153.寻找旋转排序数组中的最小值"
question_id: "153"
question: "寻找旋转排序数组中的最小值"
problem_url: "https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/"
difficulty: "Medium"
created: "2020-05-25T21:16:41+08:00"
updated: "2020-05-25T21:18:06+08:00"
upvotes: 0
comments: 0
---

# 153. 寻找旋转排序数组中的最小值

> **[yiduobo的每日leetcode 153.寻找旋转排序数组中的最小值](https://zhuanlan.zhihu.com/p/143530435) · 知乎 · 2020-05-25 · 赞同 0**
> 力扣：[153. 寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) · Medium · 灵茶山艾府：[和最后一个数比大小，简洁二分（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

153.寻找旋转排序数组中的最小值<https://leetcode-cn.com/problems/find-minimum-in-rotated-sorted-array/>

二分查找的题目。还是考虑nums[mid]，若nums[mid]大于nums[right]，那么说明mid + 1到right之间有一段是数组中最小的那个部分被旋转过来了，答案就在其中，因此有left \= mid + 1。若nums[mid]小于nums[right]，那么说明mid到right这一段都还是保持着升序，那么nums[mid + 1]到nums[right]这些数都大于nums[mid]，因此答案不会在mid + 1到right之间，于是有right \= mid。

最后附上python代码：

```python
class Solution(object):
    def findMin(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (left + right) / 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
```
