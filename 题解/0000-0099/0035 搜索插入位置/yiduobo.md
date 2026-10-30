---
title: "35. 搜索插入位置"
aliases: ["yiduobo的每日leetcode 35.搜索插入位置"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "leetcode/api", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/一-二分查找", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/121088144"
zhihu_id: "121088144"
zhihu_title: "yiduobo的每日leetcode 35.搜索插入位置"
question_id: "35"
question: "搜索插入位置"
problem_url: "https://leetcode.cn/problems/search-insert-position/"
difficulty: "Easy"
created: "2020-03-30T22:42:54+08:00"
updated: "2020-03-30T22:42:54+08:00"
upvotes: 0
comments: 0
---

# 35. 搜索插入位置

> **[yiduobo的每日leetcode 35.搜索插入位置](https://zhuanlan.zhihu.com/p/121088144) · 知乎 · 2020-03-30 · 赞同 0**
> 力扣：[35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/) · Easy · 灵茶山艾府：[二分查找总是写不对？一个视频讲透！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

35.搜索插入位置<https://leetcode-cn.com/problems/search-insert-position/>

又是二分的题目。题目需要我们找到nums中下标最小，且大于等于target的数。

首先考察特殊情况，即target比数组中最后一个数还大，那么就直接返回len(nums)，否则开始进行二分。对于nums[mid]：

如果nums[mid] \=\= target，那么直接返回mid。

如果nums[mid] \< target，那么说明答案位于mid + 1到right之间，此时left \= mid + 1。

如果nums[mid] > target，那么说明答案位于left到mid之间。需要注意这里mid还是有可能成为答案的，因此此时right \= mid而不是mid - 1。

时间复杂度为O(logn)。

最后附上python代码：

```python
class Solution(object):
    def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        if not nums:
            return 0
        if target > nums[-1]:
            return len(nums)

        left = 0
        right = len(nums) - 1
        while left <= right:
            if left == right:
                return left
            else:
                mid = (right + left) / 2
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid
```
