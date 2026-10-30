---
title: "3640. 三段式数组II"
aliases: ["yiduobo的每日leetcode 3640.三段式数组II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/simulation", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/六-分组循环", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947670828096401895"
zhihu_id: "1947670828096401895"
zhihu_title: "yiduobo的每日leetcode 3640.三段式数组II"
question_id: "3640"
question: "三段式数组 II"
problem_url: "https://leetcode.cn/problems/trionic-array-ii/"
difficulty: "Hard"
rating: 2278
created: "2025-09-06T15:40:08+08:00"
updated: "2025-09-06T15:40:09+08:00"
upvotes: 0
comments: 0
---

# 3640. 三段式数组II

> **[yiduobo的每日leetcode 3640.三段式数组II](https://zhuanlan.zhihu.com/p/1947670828096401895) · 知乎 · 2025-09-06 · 赞同 0**
> 力扣：[3640. 三段式数组 II](https://leetcode.cn/problems/trionic-array-ii/) · Hard · 灵茶山艾府：[两种方法：分组循环 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3640.三段式数组II

[3640. 三段式数组 II - 力扣（LeetCode）](https://leetcode.cn/problems/trionic-array-ii/description/)

题目给出一个长度为n的整数数组nums。

若nums中的某个连续数组nums[l: r + 1]，满足0 \<\= l \< r \< n，同时存在下标p和q满足l \< p \< q \< r，且nums[l: p + 1]单调递增，nums[p: q + 1]单调递减，nums[q: r + 1]单调递增，那么就称这个子数组为三段式子数组。

现在要求找出nums中所有三段式子数组中和最大的那个，并返回这个最大的和。

对于一个三段式子数组，其正中间p到q的单调递减的这一段必然是nums中一个完整的单调递减子数组，只有这样才可能在满足p到q单调递减的前提下，使得l到p以及q到r这一段单调递增。基于这一点，就可以一趟遍历，找出nums中所有单调递减的子数组，然后以这些子数组作为三段式子数组中间这一段，向两侧扩展找出完整的三段式子数组。

对于已经确定了中间这一段，也就是固定了p和q的三段式子数组，接下来要考虑如何向两侧扩展。

首先考虑向左扩展。由于必须保证左侧是单调递增的，那么在这里就要求至少要满足nums[p - 1]小于nums[p]。而为了使得子数组之和最大，那么就应该从nums[p - 2]开始向左扩展，将所有满足nums[index] \< nums[index + 1]，且nums[index] > 0的元素加入到子数组中，理由也很简单，尽量加入正数才能使得子数组之和最大。

接下来考虑向右扩展。同样的，至少需要满足nums[p + 1]大于nums[p]。由于右半边是单调递增的，因此在这里要么选择纳入右侧所有单调递增的部分，要么只纳入nums[p + 1]，理由是若nums[p + 1]大于等于0，此时就应该尽量多的纳入后续单调递增的元素，因为这些数都是正的，能使得子数组之和最大；反之，若nums[p + 1]小于0，那么随着后续元素的单调递增，右侧递增这一段的子数组和就会经历一个递减再递增的过程，也就是一个v字形的转折，在这个v字形中最大的两点显然就是端点上的两点，也就是只加入nums[p + 1]，或者全部加入。

到了这里，就可以将中间这一段元素之和，加上扩展出去的左右两段元素之和，得到这个三段式数组之和。取其中的最大值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumTrionic(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        p = 0
        res = None
        while p < len(nums):
            while p + 1 < len(nums) and nums[p + 1] >= nums[p]:
                p += 1
            
            if p + 1 == len(nums):
                break
            
            q = p + 1
            middle = nums[p] + nums[q]
            while q + 1 < len(nums) and nums[q + 1] < nums[q]:
                q += 1
                middle += nums[q]

            if q + 1 == len(nums):
                break

            if p == 0 or nums[p - 1] == nums[p]:
                p = q
                continue
            
            left = nums[p - 1]
            p -= 1
            while p > 0 and nums[p - 1] < nums[p] and nums[p - 1] > 0:
                left += nums[p - 1]
                p -= 1

            if nums[q + 1] == nums[q]:
                p = q + 1
                continue
            
            right_one = nums[q + 1]
            right = nums[q + 1]
            q += 1
            while q + 1 < len(nums) and nums[q + 1] > nums[q]:
                q += 1
                right += nums[q]

            tot = left + middle + max(right, right_one)
            if res is None or res < tot:
                res = tot
            p = q
        
        return res
```
