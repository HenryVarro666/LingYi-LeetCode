---
title: "2401. 最长优雅子数组"
aliases: ["yiduobo的每日leetcode 2401.最长优雅子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/two-pointers", "leetcode/enumeration", "leetcode/sliding-window", "leetcode/bao-li", "题单/滑动窗口与双指针", "题单/位运算", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567272151"
zhihu_id: "567272151"
zhihu_title: "yiduobo的每日leetcode 2401.最长优雅子数组"
question_id: "2401"
question: "最长优雅子数组"
problem_url: "https://leetcode.cn/problems/longest-nice-subarray/"
difficulty: "Medium"
rating: 1750
created: "2022-09-23T00:17:03+08:00"
updated: "2022-09-23T00:17:03+08:00"
upvotes: 0
comments: 0
---

# 2401. 最长优雅子数组

> **[yiduobo的每日leetcode 2401.最长优雅子数组](https://zhuanlan.zhihu.com/p/567272151) · 知乎 · 2022-09-23 · 赞同 0**
> 力扣：[2401. 最长优雅子数组](https://leetcode.cn/problems/longest-nice-subarray/) · Medium · 灵茶山艾府：[暴力枚举 / 双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2401.最长优雅子数组

[力扣](https://leetcode.cn/problems/longest-nice-subarray/)

对于这类找最长子数组的问题，通常的做法就是遍历其中的一端，然后利用单调性在均摊O(1)的时间内找出当前情况下子数组最优的另一端。对于本题也可以采用这种做法。

从左到右枚举子数组的右边界，另外使用一个遍历p记录当前右边界对应的最小左边界是什么。接下来对于当前枚举到的数nums[index]，其上一个位置index - 1对应的子数组左边界为p，那么index对应的左边界p'就必然大于等于p。证明也很简单，因为若p' \< p，那么说明p'到p - 1之间的数与p到index - 1之间的数两两之间按位与都等于0，那么对于index - 1而言，其最优的左边界就应该是p'而不是p，产生了矛盾。

有了这一点，对于当前的index而言，就可以在上一轮p的基础上向后来找对应的p'。最好的情况下，p'就等于p，那么此时需要满足nums[p]到nums[index - 1]之间的数与nums[index]做按位与都等于0，否则就需要找出其中下标最大的，且与nums[index]按位与不等于0的数，将p'更新为这个下标加1。当然，在这里不可能枚举每个位置来进行判断，时间复杂度太高。

由于是与运算，那么就可以使用nums[p]到nums[index - 1]中所有数的或运算结果，来和nums[index]做与运算进行判断。这样做的理由是如果与运算的结果不为0，说明必然存在至少一个二进制位，满足这个所有数的或运算结果以及nums[index]在这一位上都为1，也就是说nums[p]到nums[index - 1]中至少有一个数在这一位上为1，那么这个数和nums[index]做与运算自然也不等于0了。

根据上面的结论，不妨设nums[p]到nums[index - 1]的或运算结果为now，那么当now & nums[index]不为0时，和nums[index]与运算结果不为0的那个数的下标必然是大于等于p的，也就是说无论如何nums[p]都不可能留在以index为右边界的数组中了，因此在这里可以将nums[p]从中移除，此时就需要更新now为now ^ nums[p]，同时将p加上1。这里做异或操作的原因是由于nums[p]到nums[index - 1]之间的数两两做与运算都等于0，因此对于nums[p]二进制表示下为1的那几位而言，now的二进制表示下对应的那几位都来自于nums[p]，同时不可能有其他数的这几位为1，因此在这里直接执行异或操作就可以得到nums[p + 1]到nums[index - 1]这些数的或操作结果了。不断重复此过程，直到now与nums[index]按位与的结果为0为止。此时新的p就是index对应的左边界，因此可以使用index - p + 1来更新答案。接下来还需要将nums[index]也加入到now中，然后继续向后考虑index + 1直到枚举完所有的右边界。

最后附上python代码：

```python
class Solution(object):
    def longestNiceSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        p = 0
        now = nums[0]
        res = 1
        for index in range(1, len(nums)):
            while (now & nums[index]) > 0:
                now ^= nums[p]
                p += 1
            
            now |= nums[index]
            res = max(res, index - p + 1)
        
        return res
```
