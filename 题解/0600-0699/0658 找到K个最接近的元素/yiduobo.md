---
title: "658. 找到K个最接近的元素"
aliases: ["yiduobo的每日leetcode 658.找到K个最接近的元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/284072485"
zhihu_id: "284072485"
zhihu_title: "yiduobo的每日leetcode 658.找到K个最接近的元素"
question_id: "658"
question: "找到K个最接近的元素"
problem_url: "https://leetcode.cn/problems/find-k-closest-elements/"
created: "2020-11-10T22:40:56+08:00"
updated: "2020-11-10T22:40:56+08:00"
upvotes: 0
comments: 0
---

# 658. 找到K个最接近的元素

> **[yiduobo的每日leetcode 658.找到K个最接近的元素](https://zhuanlan.zhihu.com/p/284072485) · 知乎 · 2020-11-10 · 赞同 0**
> 力扣：[658. 找到K个最接近的元素](https://leetcode.cn/problems/find-k-closest-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

658.找到K个最接近的元素

[力扣](https://leetcode-cn.com/problems/find-k-closest-elements/)

首先，可以想到的最直观的做法就是先将arr中的每个数都减去x，然后按绝对值从小到大进行排序，取出前top k个，然后加上x之后按符号放入两个数组最后再合并起来。

当然，由于是取top k个，因此也可以使用堆来完成这个操作。

以上两个做法的时间复杂度分别是O(nlogn)和O(nlogk)，但是由于这两种做法都没有将arr本身是有序的利用起来，因此都不是最优的做法。

由于arr有序，因此最终的答案必然是arr中连续的一段。在这里可能有两种特殊情况，即x \<\= arr[0]或者x >\= arr[-1]。对于这两种情况，答案显然就是arr[:k]以及arr[len(arr) - k:]，无需进行后续操作了。若不属于上面这两种情况，那么我们可以通过二分查找很快定位到最小的且大于等于x的数的位置p，进一步得到q \= p - 1就是最大的且小于x的数的位置。

接下来，从p和q开始往两侧扩展。若arr[q] - x的绝对值小于等于arr[p] - x的绝对值，那么我们就将q往下扩展，否则将p往上扩展，直到p - q - 1 \= k。

这个做法一趟二分查找的时间复杂度位O(logn)，而找到最后的k个数的时间复杂度是O(k)，因此最终的时间复杂度就是O(k + logn)。

最后附上python代码：

```python
class Solution(object):
    def findClosestElements(self, arr, k, x):
        """
        :type arr: List[int]
        :type k: int
        :type x: int
        :rtype: List[int]
        """

        if x <= arr[0]:
            return arr[:k]
        
        if x >= arr[-1]:
            return arr[len(arr) - k:]

        l = 0
        r = len(arr) - 1
        while l < r:
            mid = (l + r) >> 1
            if arr[mid] >= x:
                r = mid
            else:
                l = mid + 1
        
        r = l
        l -= 1
        while k > 0:
            if l < 0:
                r += 1
            elif r == len(arr) or abs(arr[l] - x) <= abs(arr[r] - x):
                l -= 1
            else:
                r += 1
            k -= 1

        return arr[l + 1 : r]
```
