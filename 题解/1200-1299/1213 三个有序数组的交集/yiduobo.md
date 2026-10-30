---
title: "1213. 三个有序数组的交集"
aliases: ["yiduobo的每日leetcode 1213.三个有序数组的交集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613024773"
zhihu_id: "613024773"
zhihu_title: "yiduobo的每日leetcode 1213.三个有序数组的交集"
question_id: "1213"
question: "三个有序数组的交集"
problem_url: "https://leetcode.cn/problems/intersection-of-three-sorted-arrays/"
created: "2023-03-10T21:55:21+08:00"
updated: "2023-03-10T21:55:21+08:00"
upvotes: 0
comments: 0
---

# 1213. 三个有序数组的交集

> **[yiduobo的每日leetcode 1213.三个有序数组的交集](https://zhuanlan.zhihu.com/p/613024773) · 知乎 · 2023-03-10 · 赞同 0**
> 力扣：[1213. 三个有序数组的交集](https://leetcode.cn/problems/intersection-of-three-sorted-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1213.三个有序数组的交集

[力扣](https://leetcode.cn/problems/intersection-of-three-sorted-arrays/)

本题可以认为是之前1198题的弱化版，可以直接沿用之前1198题的处理方法。

对第一个数组进行一趟遍历，同时使用两个变量p和q分别记录后面两个数组接下来需要检测的下标。根据单调性，随着遍历的进行，p和q也只会逐渐增大，从而在O(n)的时间内找出最终的结果。

最后附上python代码：

```python
class Solution(object):
    def arraysIntersection(self, arr1, arr2, arr3):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :type arr3: List[int]
        :rtype: List[int]
        """

        p = q = 0
        res = []

        for num in arr1:
            while p < len(arr2) and arr2[p] < num:
                p += 1
            
            if p == len(arr2):
                break
            
            while q < len(arr3) and arr3[q] < num:
                q += 1
            
            if q == len(arr3):
                break
            
            if arr2[p] == arr3[q] == num:
                res.append(num)
        
        return res
```
