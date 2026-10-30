---
title: "2570. 合并两个二维数组"
aliases: ["yiduobo的每日leetcode 2570.合并两个二维数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641286383"
zhihu_id: "641286383"
zhihu_title: "yiduobo的每日leetcode 2570.合并两个二维数组"
question_id: "2570"
question: "合并两个二维数组 - 求和法"
problem_url: "https://leetcode.cn/problems/merge-two-2d-arrays-by-summing-values/"
difficulty: "Easy"
created: "2023-07-04T01:12:19+08:00"
updated: "2023-07-04T01:12:19+08:00"
upvotes: 0
comments: 0
---

# 2570. 合并两个二维数组

> **[yiduobo的每日leetcode 2570.合并两个二维数组](https://zhuanlan.zhihu.com/p/641286383) · 知乎 · 2023-07-04 · 赞同 0**
> 力扣：[2570. 合并两个二维数组 - 求和法](https://leetcode.cn/problems/merge-two-2d-arrays-by-summing-values/) · Easy · 灵茶山艾府：[线性做法：归并排序 + O(1) 额外空间](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2570.合并两个二维数组

[力扣](https://leetcode.cn/problems/merge-two-2d-arrays-by-summing-values/)

题目非常贴心地将数组都按照id排好了序，那么只需使用两个指针从数组头部开始向后走，使用类似二路归并的做法，每次将id较小那一侧指针对应的值添加到答案数组中，并将对应的指针向后移动即可。另外需要注意处理id相同的情况。

最后附上python代码：

```python
class Solution(object):
    def mergeArrays(self, nums1, nums2):
        """
        :type nums1: List[List[int]]
        :type nums2: List[List[int]]
        :rtype: List[List[int]]
        """

        p1 = p2 = 0
        res = []
        while p1 < len(nums1) or p2 < len(nums2):
            if p1 == len(nums1):
                res.append(nums2[p2][:])
                p2 += 1
            elif p2 == len(nums2):
                res.append(nums1[p1][:])
                p1 += 1
            elif nums1[p1][0] < nums2[p2][0]:
                res.append(nums1[p1][:])
                p1 += 1
            elif nums1[p1][0] > nums2[p2][0]:
                res.append(nums2[p2][:])
                p2 += 1
            else:
                res.append(nums1[p1][:])
                res[-1][1] += nums2[p2][1]
                p1 += 1
                p2 += 1
        
        return res
```
