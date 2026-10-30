---
title: "2653. 滑动子数组的美丽值"
aliases: ["yiduobo的每日leetcode 2653.滑动子数组的美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/counting", "leetcode/enumeration", "leetcode/ordered-set", "leetcode/sliding-window", "leetcode/bao-li", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/常用数据结构/五-堆-优先队列", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647641913"
zhihu_id: "647641913"
zhihu_title: "yiduobo的每日leetcode 2653.滑动子数组的美丽值"
question_id: "2653"
question: "滑动子数组的美丽值"
problem_url: "https://leetcode.cn/problems/sliding-subarray-beauty/"
difficulty: "Medium"
rating: 1786
created: "2023-08-03T02:36:33+08:00"
updated: "2023-08-03T02:36:33+08:00"
upvotes: 0
comments: 0
---

# 2653. 滑动子数组的美丽值

> **[yiduobo的每日leetcode 2653.滑动子数组的美丽值](https://zhuanlan.zhihu.com/p/647641913) · 知乎 · 2023-08-03 · 赞同 0**
> 力扣：[2653. 滑动子数组的美丽值](https://leetcode.cn/problems/sliding-subarray-beauty/) · Medium · 灵茶山艾府：[滑动窗口+暴力枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2653.滑动子数组的美丽值

[力扣](https://leetcode.cn/problems/sliding-subarray-beauty/)

题目给出一个数组，要求找出所有长度为k的子数组中的第x小值。

对于长度为k的子数组，自然是使用一个长度为k的滑动窗口从左向右滑动，期间就会经过所有长度为k的子数组。现在的问题如果高效计算窗口在滑动时这个第x小值的变化。

一种可以的处理方法是维护一个大小为x以及一个大小为k - x的堆，然后在窗口滑动时利用这两个堆来计算出第x小的值，具体实现时相对复杂。

另外注意到本题nums的取值范围在-50到50之间，因此很自然想到利用数组下标来储存窗口内每个数出现的次数，然后计算次数的前缀和就能找到第x小的数。不过就理论上来说，直接暴力计算依然会超时。

我在这里选择的是树状数组加二分的处理方法，利用树状数组记录当前窗口内小于等于某个值的数字的个数，那么这个个数随着数值的增大也是单调递增的，因此在这里就可以通过二分法加树状数组来替代暴力枚举。

最后附上python代码：

```python
class Solution(object):
    def getSubarrayBeauty(self, nums, k, x):
        """
        :type nums: List[int]
        :type k: int
        :type x: int
        :rtype: List[int]
        """

        res = [0]
        f = [0] * 102

        def add(index, delta):
            while index <= 101:
                f[index] += delta
                index += index & -index
        
        def get():
            left = 1
            right = 101
            while left < right:
                mid = (left + right) >> 1

                index = mid
                s = 0
                while index > 0:
                    s += f[index]
                    index -= index & -index
                
                if s >= x:
                    right = mid
                else:
                    left = mid + 1
            
            return left

        for v in nums[:k]:
            add(v + 51, 1)

        res = [min(get() - 51, 0)]
        for index, v in enumerate(nums[k:]):
            add(v + 51, 1)
            add(nums[index] + 51, -1)
            res.append(min(get() - 51, 0))
        
        return res
```
