---
title: "4075. 最长有韧性的子数组I & 4076. 最长有韧性的子数组II"
aliases: ["yiduobo的每日leetcode 4075.最长有韧性的子数组I && 4076.最长有韧性的子数组II", "4075. 最长有韧性的子数组I", "4076. 最长有韧性的子数组II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2093145532285851428"
zhihu_id: "2093145532285851428"
zhihu_title: "yiduobo的每日leetcode 4075.最长有韧性的子数组I && 4076.最长有韧性的子数组II"
question_id: ["4075", "4076"]
question: ["最长有韧性的子数组I", "最长有韧性的子数组II"]
problem_url: ["https://leetcode.cn/problems/longest-resilient-subarray-i/", "https://leetcode.cn/problems/longest-resilient-subarray-ii/"]
created: "2026-10-13T01:13:36+08:00"
updated: "2026-10-13T01:13:39+08:00"
upvotes: 0
comments: 0
---

# 4075. 最长有韧性的子数组I & 4076. 最长有韧性的子数组II

> **[yiduobo的每日leetcode 4075.最长有韧性的子数组I && 4076.最长有韧性的子数组II](https://zhuanlan.zhihu.com/p/2093145532285851428) · 知乎 · 2026-10-13 · 赞同 0**
> 力扣：[4075. 最长有韧性的子数组I](https://leetcode.cn/problems/longest-resilient-subarray-i/)
> 力扣：[4076. 最长有韧性的子数组II](https://leetcode.cn/problems/longest-resilient-subarray-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4075.最长有韧性的子数组I

<https://leetcode.cn/problems/longest-resilient-subarray-i/description/>

4076.最长有韧性的子数组II

<https://leetcode.cn/problems/longest-resilient-subarray-ii/description/>

题目给出一个整数数组nums以及一个整数k。

对于一个子数组，若其中的每个元素在被删掉后，剩余元素的和能被k整除，那么就称其为有韧性的。

长度为1的子数组总是被认为有韧性的。

问最长有韧性子数组的长度。

两题的题设一致，第二题的数据规模较大，nums的长度可达10^5。

对于一个有韧性的子数组，不妨设其中元素之和为s，那么对于其中任意两个不同的元素a和b，都有

s - a ≡ s - b ≡ 0(mod k)

更进一步的，就有

a ≡ b(mod k)

换言之，如果将这个子数组中的所有元素都相对k取模，那么子数组中所有的元素将全部是同一种元素，而这些元素之和模k的结果也刚好就是这种元素自身。

基于这一点，就可以将nums中所有元素都对k取模，然后将其按照相同的值分为若干段。对于每一段，都找出最长的，且和模k恰好等于这一段元素值的子数组，这个子数组就是当前这一段元素所能形成的最长的有韧性的子数组，取其中最长的长度作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def resilientSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        res = 1
        r = -1
        s = 0
        length = 0
        for v in nums:
            v %= k
            if v == r:
                s += v
                length += 1
                s %= k
                if s == v:
                    res = max(res, length)
            else:
                s = v
                length = 1
                r = v

        
        return res
```
