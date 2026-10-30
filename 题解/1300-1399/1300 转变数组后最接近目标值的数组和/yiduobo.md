---
title: "1300. 转变数组后最接近目标值的数组和"
aliases: ["yiduobo的每日leetcode 1300.转变数组后最接近目标值的数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390811169"
zhihu_id: "390811169"
zhihu_title: "yiduobo的每日leetcode 1300.转变数组后最接近目标值的数组和"
question_id: "1300"
question: "转变数组后最接近目标值的数组和"
problem_url: "https://leetcode.cn/problems/sum-of-mutated-array-closest-to-target/"
created: "2021-07-18T16:26:42+08:00"
updated: "2021-07-18T16:26:42+08:00"
upvotes: 1
comments: 0
---

# 1300. 转变数组后最接近目标值的数组和

> **[yiduobo的每日leetcode 1300.转变数组后最接近目标值的数组和](https://zhuanlan.zhihu.com/p/390811169) · 知乎 · 2021-07-18 · 赞同 1**
> 力扣：[1300. 转变数组后最接近目标值的数组和](https://leetcode.cn/problems/sum-of-mutated-array-closest-to-target/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1330.转变数组后最接近目标值的数组和

[力扣](https://leetcode-cn.com/problems/sum-of-mutated-array-closest-to-target/)

首先可以明确的是，随着value的减小，数组之和也会减小，而随着value的增大，数组之和也会增大，因此可以使用二分来寻找最终的value。

二分的下界自然是0，而二分的上界应该是max(arr)，因为当value大于等于max(arr)时，数组之后都会是arr中所有元素之和，因此选择大于max(arr)的值作为value是没有意义的。

确定了二分的值mid之后，需要想办法计算当前数组之和，这个和可以分为两部分，分别为小于等于mid的元素之和，以及mid乘以大于mid的元素数量。一个可行的做法是先将arr从小到大进行排序，那么小于mid的元素之和就是排序后arr中的某个前缀和，那么我们可以先预处理出排序后arr的前缀和数组，记为s。接下来就可以在arr中再次使用二分，确定mid在排序后arr中的位置p，对应的前缀和就是s[p]，而后续大于mid的和就是mid \* (n - p - 1)。

于是现在的做法就是：

1、先将arr从小到大进行排序，并计算出前缀和数组s

2、二分答案value，上界为arr[-1]，下界为0。对于当前二分到的mid：

2-1）若mid >\= arr[-1]，那么此时的数组之和就是s[-1]

2-2）若mid \<\= arr[0]，那么此时的数组之和就是mid \* n

2-3）其他情况下，我们二分mid在arr中的位置，找到对应的位置p，那么此时的数组之和就是s[p] + mid \* (n - p - 1)

计算好当前数组之和后，计算其与target的差值，更新答案以及二分mid的范围即可。

最后附上python代码：

```python
class Solution(object):
    def findBestValue(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """

        arr = sorted(arr)
        n = len(arr)
        s = [arr[0]]
        for num in arr[1:]:
            s.append(s[-1] + num)
        l_v = 0
        r_v = arr[-1]
        diff = None
        while l_v <= r_v:
            mid_v = (l_v + r_v + 1) >> 1
            if mid_v >= arr[-1]:
                tmp = s[-1]
            elif mid_v <= arr[0]:
                tmp = mid_v * n
            else:
                l_p = 0
                r_p = n - 1
                while l_p < r_p:
                    mid_p = (l_p + r_p + 1) >> 1
                    if arr[mid_p] <= mid_v:
                        l_p = mid_p
                    else:
                        r_p = mid_p - 1
                
                tmp = s[l_p] + mid_v * (n - l_p - 1)

            if diff is None or diff > abs(tmp - target):
                diff = abs(tmp - target)
                res = mid_v
            elif diff == abs(tmp - target) and res > mid_v:
                res = mid_v

            if tmp <= target:
                l_v = mid_v + 1
            else:
                r_v = mid_v - 1
        
        return res
```
