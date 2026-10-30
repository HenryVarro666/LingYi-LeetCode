---
title: "3835. 开销小于等于K的子数组数目"
aliases: ["yiduobo的每日leetcode 3835.开销小于等于K的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2003936432453079170"
zhihu_id: "2003936432453079170"
zhihu_title: "yiduobo的每日leetcode 3835.开销小于等于K的子数组数目"
question_id: "3835"
question: "开销小于等于 K 的子数组数目"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-cost-less-than-or-equal-to-k/"
difficulty: "Medium"
rating: 1759
created: "2026-02-09T21:19:17+08:00"
updated: "2026-02-09T21:19:18+08:00"
upvotes: 1
comments: 0
---

# 3835. 开销小于等于K的子数组数目

> **[yiduobo的每日leetcode 3835.开销小于等于K的子数组数目](https://zhuanlan.zhihu.com/p/2003936432453079170) · 知乎 · 2026-02-09 · 赞同 1**
> 力扣：[3835. 开销小于等于 K 的子数组数目](https://leetcode.cn/problems/count-subarrays-with-cost-less-than-or-equal-to-k/) · Medium · 灵茶山艾府：[O(n) 做法：单调队列 + 越短越合法型滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3835.开销小于等于K的子数组数目

<https://leetcode.cn/problems/count-subarrays-with-cost-less-than-or-equal-to-k/description/>

题目给出一个整数数组nums以及一个整数k。

对于其中的任意子数组nums[left..right]，其开销定义为

cost \= (max(nums[left..right]) - min(nums[left..right])) \* (right - left + 1)

要求找出nums中有多少个开销小于等于k的子数组。

首先观察题目中关于cost的式子。

对于一个固定的left，当right越大时，max(nums[left..right])越大，而min(nums[left.. right])越小，也就是说第一个括号中减法的这一项是随着right的增大而增大的。另一方面，第二个括号中的(right - left + 1)显然是随着right的增大而增大的，也就是说，在left固定时，right越大，对应的cost就越大。同样的，对于一个固定的right，left越大，cost就越小。

基于这一点，就可以通过滑动窗口进行求解。具体来说，对于一个特定的index，当其作为区间的左边界时，不妨设其满足条件的最大右边界为p，那么对于index + 1而言，其对应的右边界p'，就可以在p的基础上不断尝试向后扩展得到。

接下来的问题就是如何高效计算区间内的最大值以及最小值。对于这个问题，可以通过使用堆配合哈希表来实现，也可以通过单调队列来实现，我在这里采用的是后者。

以区间最大值为例。对于区间中的某两个下标p和q，若p \< q且nums[p] \<\= nums[q]，那么在nums[q]加入区间的这一刻，nums[p]就没有必要再保留在区间中了，因为nums[p]必然先于nums[q]从区间中移除，而由于nums[q]的存在，nums[p]也不可能成为区间的最大值，因此在这里没有必要保留nums[p]。

基于这个结论，最终留下来必然是一个单调递减的队列，而对于新来的元素v，则可以从后往前依次对比队尾元素与v的大小，若v更大，则将队尾元素弹出，直到队列为空或者队尾元素大于v为止，接下来将v加入到队尾即可。需要计算最大值时，只需取出队首元素就行了。另外，在本题中随着区间左边界的移动，单调队列的队首可能会过期，因此还需要将过期的队首元素从队列中移除。

到了这里，就得到了一种可行的算法。先初始化最大值和最小值的单调队列ma以及mi为空，同时初始化合法区间右边界为p，然后从左往右遍历区间的左边界index。

对于当前的index，先考察能否将nums[p]加入到区间中，即取nums[p]与ma队首这两者中的较大值作为max(nums[index..p])，取nums[p]与mi队首这两者中的较小值作为min(nums[index..p])，然后计算区间的cost，若其小于等于k，就根据上面关于单调队列的讨论，使用nums[p]更新ma以及mi，重复此过程直到p无法向后移动为止。

接下来，所有右边界在index到p - 1之间的区间都是合法的，一共是p - index个，因此需要将p - index累加到答案中。

最后，若ma或mi的队首元素是nums[index]，还需要将其从ma或者mi中弹出。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        ma = deque()
        mi = deque()

        res = 0
        p = 0
        for index, v in enumerate(nums):
            while p < len(nums):
                x = nums[p]
                if ma:
                    x = max(nums[ma[0]], x)
                
                y = nums[p]
                if mi:
                    y = min(nums[mi[0]], y)
                
                if (x - y) * (p - index + 1) > k:
                    break
                
                while ma and nums[ma[-1]] <= nums[p]:
                    ma.pop()
                ma.append(p)

                while mi and nums[mi[-1]] >= nums[p]:
                    mi.pop()
                mi.append(p)

                p += 1
            
            res += p - index

            if ma and ma[0] == index:
                ma.popleft()
            
            if mi and mi[0] == index:
                mi.popleft()
        
        return res
```
