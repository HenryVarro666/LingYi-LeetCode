---
title: "3768. 固定长度子数组中的最小逆序对数目"
aliases: ["yiduobo的每日leetcode 3768.固定长度子数组中的最小逆序对数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/ordered-set", "leetcode/sorting", "leetcode/sliding-window", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981126576650334502"
zhihu_id: "1981126576650334502"
zhihu_title: "yiduobo的每日leetcode 3768.固定长度子数组中的最小逆序对数目"
question_id: "3768"
question: "固定长度子数组中的最小逆序对数目"
problem_url: "https://leetcode.cn/problems/minimum-inversion-count-in-subarrays-of-fixed-length/"
difficulty: "Hard"
rating: 2158
created: "2025-12-09T21:05:01+08:00"
updated: "2025-12-09T21:05:03+08:00"
upvotes: 3
comments: 0
---

# 3768. 固定长度子数组中的最小逆序对数目

> **[yiduobo的每日leetcode 3768.固定长度子数组中的最小逆序对数目](https://zhuanlan.zhihu.com/p/1981126576650334502) · 知乎 · 2025-12-09 · 赞同 3**
> 力扣：[3768. 固定长度子数组中的最小逆序对数目](https://leetcode.cn/problems/minimum-inversion-count-in-subarrays-of-fixed-length/) · Hard · 灵茶山艾府：[定长滑窗 + 离散化 + 值域树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3768.固定长度子数组中的最小逆序对数目

<https://leetcode.cn/problems/minimum-inversion-count-in-subarrays-of-fixed-length/description/>

题目给出一个长度为n的整数数组nums，以及一个整数k。其中n不超过10^5，nums中的元素大小不超过10^9。

现在要求对于nums中所有长度为k的子数组，计算子数组中逆序对的数目，并返回这些逆序对数目的最小值。

看到固定长度为k的子数组，很自然就想到滑动窗口，那么不妨设当前窗口的左右边界分别为index以及index + k - 1，其中有v组逆序对，那么当窗口向后滑动时：

- 首先需要计算nums[index]与nums[index + 1: index + k]中的逆序对数目。更进一步的，实际上就是需要计算窗口内小于nums[index]的元素数目，不妨记为cnt。随着nums[index]从窗口中移除，逆序对的数目v应该减去cnt。
- 接下来需要将nums[index]从窗口中移除。
- 然后需要将nums[index + k]加入到窗口中。
- 最后需要计算nums[index + 1: index + k]与nums[index + k]的逆序对数目。更进一步的，实际上就是需要计算窗口内大于nums[index + k]的元素数目，不妨记为cnt。随着nums[index + k]加入到窗口中，逆序对的数目v应该加上cnt。

可以发现，以上步骤实际上就是需要高效求解区间中有多少个元素小于特定值，有多少个元素大于特定值。对于后者，由于区间长度已经固定住了，因此可以通过区间长度减去区间内小于等于特定值的数目计算得到，也就是说，本题上的重点就是计算区间中小于等于特定值的元素数目。

对于这个问题，最方便的处理方法自然是使用平衡树。如果需要手搓的话，使用离散化加树状数组也是可行的处理方法。我在这里采用的是后面这种处理方法。

使用树状数组是很自然的想法，因为只需要将数值视为树状数组的下标，那么树状数组天然就可以计算小于等于特定值的元素数目。而本题中nums的取值范围较大，因此需要先将其中的元素从小到大进行排序，然后将数值映射为序，在这个序的数组上使用树状数组进行求解。

最后附上python代码：

```python
class Solution(object):
    def minInversionCount(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        mapping = {}
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = len(mapping) + 1
        
        nums = [mapping[x] for x in nums]

        def add(x, f, delta):
            while x < len(f):
                f[x] += delta
                x += x & -x
        
        def get(x, f):
            cnt = 0
            while x > 0:
                cnt += f[x]
                x -= x & -x
            return cnt

        f = [0] * (len(mapping) + 1)
        now = 0
        for index in range(k - 1, -1, -1):
            v = nums[index]
            now += get(v - 1, f)
            add(v, f, 1)

        res = now
        for index, v in enumerate(nums[k:]):
            now -= get(nums[index] - 1, f)
            add(nums[index], f, -1)

            now += k - 1 - get(v, f)
            add(v, f, 1)

            res = min(res, now)
        
        return res
```
