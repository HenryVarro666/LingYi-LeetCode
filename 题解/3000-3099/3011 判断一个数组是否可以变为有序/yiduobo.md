---
title: "3011. 判断一个数组是否可以变为有序"
aliases: ["yiduobo的每日leetcode 3011.判断一个数组是否可以变为有序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693969319"
zhihu_id: "693969319"
zhihu_title: "yiduobo的每日leetcode 3011.判断一个数组是否可以变为有序"
question_id: "3011"
question: "判断一个数组是否可以变为有序"
problem_url: "https://leetcode.cn/problems/find-if-array-can-be-sorted/"
difficulty: "Medium"
rating: 1497
created: "2024-04-22T23:36:51+08:00"
updated: "2024-04-22T23:36:51+08:00"
upvotes: 1
comments: 0
---

# 3011. 判断一个数组是否可以变为有序

> **[yiduobo的每日leetcode 3011.判断一个数组是否可以变为有序](https://zhuanlan.zhihu.com/p/693969319) · 知乎 · 2024-04-22 · 赞同 1**
> 力扣：[3011. 判断一个数组是否可以变为有序](https://leetcode.cn/problems/find-if-array-can-be-sorted/) · Medium · 灵茶山艾府：[教你一次性把代码写对！O(n) 分组循环（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3011.判断一个数组是否可以变为有序

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-if-array-can-be-sorted/)

题目可以将二进制位中1数量相同的相邻数字进行任意次数的交换，那么在这里就可以将数组按照二进制位中1的数量划分成若干的子数组，那么各个子数组内部的数字可以任意交换，但子数组间的数不能交换。更进一步的，子数组内部由于可以任意交换，因此一定是可以变为有序的，那么如果要使得整个数组有序，就要求当前子数组中的所有数都大于等于上一个子数组的最大值。

于是可以一趟遍历，在划分子数组的同时对比当前子数组的值与上一个子数组最大值的大小，并计算当前子数组的最大值，用来与下一个子数组中的数进行对比。

最后附上python代码：

```python
class Solution(object):
    def canSortArray(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        def count(x):
            cnt = 0
            while x:
                if x % 2 == 1:
                    cnt += 1
                x //= 2
            return cnt

        pre_ma = 0
        ma = nums[0]
        cnt = count(nums[0])
        for index in range(1, len(nums)):
            v = count(nums[index])
            if v == cnt:
                ma = max(ma, nums[index])
            else:
                pre_ma = ma
                ma = nums[index]
                cnt = v

            if nums[index] < pre_ma:
                return False

        return True
```
