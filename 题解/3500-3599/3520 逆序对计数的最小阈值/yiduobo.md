---
title: "3520. 逆序对计数的最小阈值"
aliases: ["yiduobo的每日leetcode 3520.逆序对计数的最小阈值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902558535197389698"
zhihu_id: "1902558535197389698"
zhihu_title: "yiduobo的每日leetcode 3520.逆序对计数的最小阈值"
question_id: "3520"
question: "逆序对计数的最小阈值"
problem_url: "https://leetcode.cn/problems/minimum-threshold-for-inversion-pairs-count/"
created: "2025-05-09T22:06:59+08:00"
updated: "2025-05-09T22:06:59+08:00"
upvotes: 1
comments: 0
---

# 3520. 逆序对计数的最小阈值

> **[yiduobo的每日leetcode 3520.逆序对计数的最小阈值](https://zhuanlan.zhihu.com/p/1902558535197389698) · 知乎 · 2025-05-09 · 赞同 1**
> 力扣：[3520. 逆序对计数的最小阈值](https://leetcode.cn/problems/minimum-threshold-for-inversion-pairs-count/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3520.逆序对计数的最小阈值

[3520. 逆序对计数的最小阈值 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-threshold-for-inversion-pairs-count/description/)

题目给出一个整数数组nums以及一个整数k，阈值为x的逆序对是一组下标对(i, j)，需要满足i \< j，且0 \< nums[i] - nums[j] \<\= x。

现在要求找出最小的min_threshold，使得nums中至少有k组阈值为min_threshold的逆序对。若不存在合法的min_threshold，则返回-1。

首先可以明确的是，若min_threshold越小，那么阈值为min_threshold的逆序对就越少，因此在这里可以二分答案。二分的下界自然是1，而上界则可以设置为ma \= max(nums) - min(nums)，不过在这里为了处理无解的情况，可以将上界设置为ma + 1。

接下来对于当前二分到的阈值threshold，需要检测nums中是否存在至少k组阈值为threshold的逆序对。对于逆序对的求解，可以使用经典的分治法，利用归并排序，在排序过程中检测逆序对的数量。

具体来说，对于计算arr中left到right这一段中的阈值为threshold的逆序对数量：

1、若left \= right：

说明仅有arr[left]这一个元素，不需要进行排序，逆序对的数量也为0

2、若left \< right：

此时则可以先递归求解left到mid以及mid + 1到right。递归求解的过程中不仅需要对子区间排序，还需要计算其中的阈值为threshold的逆序对。接下来对于已经排序好到left到mid以及mid + 1到right这两段，需要执行二路归并。使用i和j分别从left和mid开始向后遍历，对比arr[i]和arr[j]的大小关系。若前者较大，说明i到mid之间的所有元素都大于arr[j]，一共可以形成mid - i + 1组逆序对。不过在这里还有一个threshold的限制需要处理。注意到i到mid这一段是单调递增的，因此可以再使用一个变量p记录最小的满足arr[p] - arr[j] > threshold的下标，那么随着j的向后移动，p也会跟着向后移动，同时满足限制的逆序对数目就是p - i。

在计算逆序对时不要忘了还要执行常规的二路归并。

另外在具体实现上，若某一时刻逆序对的数量已经大于等于k，就不需要进行剩下的计算，直接返回结果然后修正二分的边界即可。

最后附上python代码：

```python
class Solution(object):
    def minThreshold(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        ma = max(nums) - min(nums)
        left = 1
        right = ma + 1

        def calc(arr, left, right, threshold):
            if left == right:
                return 0

            tot = 0
            mid = (left + right) // 2
            tot += calc(arr, left, mid, threshold)
            if tot >= k:
                return tot
            tot += calc(arr, mid + 1, right, threshold)
            if tot >= k:
                return tot

            i = left
            j = mid + 1
            p = 0
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1 or (j <= right and arr[i] > arr[j]):
                    if p < i:
                        p = i
                    while p <= mid and arr[p] - arr[j] <= threshold:
                        p += 1

                    tot += p - i
                    if tot >= k:
                        return tot
                    tmp.append(arr[j])
                    j += 1
                else:
                    tmp.append(arr[i])
                    i += 1

            for index, v in enumerate(tmp):
                arr[index + left] = v

            return tot

        while left < right:
            mid = (left + right) // 2
            arr = nums[:]
            if calc(arr, 0, len(nums) - 1, mid) >= k:
                right = mid
            else:
                left = mid + 1
        
        if left == ma + 1:
            return -1
        return left
```
