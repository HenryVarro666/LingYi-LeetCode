---
title: "2540. 最小公共值"
aliases: ["yiduobo的每日leetcode 2540.最小公共值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637860015"
zhihu_id: "637860015"
zhihu_title: "yiduobo的每日leetcode 2540.最小公共值"
question_id: "2540"
question: "最小公共值"
problem_url: "https://leetcode.cn/problems/minimum-common-value/"
difficulty: "Easy"
created: "2023-06-18T22:34:48+08:00"
updated: "2023-06-18T22:34:48+08:00"
upvotes: 0
comments: 0
---

# 2540. 最小公共值

> **[yiduobo的每日leetcode 2540.最小公共值](https://zhuanlan.zhihu.com/p/637860015) · 知乎 · 2023-06-18 · 赞同 0**
> 力扣：[2540. 最小公共值](https://leetcode.cn/problems/minimum-common-value/) · Easy · 灵茶山艾府：[双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2540.最小公共值

[力扣](https://leetcode.cn/problems/minimum-common-value/)

由于题目给出的两个数组都已经排好序了，那么在这里就可以参考二路归并的处理方法，使用两个指针分别从两个数组头部向后移动，每一轮都将指向较小数的那个指针向后移动，直到二者指向的值相等，或者某个指针来到数组末尾为止。

最后附上python代码：

```python
class Solution(object):
    def getCommon(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        p1 = p2 = 0
        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] == nums2[p2]:
                return nums1[p1]
            elif nums1[p1] < nums2[p2]:
                p1 += 1
            else:
                p2 += 1
        
        return -1
```
