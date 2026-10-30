---
title: "2161. 根据给定数字划分数组"
aliases: ["yiduobo的每日leetcode 2161.根据给定数字划分数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/532025566"
zhihu_id: "532025566"
zhihu_title: "yiduobo的每日leetcode 2161.根据给定数字划分数组"
question_id: "2161"
question: "根据给定数字划分数组"
problem_url: "https://leetcode.cn/problems/partition-array-according-to-given-pivot/"
difficulty: "Medium"
created: "2022-06-22T00:12:50+08:00"
updated: "2022-06-22T00:12:50+08:00"
upvotes: 0
comments: 0
---

# 2161. 根据给定数字划分数组

> **[yiduobo的每日leetcode 2161.根据给定数字划分数组](https://zhuanlan.zhihu.com/p/532025566) · 知乎 · 2022-06-22 · 赞同 0**
> 力扣：[2161. 根据给定数字划分数组](https://leetcode.cn/problems/partition-array-according-to-given-pivot/) · Medium · 灵茶山艾府：[简单做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2161.根据给定数字划分数组

[力扣](https://leetcode.cn/problems/partition-array-according-to-given-pivot/)

题目要求对数组进行类似快排的大小划分，同时要求划分后的结果是稳定的，那么在这里就不适用两端直接向中间扫描的做法了。

在这里可以先进行一趟遍历，找出数组中小于等于pivot的数的个数cnt，那么大于pivot的数在答案数组中的下标就必然是从cnt开始。接下来使用两个指针l和r，分别表示小于pivot和大于pivot的数在答案数组中的初始填充下标，那么l和r的初始值就应该是0和cnt。

再然后就只需要从左向右遍历数组，对于小于pivot的数将其填充到答案数组l的位置，然后将l加上1，对于等于pivot的数可以先暂时略过，而对于大于pivot的数则将其填充到答案数组r的位置，然后将r加上1。

遍历完成后，再将l到cnt - 1这一段用pivot填充即可。

最后附上python代码：

```python
class Solution(object):
    def pivotArray(self, nums, pivot):
        """
        :type nums: List[int]
        :type pivot: int
        :rtype: List[int]
        """

        n = len(nums)
        res = [pivot] * n
        l = r = 0
        for num in nums:
            if num <= pivot:
                r += 1
        
        for num in nums:
            if num < pivot:
                res[l] = num
                l += 1
            elif num > pivot:
                res[r] = num
                r += 1
        
        return res
```
