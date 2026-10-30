---
title: "4. 寻找两个有序数组的中位数"
aliases: ["yiduobo的每日leetcode 4. 寻找两个有序数组的中位数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/binary-search", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/四-其他", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/112789053"
zhihu_id: "112789053"
zhihu_title: "yiduobo的每日leetcode 4. 寻找两个有序数组的中位数"
question_id: "4"
question: "寻找两个正序数组的中位数"
problem_url: "https://leetcode.cn/problems/median-of-two-sorted-arrays/"
difficulty: "Hard"
created: "2020-03-12T23:25:22+08:00"
updated: "2020-03-12T23:25:22+08:00"
upvotes: 1
comments: 0
---

# 4. 寻找两个有序数组的中位数

> **[yiduobo的每日leetcode 4. 寻找两个有序数组的中位数](https://zhuanlan.zhihu.com/p/112789053) · 知乎 · 2020-03-12 · 赞同 1**
> 力扣：[4. 寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) · Hard · 灵茶山艾府：[【图解】循序渐进：从排序到双指针到二分（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

4.寻找两个有序数组的中位数<https://leetcode-cn.com/problems/median-of-two-sorted-arrays/>

对于这两个有序数组a、b，长度分别为m和n，

令k \= (m + n + 1) / 2

若m + n为奇数，那么就是求a和b中第k小的数是什么。

若m + n为偶数，那么就是求a和b中第k小和第k + 1小的数是什么。

先看看如何求解两个数组中第k小的数。

对于a，b两个有序数组，我们设mid \= k / 2，那么有下面几种情况：

**1、a为空：**

取b[k - 1]即可。注意这里的数组下标是从0开始的，因此第k个数的下标是k - 1。

**2、不符合情况1且b为空：**

同上，取a[k - 1]即可。

**3、不符合情况1、2且k \= 1：**

这种情况下直接比较a[0]与b[0]的大小即可。

**4、不符合以上三点，且a的长度不足mid，即len(a) \< mid：**

此时，考虑b[0]到b[mid]。即使在最极端的情况下，即b[0] > a[-1]，此时的b[mid]在两个数组中依然是len(a) + mid小的，而len(a) \< mid, 因此len(a) + mid \< mid + mid \<\= k，即b[mid]不符合要求，自然b[0]到b[mid]都不符合要求。在这种情况下，我们舍去b[0]到b[mid]，得到newb，然后从a和newb中找第k - mid小的即可。

**5、不符合以上四点，且b的长度不足mid，即len(b) \< mid：**

同上，此时舍去a[0]到a[mid]，得到newa，然后从newa和b中找第k - mid小的。

**6、不符合以上5点：**

在这种情况下，比较a[mid]与b[mid]的大小。

若a[mid] \< b[mid]，即使在最极端的情况下，即b[mid - 1] \< a[0]，那么此时的a[mid]在两个数组中依然是mid - 1 + mid小的，而mid - 1 + mid \< mid + mid \<\= k，即a[mid]不符合要求，自然a[0]到a[mid]都不符合要求。此时，我们舍去a[0]到a[mid]，得到newa，然后从newa和b中找第k - mid小的即可。

若a[mid] >\= b[mid]，则舍去b[0]到b[mid]，得到newb，然后从a和newb中找第k - mid小的。

可以发现，以上几种情况，前三种将直接得到答案，后三种每次k都将变成k - mid，即缩小一半的规模。因此最终时间复杂度为O(log(m + n))，符合题目要求。

注意到每次a和b的迭代实际上都是舍去了靠前的元素，因此可以通过维护一个数组的左边界来表示数组舍去元素的过程，而不用每次修改数组。

此时我们已经得到了第k小的数，那么对于m + n为偶数的情况，还需要求解第k + 1小的数。对于第k + 1小的数，我们可以理解为找到第k小的数之后，舍去a，b中前k小的数，然后从新得到的newa和newb中再找最小的数。此时套用前三种情况的做法即可。

最后附上python代码，其中m，n，k，mid与题解中含义相同，left1和left2分别为两个数组的左边界，left1和left2的增长表示舍去了数组最小的那几个元素。

```python
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        
        m = len(nums1)
        n = len(nums2)
        k = (m + n + 1) / 2
        
        left1 = left2 = 0

        while True:
            if left1 == m:
                res = nums2[left2 + k - 1]
                left2 += k
                break
            elif left2 == n:
                res = nums1[left1 + k - 1]
                left1 += k
                break
            elif k == 1:
                if nums1[left1] > nums2[left2]:
                    res = nums2[left2]
                    left2 += 1
                    break
                else:
                    res = nums1[left1]
                    left1 += 1
                    break
            else:
                mid = k / 2
                if left1 + mid - 1 >= m:
                    left2 += mid
                elif left2 + mid - 1 >= n:
                    left1 += mid
                elif nums1[left1 + mid - 1] < nums2[left2 + mid - 1]:
                    left1 += mid
                else:
                    left2 += mid
                
                k -= mid

        if (m + n) % 2 == 1:
            return res * 1.0
        else:
            if left1 == m:
                return (res + nums2[left2]) * 0.5
            elif left2 == n:
                return (res + nums1[left1]) * 0.5
            else:
                return (res + min(nums1[left1], nums2[left2])) * 0.5
```
