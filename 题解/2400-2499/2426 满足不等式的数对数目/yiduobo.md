---
title: "2426. 满足不等式的数对数目"
aliases: ["yiduobo的每日leetcode 2426.满足不等式的数对数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/binary-search", "leetcode/sorting", "leetcode/shua-ti", "leetcode/ni-xu-dui", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582363825"
zhihu_id: "582363825"
zhihu_title: "yiduobo的每日leetcode 2426.满足不等式的数对数目"
question_id: "2426"
question: "满足不等式的数对数目"
problem_url: "https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/"
difficulty: "Hard"
rating: 2030
created: "2022-11-11T00:40:32+08:00"
updated: "2022-11-11T00:40:32+08:00"
upvotes: 0
comments: 0
---

# 2426. 满足不等式的数对数目

> **[yiduobo的每日leetcode 2426.满足不等式的数对数目](https://zhuanlan.zhihu.com/p/582363825) · 知乎 · 2022-11-11 · 赞同 0**
> 力扣：[2426. 满足不等式的数对数目](https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/) · Hard · 灵茶山艾府：[转换成逆序对模型（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2426.满足不等式的数对数目

[力扣](https://leetcode.cn/problems/number-of-pairs-satisfying-inequality/)

首先观察题目给出的式子。

对于

nums1[i] - nums1[j] \<\= nums2[i] - nums2[j] + diff

常见的做法就是把i和j都并拢，此时就得到了

nums1[i] - nums2[i] \<\= nums1[j] - nums2[j] + diff

可以发现，这个式子两侧都是nums1中的某个数减去nums2中相同下标对应的数，那么就可以先构造数组nums，其中nums[i] \= nums1[i] - nums2[i]，此时问题就变成了给出数组nums，求其中的数对nums[i]和nums[j]，满足i \< j且nums[i] \<\= nums[j] + diff

这是一个经典的问题，可以离散化后使用树状数组计数，也可以使用类似求逆序对的方法，在归并排序的过程中顺便求解。我在这里采用的是后面这种方法。

对于数组区间nums[left]到nums[right]，令mid \= (left + right) / 2，那么在left到right中满足条件的下标对的分布就有三种可能，分别为i \< j \<\= mid、mid + 1 \<\= i \< j、i \<\= mid \< j。

对于这三种情况，前两种可以对应的区间left到mid和mid + 1到right中满足条件的下标对，因此可以递归求解。

对于第三种情况，常规的计算方式依然需要做一些处理，但是如果此时left到mid和mid + 1到right这两个区间内的数都已经从小到大排列好了，那么就可以利用单调性在O(n)的时间内找出所有符合条件的下标对。

具体来说，可以从小到大遍历left到mid来选择当前的i，同时使用一个遍历p记录mid + 1到right中最小的满足nums[j] + diff >\= nums[i]的下标。随着i的增大，其对应的nums[i]也会跟着增大，因此满足条件的最小的j也会逐渐增大，也就是说每一个i对应的p都会比上一个i对应的p更大。有了这个结论，就可以在i向后移动时更新其对应的p，而mid + 1到right之间所有大于等于p的j与当前枚举的i都能组成合法的数对，因此可以使用right - p + 1来更新答案。

那么最后一个问题就是，如何保证两侧都有序。递归求解两侧加上有序，很自然就想到了归并排序，那么在归并排序的基础上执行上面的计数操作就可以得到最终答案了。

最后附上python代码：

```python
class Solution(object):
    def numberOfPairs(self, nums1, nums2, diff):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type diff: int
        :rtype: int
        """

        n = len(nums1)
        nums = [nums1[index] - nums2[index] for index in range(n)]
        
        def merge(left, right):
            if left == right:
                return 0
            
            mid = (left + right) >> 1
            cnt = merge(left, mid) + merge(mid + 1, right)

            p1 = left
            p2 = p = mid + 1
            tmp = []
            while p1 <= mid or p2 <= right:
                if p2 == right + 1 or (p1 != mid + 1 and nums[p1] < nums[p2]):
                    while p <= right and nums[p] + diff < nums[p1]:
                        p += 1
                    cnt += right - p + 1
                    tmp.append(nums[p1])
                    p1 += 1
                else:
                    tmp.append(nums[p2])
                    p2 += 1
            
            for index in range(left, right + 1):
                nums[index] = tmp[index - left]

            return cnt

        return merge(0, n - 1)
```
