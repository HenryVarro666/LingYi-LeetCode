---
title: "360. 有序转化数组"
aliases: ["yiduobo的每日leetcode 360.有序转化数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597860728"
zhihu_id: "597860728"
zhihu_title: "yiduobo的每日leetcode 360.有序转化数组"
question_id: "360"
question: "有序转化数组"
problem_url: "https://leetcode.cn/problems/sort-transformed-array/"
created: "2023-01-10T00:36:37+08:00"
updated: "2023-01-10T00:36:37+08:00"
upvotes: 0
comments: 0
---

# 360. 有序转化数组

> **[yiduobo的每日leetcode 360.有序转化数组](https://zhuanlan.zhihu.com/p/597860728) · 知乎 · 2023-01-10 · 赞同 0**
> 力扣：[360. 有序转化数组](https://leetcode.cn/problems/sort-transformed-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

360.有序转化数组

[力扣](https://leetcode.cn/problems/sort-transformed-array/)

由于a和b都可能为0，那么需要分情况进行讨论：

1、当a和b都为0时：

这种情况比较简单，答案就是n个c

2、当a为0，b不为0时：

f(x)是一个单调函数。当b大于0时，f(x)单调递增，否则单调递减。此时只需逐个将nums中的数带入，那么得到的结果数组也会是一个单调数组，此时若b小于0，需要翻转答案数组。

3、当a不为0时：

f(x)是一个凸函数。

此时可以使用两个指针left和right分别指向nums剩余数中最小值和最大值的下标。接下来，每次将nums剩余数中的最大值nums[right]和最小值nums[left]带入到f(x)，然后根据a与0的大小关系就可以判断f(nums[left])和f(nums[right])哪个离极值点更远。将更远的这个值加入到答案数组中，然后将对应的指针向中间移动，直到处理完所有的数字。

这样一来，同样可以得到一个单调的数组。需要注意的是，a大于0时得到的是单调递减的数组，因此这种情况下应该是a大于0时才需要翻转答案数组。

最后附上python代码：

```python
class Solution(object):
    def sortTransformedArray(self, nums, a, b, c):
        """
        :type nums: List[int]
        :type a: int
        :type b: int
        :type c: int
        :rtype: List[int]
        """

        n = len(nums)

        def f(x):
            return a * x * x + b * x + c

        if a == 0:
            if b == 0:
                return [c] * n
            else:
                res = [f(x) for x in nums]
                if b < 0:
                    res.reverse()
                return res
        
        else:
            if a > 0:
                delta = 1
            else:
                delta = -1

            left = 0
            right = n - 1
            res = []
            while left <= right:
                left_v = f(nums[left])
                right_v = f(nums[right])
                if left_v * delta > right_v * delta:
                    res.append(left_v)
                    left += 1
                else:
                    res.append(right_v)
                    right -= 1
            
            if a > 0:
                res.reverse()
            
            return res
```
