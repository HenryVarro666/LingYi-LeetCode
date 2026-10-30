---
title: "3909. 比较双调部分的和"
aliases: ["yiduobo的每日leetcode 3909.比较双调部分的和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032243977571790936"
zhihu_id: "2032243977571790936"
zhihu_title: "yiduobo的每日leetcode 3909.比较双调部分的和"
question_id: "3909"
question: "比较双调部分的和"
problem_url: "https://leetcode.cn/problems/compare-sums-of-bitonic-parts/"
difficulty: "Medium"
created: "2026-04-28T00:23:14+08:00"
updated: "2026-04-28T00:23:15+08:00"
upvotes: 1
comments: 0
---

# 3909. 比较双调部分的和

> **[yiduobo的每日leetcode 3909.比较双调部分的和](https://zhuanlan.zhihu.com/p/2032243977571790936) · 知乎 · 2026-04-28 · 赞同 1**
> 力扣：[3909. 比较双调部分的和](https://leetcode.cn/problems/compare-sums-of-bitonic-parts/) · Medium · 灵茶山艾府：[按题意模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3909.比较双调部分的和

<https://leetcode.cn/problems/compare-sums-of-bitonic-parts/description/>

题目给出一个长度为n的双调数组nums。双调数组指的是存在单个峰值元素，且在这个元素之前单调递增，在这个元素之后单调递减的数组。

现在要求分别计算递增部分与递减部分的元素之和并进行比较，若递增部分的较大，则返回0；若递减部分的较大，则返回1，否则返回-1。

题目要求对比递增部分之和与递减部分之和，那么就可以先计算递增部分之和，再减去递减部分的所有元素，这样一来就得到了递增部分与递减部分和的差，最后判断这个差与0的大小关系即可。

具体来说，初始化递增部分之和s为nums[0]，然后使用一个变量p从0开始向后迭代。若当前的p + 1 \< n，且nums[p + 1] > nums[p]，那么就说明nums[p + 1]也属于递增部分，此时将p加上1，然后将nums[p]累加到s当中。重复此过程直到p来到数组末尾，或者nums[p + 1] \< nums[p]为止。

接下来，数组中剩下的部分就都是属于递减的部分，只需从p开始向后迭代到数组末尾，然后将这些元素的值从s中减去即可。需要注意，峰值由于也需要被减去。

最后附上python代码：

```python
class Solution(object):
    def compareBitonicSums(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        s = nums[0]
        p = 0
        while p + 1 < n and nums[p + 1] > nums[p]:
            p += 1
            s += nums[p]
        
        s -= nums[p]
        while p + 1 < n:
            p += 1
            s -= nums[p]
        
        if s > 0:
            return 0
        elif s < 0:
            return 1
        else:
            return -1
```
