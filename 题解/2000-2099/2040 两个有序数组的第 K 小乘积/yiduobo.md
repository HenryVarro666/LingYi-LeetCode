---
title: "2040. 两个有序数组的第K小乘积"
aliases: ["yiduobo的每日leetcode 2040.两个有序数组的第K小乘积"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/509869977"
zhihu_id: "509869977"
zhihu_title: "yiduobo的每日leetcode 2040.两个有序数组的第K小乘积"
question_id: "2040"
question: "两个有序数组的第 K 小乘积"
problem_url: "https://leetcode.cn/problems/kth-smallest-product-of-two-sorted-arrays/"
difficulty: "Hard"
rating: 2518
created: "2022-05-05T23:24:54+08:00"
updated: "2022-05-05T23:24:54+08:00"
upvotes: 0
comments: 0
---

# 2040. 两个有序数组的第K小乘积

> **[yiduobo的每日leetcode 2040.两个有序数组的第K小乘积](https://zhuanlan.zhihu.com/p/509869977) · 知乎 · 2022-05-05 · 赞同 0**
> 力扣：[2040. 两个有序数组的第 K 小乘积](https://leetcode.cn/problems/kth-smallest-product-of-two-sorted-arrays/) · Hard · 灵茶山艾府：[第 k 小/大问题的通用转换方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2040.两个有序数组的第K小乘积

[力扣](https://leetcode-cn.com/problems/kth-smallest-product-of-two-sorted-arrays/)

题目相当于给出了一个矩阵，需要找到其中第k小的值。本题与之前一题有点像，不过有所区别的是，本题由于有负数的存在，因此给出的矩阵是局部单调的，从整体上来说不太好利用这个单调性来求解。

另一方面，本题的结果显然是符合二分性质的，那么可以考虑二分答案然后进行检测。

虽然题目给出的矩阵只是局部单调的，但是对于矩阵中的每一行或者每一列，都是由单调性质的。在这里以行来说明。设nums1的长度为n，nums2的长度为m，对于第i行，这一行中的数分别是

x[0] \= nums1[i - 1] \* nums2[0]

x[1] \= nums1[i - 1] \* nums2[1]

...

x[m - 1] \= nums1[i - 1] \* nums2[m - 1]

在这里nums2满足nums2[0] \<\= nums2[1] \<\= ... \<\= nums2[m - 1]

那么对于nums1[i - 1]：

1、当nums1[i - 1] \< 0时，x[0] >\= x[1] >\= ... >\= x[m - 1]

2、当nums2[i - 1] \= 0时，全部的x都是0

3、当nums2[i - 1] > 0时，x[0] \<\= x[1] \<\= ... \<\= x[m - 1]

可以发现，每一行依然是单调的，那么对于当前二分到的结果mid，可以在行中再次进行二分，找出当前行中有多少个数小于等于mid。遍历每一行，都通过二分法找出当前行有多少个数小于等于mid，累加起来就可以直到整个矩阵中有多少个数小于等于mid，进而调整二分答案的上下界了。当然，如果碰到全0的行，则可以直接判断省去二分的时间。

如果枚举行，最终的时间复杂度O(nlogm \* logC)，而如果枚举列，最终的时间复杂度是O(mlogn \* logC)，那么在这里显然应该根据m和n的大小决定枚举那个数组，然后在哪个数组中进行二分。

在这里需要注意的是，在单调不增和单调不减的数组中进行二分，二分的中间点以及上下界的调整方式都略有不同，这个跟个人实现的习惯有关系，不过简单总结就是：

1、调整边界时需要考虑当前二分要找的是什么，从而决定边界调整时是否需要将mid包含进来或者排除在外

2、二分选择mid时需要注意，是否可能出现边界调整时包含了mid，但是mid可能恰好等于边界的情况。举个最简单的例子，l \= 0，r \= 1时进行二分，此时如果mid选择的是0，且最终调整时将l调整为mid，那么就会出现mid和l一直都等于0的情况，导致死循环的出现

另外，python这个语言最好还是用它提供的方法和数据结构，自己手动实现的二分比bisect真的慢太多了。

最后附上python代码：

```python
class Solution(object):
    def kthSmallestProduct(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: int
        """

        if len(nums1) > len(nums2):
            ma = nums1
            mi = nums2
        else:
            ma = nums2
            mi = nums1

        def cnt(x, multi, nums):
            if multi < 0:
                if x >= multi * nums[0]:
                    return len(nums)
                else:
                    l = 0
                    r = len(nums) - 1
                    while l < r:
                        mid = (l + r + 1) >> 1
                        if x < multi * nums[mid]:
                            l = mid
                        else:
                            r = mid - 1
                    return len(nums) - (l + 1)
            
            elif multi > 0:
                if x >= multi * nums[-1]:
                    return len(nums)
                else:
                    l = 0
                    r = len(nums) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if x >= multi * nums[mid]:
                            l = mid + 1
                        else:
                            r = mid
                    return l

            else:
                if x >= 0:
                    return len(nums)
                else:
                    return 0

        l = -(10**10)
        r = 10**10

        while l < r:
            mid = (l + r) >> 1
            now = 0
            for num in mi:
                now += cnt(mid, num, ma)

            if now < k:
                l = mid + 1
            else:
                r = mid
        
        return l
```
