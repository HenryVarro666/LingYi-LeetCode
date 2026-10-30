---
title: "3724. 转换数组的最少操作次数"
aliases: ["yiduobo的每日leetcode 3724.转换数组的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965847255362834966"
zhihu_id: "1965847255362834966"
zhihu_title: "yiduobo的每日leetcode 3724.转换数组的最少操作次数"
question_id: "3724"
question: "转换数组的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-transform-array/"
difficulty: "Medium"
rating: 1790
created: "2025-10-26T18:41:00+08:00"
updated: "2025-10-26T18:41:01+08:00"
upvotes: 1
comments: 0
---

# 3724. 转换数组的最少操作次数

> **[yiduobo的每日leetcode 3724.转换数组的最少操作次数](https://zhuanlan.zhihu.com/p/1965847255362834966) · 知乎 · 2025-10-26 · 赞同 1**
> 力扣：[3724. 转换数组的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-transform-array/) · Medium · 灵茶山艾府：[贪心 + 分类讨论，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3724.转换数组的最少操作次数

[3724. 转换数组的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-transform-array/description/)

题目给出两个整数数组，第一个数组nums1的长度为n，第二个数组nums2的长度为n + 1。

现在要求使用最少的操作次数将nums1转换为nums2。每次操作，需要选择一个下标index，然后选择以下三项其中之一：

1、将nums1[index]添加1

2、将nums1[index]减去1

3、将nums1[index]添加到nums1的末尾

问至少要多少次操作才能将nums1转换为nums2。

首先可以明确的是，对于0到n - 1之间的下标index，进行操作的次数是固定好了的，即nums1与nums2在对应位置上元素之差的绝对值，因此在这里主要需要讨论的就是如何高效得到nums2[-1]。

对于下标为index的元素nums1[index]，如果在将其变换为nums2[index]的过程中恰好经过了nums2[-1]，那么只需在边长nums2[-1]的时刻将其复制到数组末尾就行了，也就是说对于这种情况没有额外的开销；反之，则应该在nums1[index]在最接近nums2[-1]的那一刻将其复制到数组末尾，然后再调整数组末尾的这个元素。具体来说，就是：

1、当nums1[index] \<\= nums2[-1] \<\= nums2[index]，或者nums1[index] >\= nums2[-1] >\= nums2[index]时，将nums1[index]变换为nums2[index]必然会经过nums2[-1]，只需在经过的时刻将其复制到数组末尾就行了，无需进行额外的调整

2、当max(nums1[index], nums2[index]) \< nums2[-1]时，应该在nums1[index]处于这个最大值时就将其复制到数组末尾，还需要额外的nums2[-1] - max(nums1[index], nums2[index])次调整

3、当min(nums1[index], nums2[index]) > nums2[-1]时，则应该在nums1[index]处于这个最小值时就将其复制到数组末尾，还需要额外的min(nums1[index], nums2[index]) - nums2[-1]次调整

根据上面的结论，就只需要一趟遍历，一边累加每个位置上变换所需的操作次数，一边记录将当前位置上的元素变为nums2[-1]所需的额外调整次数mi。遍历完成后，将所有位置上变换所需的操作次数之和，加上mi，再加上1记为最终答案。其中1是复制的那一次操作开销。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        
        res = 0
        n = len(nums1)
        mi = None
        for index in range(n):
            res += abs(nums1[index] - nums2[index])
            if nums1[index] <= nums2[-1] <= nums2[index] or nums1[index] >= nums2[-1] >= nums2[index]:
                cost = 0
            elif nums2[-1] >= max(nums1[index], nums2[index]):
                cost = nums2[-1] - max(nums1[index], nums2[index])
            else:
                cost = min(nums1[index], nums2[index]) - nums2[-1]
            
            if mi is None or mi > cost:
                mi = cost
        
        return res + mi + 1
```
