---
title: "1385. 两个数组间的距离值"
aliases: ["yiduobo的每日leetcode 1385.两个数组间的距离值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/二分算法", "题单/滑动窗口与双指针/四-双序列双指针", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402843605"
zhihu_id: "402843605"
zhihu_title: "yiduobo的每日leetcode 1385.两个数组间的距离值"
question_id: "1385"
question: "两个数组间的距离值"
problem_url: "https://leetcode.cn/problems/find-the-distance-value-between-two-arrays/"
difficulty: "Easy"
rating: 1235
created: "2021-08-23T22:44:26+08:00"
updated: "2021-08-23T22:44:26+08:00"
upvotes: 0
comments: 0
---

# 1385. 两个数组间的距离值

> **[yiduobo的每日leetcode 1385.两个数组间的距离值](https://zhuanlan.zhihu.com/p/402843605) · 知乎 · 2021-08-23 · 赞同 0**
> 力扣：[1385. 两个数组间的距离值](https://leetcode.cn/problems/find-the-distance-value-between-two-arrays/) · Easy · 灵茶山艾府：[两种方法：二分查找/双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1385.两个数组间的距离值

<https://leetcode-cn.com/problems/find-the-distance-value-between-two-arrays/>

由于数组的规模不大，那么可以先枚举arr1中的每个元素，对于当前元素，再枚举arr2中的每个元素然后检测。

我在这里采用的做法是先将arr2中的元素转化为区间，然后将区间按起点排序，再将有重叠部分的区间合并成一个区间。这样一来，我们就得到了一些单调递增，且互不相交的区间。

接下来，将arr1中元素从小到达排序后逐个检测其是否位于区间中，由于两边都是单调递增的，因此利用这个单调性可以在O(n)的时间复杂度内完成检测，因此最终的时间复杂度就是排序的复杂度O(nlogn)，由于上面朴素的平方算法。

最后附上python代码：

```python
class Solution(object):
    def findTheDistanceValue(self, arr1, arr2, d):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :type d: int
        :rtype: int
        """

        intervals = []
        for num in arr2:
            intervals.append([num - d, num + d])
        
        intervals = sorted(intervals, key=lambda d:d[0])
        merged = []
        nowx, nowy = intervals[0]
        for x, y in intervals[1:]:
            if x <= nowy:
                nowy = y
            else:
                merged.append([nowx, nowy])
                nowx, nowy = x, y
        
        merged.append([nowx, nowy])

        res = 0
        p = 0
        for num in sorted(arr1):
            while p < len(merged) and num > merged[p][1]:
                p += 1
            if p == len(merged) or num < merged[p][0]:
                res += 1

        return res
```
