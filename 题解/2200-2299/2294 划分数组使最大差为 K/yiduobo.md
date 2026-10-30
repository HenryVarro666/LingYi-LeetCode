---
title: "2294. 划分数组使最大差为K"
aliases: ["yiduobo的每日leetcode 2294.划分数组使最大差为K"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553381341"
zhihu_id: "553381341"
zhihu_title: "yiduobo的每日leetcode 2294.划分数组使最大差为K"
question_id: "2294"
question: "划分数组使最大差为 K"
problem_url: "https://leetcode.cn/problems/partition-array-such-that-maximum-difference-is-k/"
difficulty: "Medium"
rating: 1416
created: "2022-08-13T15:20:51+08:00"
updated: "2022-08-13T15:20:51+08:00"
upvotes: 0
comments: 0
---

# 2294. 划分数组使最大差为K

> **[yiduobo的每日leetcode 2294.划分数组使最大差为K](https://zhuanlan.zhihu.com/p/553381341) · 知乎 · 2022-08-13 · 赞同 0**
> 力扣：[2294. 划分数组使最大差为 K](https://leetcode.cn/problems/partition-array-such-that-maximum-difference-is-k/) · Medium · 灵茶山艾府：[排序 + 贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2294.划分数组使最大差为K

[力扣](https://leetcode.cn/problems/partition-array-such-that-maximum-difference-is-k/)

不妨从数组中的最小值入手来考虑这个问题。由于nums中的每个数都需要被划分到一个子序列中，那么对于数组中的最小值nums[p]，其所在的子序列中所有的数都是大于等于nums[p]的，同时这些数都必须小于等于nums[p] + k，否则这些数与nums[p]的差就大于等k了。于是在这里就可以得到第一个子序列划分，其中的数为nums中的最小值nums[p]以及所有小于等于nums[p] + k的数。

接下来，对于剩下的数，又可以找出新的最小值，然后按照上面的方法进行第二次划分。以此类推，不断找出剩余数中的最小值并将满足条件的数划分到同一个子序列中，直到所有数都被划分完。

为了完成上面的划分操作，需要知道当前剩余数中的最小值以及所有满足小于等于这个最小值加上k的数有哪些，那么可以将nums从小到大进行排序，然后使用两个指针l和r分别指向当前剩余数中最小值的下标以及满足条件的数的最大值的下标。每一轮操作中，先确定l的位置，然后根据nums[l] + k与nums[r]的大小关系来确定r的位置。确定了l和r之后，其中的数就是一个子序列中的数，此时更新答案，然后将l移动到r + 1然后重复这个过程即可。

最后附上python代码：

```python
class Solution(object):
    def partitionArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        sorted_nums = sorted(nums)
        l = 0
        r = 0
        res = 0
        while l < len(sorted_nums):
            while r + 1 < len(sorted_nums) and sorted_nums[r + 1] - sorted_nums[l] <= k:
                r += 1
            
            res += 1
            l = r + 1
            r = l
        
        return res
```
