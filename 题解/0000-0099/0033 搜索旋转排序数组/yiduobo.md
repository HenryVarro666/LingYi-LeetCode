---
title: "33. 搜算旋转排序数组"
aliases: ["yiduobo的每日leetcode 33.搜算旋转排序数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/四-其他", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/120368744"
zhihu_id: "120368744"
zhihu_title: "yiduobo的每日leetcode 33.搜算旋转排序数组"
question_id: "33"
question: "搜索旋转排序数组"
problem_url: "https://leetcode.cn/problems/search-in-rotated-sorted-array/"
difficulty: "Medium"
created: "2020-03-29T20:56:31+08:00"
updated: "2020-03-29T20:56:31+08:00"
upvotes: 0
comments: 0
---

# 33. 搜算旋转排序数组

> **[yiduobo的每日leetcode 33.搜算旋转排序数组](https://zhuanlan.zhihu.com/p/120368744) · 知乎 · 2020-03-29 · 赞同 0**
> 力扣：[33. 搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/) · Medium · 灵茶山艾府：[两种方法：两次二分 / 一次二分（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

33.搜索旋转排序数组<https://leetcode-cn.com/problems/search-in-rotated-sorted-array/>

二分查找的题目。根据题干，数组中可能存在一个分界点，满足

(1) a[left] \< a[left + 1] \< ... \< a[k]，a[k + 1] \< a[k + 2] \< ... a[right]且a[left] > a[right]

或者是满足：

(2) a[left] \< a[left + 1] \< ... \< a[k] \< a[k + 1] \< ... \< a[right]

不妨设mid \= (left + right) / 2，那么无论哪种情况，对于a[mid]：

如果满足a[mid] \=\= target，那么就是要找的答案了。

如果满足a[mid] > a[left]，如果是情况(1)，那么a[mid]一定处于a[left]到a[k]之间，所以a[left]到a[mid]是升序的，于是可以判断target是否处于a[left]到a[mid]中，从而进行二分。

如果满足不满足a[mid] > a[left]，那么就反过来判断target是否处于a[mid]到a[right]之间，从而进行二分。

每次缩小一半的规模，所以最后的时间复杂度为O(logn)

最后附上python代码：

```python
class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (right - left) / 2 + left
            if nums[mid] == target:
                return mid
            
            if nums[left] <= nums[mid]:
                if target >= nums[left] and target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            elif target > nums[mid] and target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

        return -1
```
