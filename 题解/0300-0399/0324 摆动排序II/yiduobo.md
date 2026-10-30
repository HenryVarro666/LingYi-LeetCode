---
title: "324. 摆动排序II"
aliases: ["yiduobo的每日leetcode 324.摆动排序II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/160210221"
zhihu_id: "160210221"
zhihu_title: "yiduobo的每日leetcode 324.摆动排序II"
question_id: "324"
question: "摆动排序II"
problem_url: "https://leetcode.cn/problems/wiggle-sort-ii/"
created: "2020-07-15T21:40:31+08:00"
updated: "2020-07-15T21:40:31+08:00"
upvotes: 0
comments: 0
---

# 324. 摆动排序II

> **[yiduobo的每日leetcode 324.摆动排序II](https://zhuanlan.zhihu.com/p/160210221) · 知乎 · 2020-07-15 · 赞同 0**
> 力扣：[324. 摆动排序II](https://leetcode.cn/problems/wiggle-sort-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

324.摆动排序II <https://leetcode-cn.com/problems/wiggle-sort-ii/>

这个问题最直观的做法就是排序，然后将排好序的数组从中间截断，按照一左一右的顺序合并起来。需要注意的是，在合并的过程中，原始位置越靠中间的数应该放到更靠边的位置，防止形如1，2，2，3这种情况下两个2相邻的情况。

由于题目只需要满足大小关系，因此实际上并不需要将整个数组排序，而只需要将数组中较小的一半放在前半部分，而较大的一半放在后半部分即可。听起来就是快排的过程，但是这里有一个问题就是如何选择快排分割的基准点。

一个自然的想法就是选取数组的中位数，也就是找到数组中第 (len(nums) + 1)/2 大的数，这一步之前已经做过原题（传送门在这里：[yiduobo：yiduobo的每日leetcode 215.数组中的第K个最大元素](https://zhuanlan.zhihu.com/p/148151993)），只需要将递归改成迭代保证O(1)的空间复杂度即可。

到了这里，我们找到了中位数mid_num。接下来，我们需要将所有小于mid_num的数放在数组的左侧，而大于mid_num的数放在数组右侧。这一步直接照搬快排的做法即可。

最后，我们需要重新合并数组的前半部分与后半部分。我在这里的做法是首先计算出每个数应该放置的位置，那么这些数之间会形成若干个交换的环，于是从左往右一趟遍历，对于未遍历过的环进行逐个交换，并设置好标记。

对于标记的设置，由于不允许使用额外的空间，于是我在这里用了一种取巧的做法，即对于每个交换过后的数加上数组中的最大值max_num再加上1，那么当循环到某个数时，如果其大于max_num，说明其已经被交换过了，因此需要直接跳过这个数。这样做会有负数或者越界的问题，需要进行比较繁琐的判断。考虑到python的特性，因此我是直接将数组中所有的数先将去最小值min_num，这样一来就保证了数组中所有数都非负，接下来直接利用这个max_num + 1的做法进行标记。

最后附上python代码：

```python
class Solution(object):
    def wiggleSort(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        l = 0
        r = len(nums) - 1
        k = (len(nums) + 1) / 2
        while l <= r:
            if l == r:
                mid_num = nums[l]
                break

            mid = nums[(l + r) / 2]
            i = l
            j = r
            while i <= j:
                while i <= r and nums[i] < mid: i += 1
                while j >= l and nums[j] > mid: j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1

            if j - l + 1 >= k:
                r = j
            elif i - l >= k:
                mid_num = nums[l + k - 1]
                break
            else:
                k -= i - l
                l = i

        small_pos = -1
        equal_pos = -1
        for index, num in enumerate(nums):
            if num > mid_num:
                continue
            elif num == mid_num:
                nums[index] = nums[equal_pos + 1]
                nums[equal_pos + 1] = mid_num
                equal_pos += 1
            else:
                nums[index] = nums[equal_pos + 1]
                nums[equal_pos + 1] = nums[small_pos + 1]
                nums[small_pos + 1] = num
                small_pos += 1
                equal_pos += 1

        min_num = min(nums)
        for index in range(len(nums)):
            nums[index] -= min_num
        max_num = max(nums)

        for index in range(len(nums)):
            if nums[index] <= max_num:
                now = index
                prev_num = nums[index]
                while True:
                    if now <= (len(nums) - 1) / 2:
                        next_pos = ((len(nums) - 1) / 2 - now) * 2
                    else:
                        next_pos = (len(nums) - 1 - now) * 2 + 1
                    
                    if next_pos == index:
                        break
                    prev_num, nums[next_pos] = nums[next_pos], prev_num
                    nums[next_pos] += max_num + 1
                    now = next_pos

                nums[index] = prev_num + max_num + 1

        for index in range(len(nums)):
            nums[index] -= max_num + 1 
            nums[index] += min_num
```
