---
title: "2321. 拼接数组的最大分数"
aliases: ["yiduobo的每日leetcode 2321.拼接数组的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557481560"
zhihu_id: "557481560"
zhihu_title: "yiduobo的每日leetcode 2321.拼接数组的最大分数"
question_id: "2321"
question: "拼接数组的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-of-spliced-array/"
difficulty: "Hard"
rating: 1791
created: "2022-08-24T22:51:30+08:00"
updated: "2022-08-24T22:51:30+08:00"
upvotes: 0
comments: 0
---

# 2321. 拼接数组的最大分数

> **[yiduobo的每日leetcode 2321.拼接数组的最大分数](https://zhuanlan.zhihu.com/p/557481560) · 知乎 · 2022-08-24 · 赞同 0**
> 力扣：[2321. 拼接数组的最大分数](https://leetcode.cn/problems/maximum-score-of-spliced-array/) · Hard · 灵茶山艾府：[转换成最大子数组和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2321.拼接数组的最大分数

[力扣](https://leetcode.cn/problems/maximum-score-of-spliced-array/)

题目可以拆分成两个问题，分别是

1、使用nums2中的某个子数组替代nums1中对应位置的子数组后使得nums1之和最大

2、使用nums1中的某个子数组替代nums2中对应位置的子数组后使得nums2之和最大

最终答案就是这两个最大值中较大的那一个。

这两个问题是对称的，因此只要找出其中一个问题的处理方法，使用相同的方法计算另一个问题就行了。在这里不妨考虑问题1，使用nums2中的某个子数组来替代nums1中对应位置的子数组。

在这里不妨设diff[i] \= nums2[i] - nums1[i]，那么在替换掉l到r这一段时，nums1的和就变成了

s \= (nums1[0] + ... + nums1[l - 1]) + (nums2[l] + ... + nums2[r]) + (nums1[r + 1] + ... + nums1[n - 1])

在这里将nums2[i] \= diff[i] + nums1[i]代入，就有

s \= (nums1[0] + ... + nums1[l - 1] + (nums1[l] + ... + nums1[r]) + (diff[l] + diff[l + 1] + ... + diff[r]) + (nums1[r + 1] + ... + nums1[n - 1])

将nums1有关的项收集起来，就有

s \= sum(nums1) + diff[l] + diff[l + 1] + ... + diff[r]

由于sum(nums1)是个常量，那么为了使得s最大，实际上就是要让diff[l] + diff[l + 1] + ... + diff[r]最大，可以发现这就是非常熟悉的最大子段和问题。那么只需先一趟遍历，计算出diff数组，然后对diff数组求最大子段和，即为f1，最终答案就是sum(nums1) + f1了。

反过来，对于问题2，同样是使用最大子段和来求解，不过这里的diff与问题1中的diff刚好相反。设此时求得的最大子段和为f2，那么问题2的最终答案就是sum(nums2) + f2。

综合起来，最终答案就是max(sum(nums1) + f1, sum(nums2) + f2)

最后附上python代码：

```python
class Solution(object):
    def maximumsSplicedArray(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        max_f1 = max_f2 = 0
        f1 = f2 = 0
        s1 = s2 = 0
        for index in range(len(nums1)):
            s1 += nums1[index]
            s2 += nums2[index]

            diff = nums1[index] - nums2[index]
            f1 -= diff
            f2 += diff

            if f1 < 0:
                f1 = 0
            if f2 < 0:
                f2 = 0

            max_f1 = max(max_f1, f1)
            max_f2 = max(max_f2, f2)

        return max(s1 + max_f1, s2 + max_f2)
```
