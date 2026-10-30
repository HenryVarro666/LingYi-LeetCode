---
title: "34. 在排序数组中查找元素的第一个和最后一个位置"
aliases: ["yiduobo的每日leetcode 34.在排序数组中查找元素的第一个和最后一个位置"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/一-二分查找", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/120380007"
zhihu_id: "120380007"
zhihu_title: "yiduobo的每日leetcode 34.在排序数组中查找元素的第一个和最后一个位置"
question_id: "34"
question: "在排序数组中查找元素的第一个和最后一个位置"
problem_url: "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/"
difficulty: "Medium"
created: "2020-03-29T21:22:36+08:00"
updated: "2020-03-29T21:22:36+08:00"
upvotes: 0
comments: 0
---

# 34. 在排序数组中查找元素的第一个和最后一个位置

> **[yiduobo的每日leetcode 34.在排序数组中查找元素的第一个和最后一个位置](https://zhuanlan.zhihu.com/p/120380007) · 知乎 · 2020-03-29 · 赞同 0**
> 力扣：[34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) · Medium · 灵茶山艾府：[【视频讲解】二分查找总是写不对？三种写法，一个视频讲透！（Python/Java/C++/C/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

34.在排序数组中查找元素的第一个和最后一个位置<https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array/>

妈妈说标题要长才能引人注目。

还是二分查找的题目，需要关注在二分的过程中left与right的变化。

依然是mid \= (left + right) / 2，那么对于a[mid]与target的关系：

(1) target \< a[mid]，依然是普通的 right \= mid - 1

(2) target > a[mid]，依然是普通的 left \= mid + 1

(3) target \= a[mid]：

如果找的是左边界，那么当前mid为可行的左边界，但是在a[left]到a[mid - 1]之间也可能出现target，因此应该继续检索左半边，即 right \= mid - 1。

同理，如果找的是右边界，那么当前mid为可行的右边界，同时继续检索右半边，即 left \= mid + 1。

通过两次二分查找分别找到左边界与右边界，最后的时间复杂度为O(logn)

最后附上python代码：

```python
class Solution(object):
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        if not nums:
            return [-1, -1]

        left = 0 
        right = len(nums) - 1
        left_pos = -1
        while left <= right:
            if left == right:
                if nums[left] == target:
                    left_pos = left
                break
            else:
                mid = (left + right) / 2
                if nums[mid] == target:
                    left_pos = mid
                    right = mid - 1
                elif nums[mid] > target:
                    right = mid - 1
                else:
                    left = mid + 1

        left = 0
        right = len(nums) - 1
        right_pos = -1
        while left <= right:
            if left == right:
                if nums[right] == target:
                    right_pos = right
                break
            else:
                mid = (left + right) / 2
                if nums[mid] == target:
                    right_pos = mid
                    left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return [left_pos, right_pos]
```
