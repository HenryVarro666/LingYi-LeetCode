---
title: "1755. 最接近目标值的子序列和"
aliases: ["yiduobo的每日leetcode 1755.最接近目标值的子序列和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/459169163"
zhihu_id: "459169163"
zhihu_title: "yiduobo的每日leetcode 1755.最接近目标值的子序列和"
question_id: "1755"
question: "最接近目标值的子序列和"
problem_url: "https://leetcode.cn/problems/closest-subsequence-sum/"
created: "2022-01-18T23:00:40+08:00"
updated: "2022-01-18T23:00:40+08:00"
upvotes: 0
comments: 0
---

# 1755. 最接近目标值的子序列和

> **[yiduobo的每日leetcode 1755.最接近目标值的子序列和](https://zhuanlan.zhihu.com/p/459169163) · 知乎 · 2022-01-18 · 赞同 0**
> 力扣：[1755. 最接近目标值的子序列和](https://leetcode.cn/problems/closest-subsequence-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1755.最接近目标值的子序列和

[力扣](https://leetcode-cn.com/problems/closest-subsequence-sum/)

题目非常取巧地给了一个40的数据范围。一个常见的数据范围是2^20 \= 1048576，也就是百万规模。这个大小差不多刚好是一般情况下运算规模的上限。

对于本题，则可以将40分成两组20，然后执行暴力dfs，这样一来就会得到两个大小为1048576的数组，分别存放了这两组数所有组合的数值和。

接下来的任务就是从这两个数组中各选出一个数，使得这两个数的和的大小最接近目标值。这个问题则可以利用类似两数之和的做法，在这里有所区别但答题思路差不多，同样是排序后利用单调性。具体来说，是将两个数组从小到大进行排序，接下来从头开始枚举第一个数组nums1中的数，并设置指针p从尾部开始向前扫描第二个数组nums2中的数，要求满足

nums1[index] + nums2[p] \<\= goal \<\= nums1[index] + nums[p + 1]

每次得到p之后，就根据这两个数的和与goal的差距来更新答案。当index向后移动时，nums[index]是越来越大的，因此此时的p只有越来越小才能满足上面的条件，于是可以在index向后移动时在当前p的基础上向前移动。这样一来就可以在均摊O(1)的时间内确定每个index对应的p的位置。

最后附上python代码：

```python
class Solution(object):
    def minAbsDifference(self, nums, goal):
        """
        :type nums: List[int]
        :type goal: int
        :rtype: int
        """

        n = len(nums)
        if n == 1:
            return min(abs(nums[0] - goal), abs(goal))
        
        cut_pos = n / 2
        left_sum = set([0])
        for num in nums[:cut_pos]:
            left_sum = left_sum.union(set([x + num for x in left_sum]))
        
        right_sum = set([0])
        for num in nums[cut_pos:]:
            right_sum = right_sum.union(set([x + num for x in right_sum]))
        
        left_list = sorted(left_sum)
        right_list = sorted(right_sum)

        p = len(right_list) - 1
        res = abs(goal)
        for num in left_list:
            while p >= 0 and num + right_list[p] > goal:
                p -= 1
            
            if p >= 0:
                res = min(res, abs(num + right_list[p] - goal))
            if p < len(right_list) - 1:
                res = min(res, abs(num + right_list[p + 1] - goal))
        
        return res
```
