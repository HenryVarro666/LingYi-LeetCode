---
title: "3095. 或值至少K的最短子数组I"
aliases: ["yiduobo的每日leetcode 3095.或值至少K的最短子数组I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699514142"
zhihu_id: "699514142"
zhihu_title: "yiduobo的每日leetcode 3095.或值至少K的最短子数组I"
question_id: "3095"
question: "或值至少为 K 的最短子数组 I"
problem_url: "https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-i/"
difficulty: "Easy"
created: "2024-05-23T23:52:16+08:00"
updated: "2024-05-23T23:52:16+08:00"
upvotes: 0
comments: 0
---

# 3095. 或值至少K的最短子数组I

> **[yiduobo的每日leetcode 3095.或值至少K的最短子数组I](https://zhuanlan.zhihu.com/p/699514142) · 知乎 · 2024-05-23 · 赞同 0**
> 力扣：[3095. 或值至少为 K 的最短子数组 I](https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3095.或值至少K的最短子数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-i/description/)

题目的数据规模很小，直接使用暴力法也是完全可行的，我在这里采用的滑动窗口。使用一个变长的滑动窗口从左向右滑动，若当前窗口内元素的或值小于k，就不断向右扩展窗口右边界直到来到数组末尾或者窗口内元素或值大于等于k为止。另一方面，每轮向右移动窗口左边界，由于是或运算，无法简单的计算窗口内部新的或值，我在这里使用了一个哈希表来记录窗口内每种位上有多少个1，当出现窗口左边界右移导致的某一数位上的1被全部清空时，窗口内元素的或值就需要清除掉这一位上的1。

最后附上python代码：

```python
class Solution(object):
    def minimumSubarrayLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        freq = [0] * 30
        p = 0
        now = 0
        res = -1
        for index, v in enumerate(nums):
            if p == index:
                now = v
                p += 1
                for t in range(30):
                    if v & (1 << t) == (1 << t):
                        freq[t] += 1

            while p < len(nums) and now < k:
                now |= nums[p]
                for t in range(30):
                    if nums[p] & (1 << t) == (1 << t):
                        freq[t] += 1
                p += 1
            
            if now < k:
                break

            if res == -1 or res > p - index:
                res = p - index
            
            for t in range(30):
                if nums[index] & (1 << t) == (1 << t):
                    freq[t] -= 1
                    if freq[t] == 0:
                        now ^= (1 << t)
        
        return res
```
