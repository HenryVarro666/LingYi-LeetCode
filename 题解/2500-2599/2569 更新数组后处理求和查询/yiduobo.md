---
title: "2569. 更新数组后处理求和查询"
aliases: ["yiduobo的每日leetcode 2569.更新数组后处理求和查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641284037"
zhihu_id: "641284037"
zhihu_title: "yiduobo的每日leetcode 2569.更新数组后处理求和查询"
question_id: "2569"
question: "更新数组后处理求和查询"
problem_url: "https://leetcode.cn/problems/handling-sum-queries-after-update/"
difficulty: "Hard"
rating: 2398
created: "2023-07-04T01:10:14+08:00"
updated: "2023-07-04T01:10:14+08:00"
upvotes: 0
comments: 0
---

# 2569. 更新数组后处理求和查询

> **[yiduobo的每日leetcode 2569.更新数组后处理求和查询](https://zhuanlan.zhihu.com/p/641284037) · 知乎 · 2023-07-04 · 赞同 0**
> 力扣：[2569. 更新数组后处理求和查询](https://leetcode.cn/problems/handling-sum-queries-after-update/) · Hard · 灵茶山艾府：[【模板】Lazy 线段树（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2569.更新数组后处理求和查询

[力扣](https://leetcode.cn/problems/handling-sum-queries-after-update/)

题目中有三种操作，不过第三种操作是求nums2的和。如果使用一个变量s维护nums2的和的话，就可以在O(1)的时间内处理第三种操作了。而对于第二种操作而言，就相当于将s加上k个p，这里的k为nums1中1的数量。换言之，本题实际上需要考虑的问题就是如何翻转数组的某个区间，并对数组求和。

由于是翻转操作，在这里就不太适合适用前缀和来替代区间和了，只能老老实实用线段树来进行求解。题目中只有区间翻转这一种操作，不过还有一个求和的需求，因此还需要额外维护区间和，那么就只需在基础的线段树上增加区间翻转标记数组以及区间和数组，使用懒更新的做法来进行区间翻转即可。

所谓懒更新，指的是对于区间操作，若操作的区间与当前树节点覆盖的区间一致，那么就给这个节点打上某种标记，表示该区间需要更新，但是并不继续往下更新左右子区间，而是等到之后的某次子区间更新时，先将这个标记下放，然后再更新这次需要更新的区间。

最后附上python代码：

```python
class Solution(object):
    def handleQuery(self, nums1, nums2, queries):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums1)
        v = [0] * (n * 4)
        rev = [False] * (n * 4)
        s = sum(nums2)

        def reverse(now, left, right, i, j):
            if left == right:
                v[now] = 1 - v[now]
                return
            
            if left == i and right == j:
                rev[now] = not rev[now]
                v[now] = right - left + 1 - v[now]
                return
            
            mid = (left + right) >> 1
            if rev[now]:
                reverse(now + now + 1, left, mid, left, mid)
                reverse(now + now + 2, mid + 1, right, mid + 1, right)
                rev[now] = False
            
            if j <= mid:
                reverse(now + now + 1, left, mid, i, j)
            elif i > mid:
                reverse(now + now + 2, mid + 1, right, i, j)
            else:
                reverse(now + now + 1, left, mid, i, mid)
                reverse(now + now + 2, mid + 1, right, mid + 1, j)
            
            v[now] = v[now + now + 1] + v[now + now + 2]

        for index in range(n):
            if nums1[index] == 1:
                reverse(0, 0, n - 1, index, index)

        res = []
        for q in queries:
            if q[0] == 1:
                reverse(0, 0, n - 1, q[1], q[2])
            elif q[0] == 2:
                s += v[0] * q[1]
            else:
                res.append(s)
        
        return res
```
