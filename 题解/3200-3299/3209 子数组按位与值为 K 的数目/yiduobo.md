---
title: "3209. 子数组按位与值为K的数目"
aliases: ["yiduobo的每日leetcode 3209.子数组按位与值为K的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/bit-manipulation", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/sliding-window", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707956850"
zhihu_id: "707956850"
zhihu_title: "yiduobo的每日leetcode 3209.子数组按位与值为K的数目"
question_id: "3209"
question: "子数组按位与值为 K 的数目"
problem_url: "https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/"
difficulty: "Hard"
rating: 2050
created: "2024-07-10T00:15:43+08:00"
updated: "2024-07-10T00:15:43+08:00"
upvotes: 0
comments: 0
---

# 3209. 子数组按位与值为K的数目

> **[yiduobo的每日leetcode 3209.子数组按位与值为K的数目](https://zhuanlan.zhihu.com/p/707956850) · 知乎 · 2024-07-10 · 赞同 0**
> 力扣：[3209. 子数组按位与值为 K 的数目](https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/) · Hard · 灵茶山艾府：[两类方法：LogTrick / 滑动窗口 + 栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3209.子数组按位与为K的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-subarrays-with-and-value-of-k/description/)

题目给出一个整数数组nums以及一个整数k，要求找出nums中存在多少个子数组满足按位与的结果恰好等于k。

根据按位与的性质，参与运算的数越多，按位与的结果就越小，因此在这里就可以固定住子数组的右边界index，那么所有以index为右边界的子数组的按位与结果将会经历小于k、等于k、大于k这三个阶段，此时只需要找出等于k这个阶段对应的最左侧和最右侧的下标left以及right即可。

当然，当nums[index]本来就小于k时，则不会出现等于k和大于k这两个阶段，而当nums[index]大于k时，也不一定会出现小于k以及等于k这两个阶段，但是有一点可以明确的是，虽然index向后移动，对应的left和right也会跟着向后移动，因此可以使用两个变长滑动窗口来分别处理left和right。

不过需要注意的是，窗口内元素计算的是按位与，那么随着left和right的移动，窗口内元素的按位与无法简单运算得到，此时就还需要使用两个数组freq_left和freq_right分别记录两个窗口中各元素在每个二进制位上值为1的数量，当窗口左边界移动时，若移除的元素在d这一位上为0，同时其对应的freq值恰好等于新的窗口长度，那么窗口内元素的按位与结果在d这一位上就会由0变1。

写到这里，突然想起之前好像有道按位与的题变按位或了，不过之前另有一题也用到了相同的处理方法，可以参考

[yiduobo：yiduobo的每日leetcode 3117.划分数组得到最小的值之和](https://zhuanlan.zhihu.com/p/701264461)

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        left_now = None
        right_now = None
        left = None
        right = None
        left_freq = [0] * 30
        right_freq = [0] * 30
        res = 0
        for index, v in enumerate(nums):
            if left_now is None:
                left_now = v
                left = index
                for d in range(30):
                    if v & (1 << d) == (1 << d):
                        left_freq[d] += 1
            
            else:
                left_now &= v
                if right is not None:
                    right_now &= v
                for d in range(30):
                    if v & (1 << d) == (1 << d):
                        left_freq[d] += 1
                        if right is not None:
                            right_freq[d] += 1

                while left_now < k and left < index:
                    x = nums[left]
                    t = 0
                    for d in range(30):
                        if x & (1 << d) == (1 << d):
                            left_freq[d] -= 1
                        elif left_freq[d] == index - left:
                            t |= (1 << d)
                    
                    left_now |= t
                    left += 1
                
            if left_now < k:
                left_now = None
                left = None
                left_freq = [0] * 30
                right_now = None
                right = None
                right_freq = [0] * 30

            elif left_now == k:
                if right is None or right < left:
                    right_now = left_now
                    right_freq = left_freq[:]
                    right = left
                    
                while right < index:
                    x = nums[right]
                    t = 0
                    for d in range(30):
                        if (x & (1 << d) == 0) and right_freq[d] == index - right:
                            t |= (1 << d)
                    
                    if (right_now | t) == k:
                        for d in range(30):
                            if x & (1 << d) == (1 << d):
                                right_freq[d] -= 1
                        right_now |= t
                        right += 1
                    else:
                        break

                res += right - left + 1

        return res
```
