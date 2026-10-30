---
title: "3171. 找到按位或最接近k的子数组"
aliases: ["yiduobo的每日leetcode 3171.找到按位或最接近k的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/bit-manipulation", "leetcode/sliding-window", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705222424"
zhihu_id: "705222424"
zhihu_title: "yiduobo的每日leetcode 3171.找到按位或最接近k的子数组"
question_id: "3171"
question: "找到按位或最接近 K 的子数组"
problem_url: "https://leetcode.cn/problems/find-subarray-with-bitwise-or-closest-to-k/"
difficulty: "Hard"
created: "2024-06-25T00:50:19+08:00"
updated: "2024-06-25T00:50:19+08:00"
upvotes: 1
comments: 0
---

# 3171. 找到按位或最接近k的子数组

> **[yiduobo的每日leetcode 3171.找到按位或最接近k的子数组](https://zhuanlan.zhihu.com/p/705222424) · 知乎 · 2024-06-25 · 赞同 1**
> 力扣：[3171. 找到按位或最接近 K 的子数组](https://leetcode.cn/problems/find-subarray-with-bitwise-or-closest-to-k/) · Hard · 灵茶山艾府：[两种方法：LogTrick/滑动窗口+栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3171.找到按位或最接近k的子数组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-subarray-with-bitwise-or-closest-to-k/description/)

题目给出一个数组nums以及一个整数k，要求从中找出一个子数组，使得子数组中各元素按位或的结果与k的差的绝对值最小。

当时写这题的时候，题目是要找按位与最接近k的子数组，现在不知道怎么突然改成或了，不过处理方法也差不太多。对于按位与的处理方法，可以参考之前的3117题。

[yiduobo：yiduobo的每日leetcode 3117.划分数组得到最小的值之和](https://zhuanlan.zhihu.com/p/701264461)

题目实际上可以认为是对于每个下标index，找出下标p使得nums[p : index]小于等于p，同时nums[p - 1 : index]大于p，此时就可以用这两个按位或的结果来更新答案。

对于按位或而言，有一个性质就是参与运算的数字越多，按位或的结果就越大。换言之，对于某个下标index以及其对应的下标p，若index' \= index + 1，那么其对应的p'必然大于等于p，也就是说在这里可以使用变长的滑动窗口来处理。

不过需要注意的是，当窗口的左边界移动时，左边界上的元素被移除，但是无法直接判断移除这个元素会使得窗口内元素按位或的结果产生什么变化，此时就需要额外维护一个频率数组freq，其中freq[d]表示当前窗口内元素在二进制位d这一位上1的数量。当某个元素被移除窗口时，遍历所有二进制位d，若这个元素在d这一位上的值为1，那么就将freq[d]减去1，若此时freq[d]变成了0，就说明窗口中所有元素都不包含这一位，此时就需要将这一位从窗口内元素的按位或结果中移除。

另外还有一点就是题目要求数组非空，因此在这里需要保证窗口内至少有一个元素。

最后附上python代码：

```python
class Solution(object):
    def minimumDifference(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        freq = [0] * 30
        now = 0
        p = 0
        res = None

        for index, v in enumerate(nums):
            now |= v

            for d in range(30):
                if v & (1 << d) == (1 << d):
                    freq[d] += 1

            if res is None or res > abs(now - k):
                res = abs(now - k)
            
            while p < index and now > k:
                for d in range(30):
                    if nums[p] & (1 << d) == (1 << d):
                        freq[d] -= 1
                        if freq[d] == 0:
                            now ^= (1 << d)
                p += 1
            
                if res is None or res > abs(now - k):
                    res = abs(now - k)

        return res
```
