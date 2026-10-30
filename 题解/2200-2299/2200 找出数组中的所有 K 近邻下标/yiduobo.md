---
title: "2200. 找出数组中的所有K近邻下标"
aliases: ["yiduobo的每日leetcode 2200.找出数组中的所有K近邻下标"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538972659"
zhihu_id: "538972659"
zhihu_title: "yiduobo的每日leetcode 2200.找出数组中的所有K近邻下标"
question_id: "2200"
question: "找出数组中的所有 K 近邻下标"
problem_url: "https://leetcode.cn/problems/find-all-k-distant-indices-in-an-array/"
difficulty: "Easy"
created: "2022-07-07T23:59:34+08:00"
updated: "2022-07-07T23:59:34+08:00"
upvotes: 0
comments: 0
---

# 2200. 找出数组中的所有K近邻下标

> **[yiduobo的每日leetcode 2200.找出数组中的所有K近邻下标](https://zhuanlan.zhihu.com/p/538972659) · 知乎 · 2022-07-07 · 赞同 0**
> 力扣：[2200. 找出数组中的所有 K 近邻下标](https://leetcode.cn/problems/find-all-k-distant-indices-in-an-array/) · Easy · 灵茶山艾府：[两种 O(n) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2200.找出数组中的所有K近邻下标

[力扣](https://leetcode.cn/problems/find-all-k-distant-indices-in-an-array/)

由于题目的数据规模比较小，因此直接使用朴素的O(n^2)算法也是可以的，不过还存在更好的做法。

题目要求找出所有离key的距离小于k的下标，那么不妨反过来思考，对于nums中所有值等于key的数影响到的范围是哪些，然后将这些范围合并起来，也就是说可以先对nums进行一趟遍历，找出所有值等于key的下标index，然后将区间[index - k, index + k]加入到区间数组intervals当中。

在这里需要注意区间的边界不应该越过数组的边界0或者n - 1。

接下来，由于intervals中的区间已经天然就按左边界排好序了，因此只需要一趟遍历，通过判断当前区间的左边界是否小于等于上一个区间的右边界来决定是否合并两个区间即可。

最后附上python代码：

```python
class Solution(object):
    def findKDistantIndices(self, nums, key, k):
        """
        :type nums: List[int]
        :type key: int
        :type k: int
        :rtype: List[int]
        """

        n = len(nums)
        intervals = []
        for index, num in enumerate(nums):
            if num == key:
                intervals.append([max(0, index - k), min(n - 1, index + k)])
        
        if not intervals:
            return []
        
        res = []
        nowx, nowy = intervals[0]
        for x, y in intervals[1:]:
            if nowy >= x:
                nowy = y
            else:
                res.extend(range(nowx, nowy + 1))
                nowx, nowy = x, y
        
        res.extend(range(nowx, nowy + 1))
        return res
```
