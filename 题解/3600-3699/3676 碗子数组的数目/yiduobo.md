---
title: "3676. 碗子数组的数目"
aliases: ["yiduobo的每日leetcode 3676.碗子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952810893101478628"
zhihu_id: "1952810893101478628"
zhihu_title: "yiduobo的每日leetcode 3676.碗子数组的数目"
question_id: "3676"
question: "碗子数组的数目"
problem_url: "https://leetcode.cn/problems/count-bowl-subarrays/"
difficulty: "Medium"
rating: 1848
created: "2025-09-22T21:49:43+08:00"
updated: "2025-09-22T21:49:45+08:00"
upvotes: 0
comments: 0
---

# 3676. 碗子数组的数目

> **[yiduobo的每日leetcode 3676.碗子数组的数目](https://zhuanlan.zhihu.com/p/1952810893101478628) · 知乎 · 2025-09-22 · 赞同 0**
> 力扣：[3676. 碗子数组的数目](https://leetcode.cn/problems/count-bowl-subarrays/) · Medium · 灵茶山艾府：[单调栈，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3676.碗子数组的数目

[3676. 碗子数组的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-bowl-subarrays/description/)

题目给出一个整数数组nums，其中包含互不相同的元素。

若nums中的一个子数组nums[left...right]，其长度至少为3，且两端元素的最小值严格大于中间所有元素的最大值，即min(nums[left], nums[right]) > max(nums[left + 1], ..., nums[right - 1])，那么就称其为碗子数组。

问nums中碗子数组的数量。

基于题目中关于碗子数组的定义来看，可以从不等式两侧的极值，也就是从两端元素的较小值，或者从中间元素的最大值出发来进行计算，我在这里选择的是后者。

对于数组中的某个元素nums[index]，若其是某个碗子数组的中间部分的最大值，那么这个碗的左边界只能index左侧的第一个更大元素对应的下标，而右边界则只能是index右侧的第一个更大元素对应的下标，理由是如果在碗的边界之间不能存在比nums[index]更大的元素，因此左右两侧的边界都只能是第一个更大的元素。

由于在这里并不需要关心具体的碗子数组是如何构成的，因此在这里只需要保证nums[index]左右两侧都有更大的元素，那么就必然存在一个以nums[index]为中间部分最大值的碗子数组。

基于上面的结论，就只需要先正序一趟遍历，使用数组left记录每个元素左侧是否存在更大的元素，然后再倒序一趟遍历，检测每个元素右侧是否存在更大的元素，配合left确定是否存在以nums[index]作为中间部分最大值的碗子数组并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def bowlSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        left = [False] * n
        ma = nums[0]
        for index in range(1, n):
            if nums[index] < ma:
                left[index] = True
            else:
                ma = nums[index]
        
        ma = nums[-1]
        res = 0
        for index in range(n - 1, 0, -1):
            if nums[index] < ma:
                if left[index]:
                    res += 1
            else:
                ma = nums[index]
        
        return res
```
