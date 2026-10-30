---
title: "2407. 最长递增子序列"
aliases: ["yiduobo的每日leetcode 2407.最长递增子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/四-经典线性-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568079930"
zhihu_id: "568079930"
zhihu_title: "yiduobo的每日leetcode 2407.最长递增子序列"
question_id: "2407"
question: "最长递增子序列 II"
problem_url: "https://leetcode.cn/problems/longest-increasing-subsequence-ii/"
difficulty: "Hard"
rating: 2280
created: "2022-09-25T23:06:49+08:00"
updated: "2022-09-25T23:06:49+08:00"
upvotes: 0
comments: 0
---

# 2407. 最长递增子序列

> **[yiduobo的每日leetcode 2407.最长递增子序列](https://zhuanlan.zhihu.com/p/568079930) · 知乎 · 2022-09-25 · 赞同 0**
> 力扣：[2407. 最长递增子序列 II](https://leetcode.cn/problems/longest-increasing-subsequence-ii/) · Hard · 灵茶山艾府：[线段树优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2407.最长递增子序列

[力扣](https://leetcode.cn/problems/longest-increasing-subsequence-ii/)

经典动态规划问题的变形，最常规的O(n^2)的动态规划算法依然可以得到正确的答案，但是由于数据规模较大，时间复杂度上存在一些问题。而对于经典的贪心加二分的优化，因为有子序列中相邻元素间的差小于等于k这个限制条件，对于本题就不再适用了。

注意到原数组中的每个数都不超过10^5，那么就可以换一种状态表示，令f[i]表示以数字i为结尾的最长上升子序列的长度。接下来同样是一趟遍历，对于当前遍历到的值num，就有

f[num] \= max(f[num - 1], f[num - 2], ..., f[num - k]) + 1

这是一个非常典型的动态区间最大值问题，而且是单点更新加上区间求值，非常适合适用线段树来进行优化。于是在这里可以改为用线段树来维护这个f数组，每一轮都通过线段树取的f[num - 1]到f[num - k]这个区间中的最大值，利用这个最大值更新f[num]以及答案即可。

关于线段树的简单介绍可以参考之前的699题，在这里就不展开了。

[yiduobo：yiduobo的每日leetcode 699.掉落的方块](https://zhuanlan.zhihu.com/p/316523832)

最后附上python代码：

```python
class Solution(object):
    def lengthOfLIS(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        max_n = max(nums)
        f = [0] * (max_n * 4)

        def find(f, p, l, r, left, right):
            if l == left and r == right:
                return f[p]
            else:
                mid = (l + r) >> 1
                if right <= mid:
                    return find(f, p + p + 1, l, mid, left, right)
                elif left > mid:
                    return find(f, p + p + 2, mid + 1, r, left, right)
                else:
                    return max(find(f, p + p + 1, l, mid, left, mid), find(f, p + p + 2, mid + 1, r, mid + 1, right))
        
        def insert(f, p, l, r, num, now):
            f[p] = max(f[p], now)
            if l < r:
                mid = (l + r) >> 1
                if num <= mid:
                    insert(f, p + p + 1, l, mid, num, now)
                else:
                    insert(f, p + p + 2, mid + 1, r, num, now)

        res = 0
        for num in nums:
            if num == 1:
                now = 1
            else:
                left = max(1, num - k)
                right = num - 1
                now = find(f, 0, 1, max_n, left, right) + 1
            
            res = max(res, now)
            insert(f, 0, 1, max_n, num, now)

        return res
```
