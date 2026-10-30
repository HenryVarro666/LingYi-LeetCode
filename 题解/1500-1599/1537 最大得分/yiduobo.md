---
title: "1537. 最大得分"
aliases: ["yiduobo的每日leetcode 1537.最大得分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424230443"
zhihu_id: "424230443"
zhihu_title: "yiduobo的每日leetcode 1537.最大得分"
question_id: "1537"
question: "最大得分"
problem_url: "https://leetcode.cn/problems/get-the-maximum-score/"
created: "2021-10-21T22:41:41+08:00"
updated: "2021-10-21T22:41:41+08:00"
upvotes: 0
comments: 0
---

# 1537. 最大得分

> **[yiduobo的每日leetcode 1537.最大得分](https://zhuanlan.zhihu.com/p/424230443) · 知乎 · 2021-10-21 · 赞同 0**
> 力扣：[1537. 最大得分](https://leetcode.cn/problems/get-the-maximum-score/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1537.最大得分

[力扣](https://leetcode-cn.com/problems/get-the-maximum-score/)

由于题目可以在同值节点之间自由切换，那么如果按照同值节点对数组进行划分的话，就可以得到若干互不相关的子数组，而对于每一段子数组，则只需要选择其中和较大的那一侧。由于两个数组已经是有序的，那么可以使用类似二路归并的做法，使用两个指针从两个数组头部开始向后扫描，每次将较小那一侧的数组元素累加到改侧的累加和中，并将对应的指针向后移动。当遇到两个相同值时，则将当前两侧累加和中的较大值加入到答案中，并将累加和清零然后重复这个过程，直到扫描到末尾为止。

最后附上python代码。其中的cnt1和cnt2是由于累加和s1和s2可能超过mod，而如果在过程中就对mod取模将会影响最终对比s1和s2的大小，因此需要记录累加和大于等于mod的次数，也就是代码中的cnt1和cnt2：

```python
class Solution(object):
    def maxSum(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        n1 = len(nums1)
        n2 = len(nums2)
        p1 = p2 = 0
        s1 = s2 = 0
        cnt1 = cnt2 = 0
        res = 0
        mod = 10 ** 9 + 7
        while p1 < n1 and p2 < n2:
            if nums1[p1] == nums2[p2]:
                res += nums1[p1]
                if res >= mod:
                    res -= mod
                p1 += 1
                p2 += 1
                if cnt1 > cnt2 or (cnt1 == cnt2 and s1 > s2):
                    res += s1
                else:
                    res += s2
                
                if res >= mod:
                    res -= mod

                s1 = s2 = 0
                cnt1 = cnt2 = 0

            elif nums1[p1] < nums2[p2]:
                s1 += nums1[p1]
                p1 += 1
                if s1 >= mod:
                    cnt1 += 1
                    s1 -= mod
            else:
                s2 += nums2[p2]
                p2 += 1
                if s2 >= mod:
                    cnt2 += 1
                    s2 -= mod
                    
        while p1 < n1:
            s1 += nums1[p1]
            p1 += 1
            if s1 >= mod:
                cnt1 += 1
                s1 -= mod

        while p2 < n2:
            s2 += nums2[p2]
            p2 += 1
            if s2 >= mod:
                cnt2 += 1
                s2 -= mod

        if cnt1 > cnt2 or (cnt1 == cnt2 and s1 > s2):
            res += s1
        else:
            res += s2
        
        if res >= mod:
            res -= mod

        return res
```
