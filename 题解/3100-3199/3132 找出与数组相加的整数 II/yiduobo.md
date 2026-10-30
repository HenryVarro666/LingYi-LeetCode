---
title: "3132. 找出与数组相加的整数II"
aliases: ["yiduobo的每日leetcode 3132.找出与数组相加的整数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702404202"
zhihu_id: "702404202"
zhihu_title: "yiduobo的每日leetcode 3132.找出与数组相加的整数II"
question_id: "3132"
question: "找出与数组相加的整数 II"
problem_url: "https://leetcode.cn/problems/find-the-integer-added-to-array-ii/"
difficulty: "Medium"
rating: 1620
created: "2024-06-08T22:10:58+08:00"
updated: "2024-06-08T22:10:58+08:00"
upvotes: 0
comments: 0
---

# 3132. 找出与数组相加的整数II

> **[yiduobo的每日leetcode 3132.找出与数组相加的整数II](https://zhuanlan.zhihu.com/p/702404202) · 知乎 · 2024-06-08 · 赞同 0**
> 力扣：[3132. 找出与数组相加的整数 II](https://leetcode.cn/problems/find-the-integer-added-to-array-ii/) · Medium · 灵茶山艾府：[O(nlogn) 排序+判断子序列（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3132.找出与数组相加的整数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-integer-added-to-array-ii/description/)

题目给出两个整数数组nums1和nums2，其中nums1比nums2多出两个元素。要求从nums1中移除两个元素，然后将其他的元素都加上整数x，使得nums1每种元素出现次数都与nums2中相同，问最小的x是多少。

在确定了nums1中删除的两个元素之后，如果存在合法的x，那么x就必然等于nums2的最小值减去nums1中剩下元素中的最小值。更进一步的，在这里并不需要一开始就确定nums1中删除了哪两个元素，而是只需要直到删除之后的最小值是多少，也就是说这里有三种情况：

1、没有删掉原来的最小值。此时nums1剩下元素中的最小值保持不变。

2、删掉了原来的最小值，但没有删掉原来的次小值。此时nums1剩下元素中的最小值就是原来的次小值。

3、删掉了最小值以及次小值。此时nums1剩下元素中的最小值就是原来的第三小值。

那么在这里就只需要分别检测这三种情况，对于每种情况，先计算出对应的x，然后将nums1中的所有元素都减去x，再检测nums2是否为nums1的子序列即可。对于检测一个数组是否为另一个数组的子序列这个问题，则可以先将两个数组排序，然后一趟遍历尽量匹配就行了。

具体实现上，由于数组中所有元素同时加上x后不影响数组的序，因此可以先将两个数组先从小到大进行排序，那么x的取值就是nums2[0]与nums1[0]、nums1[1]、nums1[2]的差这三者之一，接下来再分别遍历检测是否为子序列即可。

最后附上python代码：

```python
class Solution(object):
    def minimumAddedInteger(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        nums1.sort()
        nums2.sort()
        res = None
        for p, v in enumerate(nums1[:3]):
            diff = nums2[0] - v
            flag = True
            for x in nums2:
                while p < len(nums1) and x - nums1[p] != diff:
                    p += 1
                if p == len(nums1):
                    flag = False
                    break
                
                p += 1
            
            if flag and (res is None or res > diff):
                res = diff
        
        return res
```
