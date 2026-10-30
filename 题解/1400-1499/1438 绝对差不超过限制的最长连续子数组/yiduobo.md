---
title: "1438. 绝对差不超过限制的最长连续子数组"
aliases: ["yiduobo的每日leetcode 1438.绝对差不超过限制的最长连续子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409580852"
zhihu_id: "409580852"
zhihu_title: "yiduobo的每日leetcode 1438.绝对差不超过限制的最长连续子数组"
question_id: "1438"
question: "绝对差不超过限制的最长连续子数组"
problem_url: "https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/"
difficulty: "Medium"
rating: 1672
created: "2021-09-12T17:15:08+08:00"
updated: "2021-09-12T17:15:08+08:00"
upvotes: 1
comments: 0
---

# 1438. 绝对差不超过限制的最长连续子数组

> **[yiduobo的每日leetcode 1438.绝对差不超过限制的最长连续子数组](https://zhuanlan.zhihu.com/p/409580852) · 知乎 · 2021-09-12 · 赞同 1**
> 力扣：[1438. 绝对差不超过限制的最长连续子数组](https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) · Medium · 灵茶山艾府：[O(n) 做法：滑动窗口 + 单调队列（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1438.绝对差不超过限制的最长连续子数组

[力扣](https://leetcode-cn.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

看上去应该可以使用双指针来解决，具体来说就是对于当前的左边界l，不妨设其最大的符合题目要求的右边界为r，那么对于任意l' \= l + 1而言，其对应的最大右边界r'必然大于等于r。证明也很简单：

1、当l等于r时，已经有l' > r，因此r'必然也大于r

2、当r > l时，设l到r之间的最大值和最小值分别为ma和mi，l + 1到r之间的最大值和最小值为ma'和mi'，那么必然就有ma >\= ma'，mi \<\= mi'，因此若ma - mi \<\= k，那么ma'以及mi'也会满足ma' - mi' \<\= k，因此对于l'而言，r就是一个合法的右边界，因此r'必然大于等于r

于是可以使用双指针，每次将左边界l向右移动一位，并根据此时的情况调整右边界r。这里变成了一个静态的区间最大值和最小值问题，很自然想到使用logn级的数据结构来进行优化，不过在这里如果利用单调性的话，可以由更好的做法。

以最大值为例。由于这里求解的区间是不断向右在移动的，因此对于两个位置p和q，不妨设其满足l \<\= p \< q \<\= r，且nums[p] \<\= nums[q]，那么对于后续任意位置而言，nums[p]都不可能被用来作为最大值，因此在这里需要维护的候选最大值实际上是一个单调递减的数组。当然，随着l的向后移动，也需要修正数组的头部，因此在这里可以使用一个双向队列来维护这些候选值。

首先，若当前队列的头部下标小于l，那么就将队列头部弹出。由于这里l每次只会向右移动一步，因此这个检测只需要做一次。

接下来，考察队列尾部对应的值与当前r对应的值的大小。若队列非空，且队尾的值小于等于r对应的值，那么就将队尾弹出，直到队列为空或者队尾的值大于r对应的值为止。然后将r加入到队列的尾部。若此时满足l到r之间最大最小值之差小于等于k，那么就将r向后移动一位，并重复这个过程。

对于最小值，也同样是使用一个单调的双向队列来进行维护，不过是单调递增的双向队列。

这样一来，由于每个数进出队列只有一次，因此最终的时间复杂度就是O(n)。还有一个小trick是，当r到达数组末尾时，后续的l就没有必要再考虑了，因此随着l的向后移动，得到的合法区间长度必然是越来越小的，不可能超过当前的答案了。

最后附上python代码：

```python
class Solution(object):
    def longestSubarray(self, nums, limit):
        """
        :type nums: List[int]
        :type limit: int
        :rtype: int
        """

        mi_q = []
        ma_q = []
        mi_l = 0
        mi_r = 0
        ma_l = 0
        ma_r = 0
        
        l = 0
        r = 0
        n = len(nums)
        res = 0

        while l < n:
            if mi_l < mi_r and mi_q[mi_l] == l - 1:
                mi_l += 1
            if ma_l < ma_r and ma_q[ma_l] == l - 1:
                ma_l += 1
            
            while r < n:
                num = nums[r]
                while mi_r > mi_l and nums[mi_q[mi_r - 1]] >= num:
                    mi_q.pop()
                    mi_r -= 1

                mi_q.append(r)
                mi_r += 1

                while ma_r > ma_l and nums[ma_q[ma_r - 1]] <= num:
                    ma_q.pop()
                    ma_r -= 1

                ma_q.append(r)
                ma_r += 1

                if nums[ma_q[ma_l]] - nums[mi_q[mi_l]] <= limit:
                    r += 1
                    res = max(res, r - l)
                else:
                    break

            if r == n:
                break
            
            l += 1
        
        return res
```
