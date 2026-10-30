---
title: "1855. 下标对中的最大距离"
aliases: ["yiduobo的每日leetcode 1855.下标对中的最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/472121026"
zhihu_id: "472121026"
zhihu_title: "yiduobo的每日leetcode 1855.下标对中的最大距离"
question_id: "1855"
question: "下标对中的最大距离"
problem_url: "https://leetcode.cn/problems/maximum-distance-between-a-pair-of-values/"
difficulty: "Medium"
rating: 1515
created: "2022-02-24T23:54:20+08:00"
updated: "2022-02-24T23:54:20+08:00"
upvotes: 0
comments: 0
---

# 1855. 下标对中的最大距离

> **[yiduobo的每日leetcode 1855.下标对中的最大距离](https://zhuanlan.zhihu.com/p/472121026) · 知乎 · 2022-02-24 · 赞同 0**
> 力扣：[1855. 下标对中的最大距离](https://leetcode.cn/problems/maximum-distance-between-a-pair-of-values/) · Medium · 灵茶山艾府：[双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1855.下标对中的最大距离

[力扣](https://leetcode-cn.com/problems/maximum-distance-between-a-pair-of-values/)

题目非常贴心地将两个数组都排好了序，那么很自然想到利用数组的单调性来解决问题。

对于nums1\[index\]，设p\[index\]为满足nums2\[p\[index\]\] >\= nums1\[index\]的最大下标值，那么对于nums1\[index + 1\]而言，首先可以确定的是由于nums1\[index\] >\= nums1\[index + 1\]，因此必然有nums2\[p\[index\]\] >\= nums1\[index\] >\= nums1\[index + 1\]，换言之，此时求解p\[index + 1\]就只需在p\[index\]的基础上继续向后遍历。这样一来，就可以对nums1一趟遍历，在均摊O(1)的时间复杂度内求出所有的p。而在求解p的过程中，利用当前的index以及p\[index\]更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        j = 0
        res = 0
        for i in range(len(nums1)):
            while j < len(nums2) and nums1[i] <= nums2[j]:
                j += 1
            res = max(res, j - i - 1)
            if j == len(nums2):
                break
        
        return res
```
