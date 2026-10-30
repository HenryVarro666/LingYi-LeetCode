---
title: "1818. 绝对差值和"
aliases: ["yiduobo的每日leetcode 1818.绝对差值和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465968051"
zhihu_id: "465968051"
zhihu_title: "yiduobo的每日leetcode 1818.绝对差值和"
question_id: "1818"
question: "绝对差值和"
problem_url: "https://leetcode.cn/problems/minimum-absolute-sum-difference/"
created: "2022-02-10T23:10:45+08:00"
updated: "2022-02-10T23:10:45+08:00"
upvotes: 0
comments: 0
---

# 1818. 绝对差值和

> **[yiduobo的每日leetcode 1818.绝对差值和](https://zhuanlan.zhihu.com/p/465968051) · 知乎 · 2022-02-10 · 赞同 0**
> 力扣：[1818. 绝对差值和](https://leetcode.cn/problems/minimum-absolute-sum-difference/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1818.绝对差值和

[力扣](https://leetcode-cn.com/problems/minimum-absolute-sum-difference/)

按照题目描述，可以将nums1中任意位置的数变换成nums1中的某个数，设这个变换的位置为index，变换的目标为p，那么最终就是要求abs(nums1[index] - nums2[index]) - abs(nums1[p] - nums2[index])最大。

对于上面这个式子，一个很自然的想法就是枚举index的位置，然后想办法找到p。在确定了index之后，为了使得上面的式子最大，那么就需要nums1[p]尽量接近nums2[index]。为了解决这个问题，可以先将nums1排序得到sorted_nums1，然后通过二分法找到位置q，这里的q满足sorted_nums1[q] \<\= nums2[index] \<\= sorted_nums1[q + 1]，那么index对应的p必然是q和q + 1之中的一个。

除此之外，也可以将nums1和nums2都进行排序，然后利用单调性使用双指针来找到这个p。

具体实现上，主要是需要注意边界情况，即nums1中没有比nums2[index]小的数，或者没有比nums2[index]大的数这两种边界情况。

得到上面式子的最大值之后，还需要计算nums1和nums2在每个位置上的绝对值之差，然后减去这个最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minAbsoluteSumDiff(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        p = 0
        n = len(nums1)
        res = 0
        mod = 10 ** 9 + 7
        for index in range(n):
            res += abs(nums1[index] - nums2[index])
            if res >= mod:
                res -= mod
        
        max_change = 0
        sorted_nums1 = sorted(list(set(nums1)))
        for num, diff in sorted(zip(nums2, [abs(nums1[index] - nums2[index]) for index in range(n)])):
            if num <= sorted_nums1[0]:
                if abs(sorted_nums1[0] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[0] - num))
            elif num > sorted_nums1[-1]:
                if abs(sorted_nums1[-1] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[-1] - num))
            else:
                while p < len(sorted_nums1) and sorted_nums1[p] <= num:
                    p += 1
                if p < len(sorted_nums1) and abs(sorted_nums1[p] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[p] - num))
                if p > 0 and abs(sorted_nums1[p - 1] - num) < diff:
                    max_change = max(max_change, diff - abs(sorted_nums1[p - 1] - num))
        
        res = res - max_change
        if res < 0:
            res += mod

        return res
```
