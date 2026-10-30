---
title: "2465. 不同的平均值数目"
aliases: ["yiduobo的每日leetcode 2465.不同的平均值数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587034124"
zhihu_id: "587034124"
zhihu_title: "yiduobo的每日leetcode 2465.不同的平均值数目"
question_id: "2465"
question: "不同的平均值数目"
problem_url: "https://leetcode.cn/problems/number-of-distinct-averages/"
difficulty: "Easy"
created: "2022-11-27T03:31:02+08:00"
updated: "2022-11-27T03:31:02+08:00"
upvotes: 0
comments: 0
---

# 2465. 不同的平均值数目

> **[yiduobo的每日leetcode 2465.不同的平均值数目](https://zhuanlan.zhihu.com/p/587034124) · 知乎 · 2022-11-27 · 赞同 0**
> 力扣：[2465. 不同的平均值数目](https://leetcode.cn/problems/number-of-distinct-averages/) · Easy · 灵茶山艾府：[排序+遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2465.不同的平均值数目

[力扣](https://leetcode.cn/problems/number-of-distinct-averages/)

题目每次要求选出剩余数中最大和最小值并计算平均数，那么只需将数组从小到大进行排序，然后从两边向中间遍历，每次取当前遍历到的两个数求和并加入到集合中。遍历完成后集合的大小即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def distinctAverages(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort()
        left = 0
        right = len(nums) - 1
        sum_set = set()
        while left < right:
            sum_set.add(nums[left] + nums[right])
            left += 1
            right -= 1
        
        return len(sum_set)
```
