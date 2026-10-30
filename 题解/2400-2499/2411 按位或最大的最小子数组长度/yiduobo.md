---
title: "2411. 按位或最大的最小子数组长度"
aliases: ["yiduobo的每日leetcode 2411.按位或最大的最小子数组长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/sliding-window", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/568474032"
zhihu_id: "568474032"
zhihu_title: "yiduobo的每日leetcode 2411.按位或最大的最小子数组长度"
question_id: "2411"
question: "按位或最大的最小子数组长度"
problem_url: "https://leetcode.cn/problems/smallest-subarrays-with-maximum-bitwise-or/"
difficulty: "Medium"
rating: 1938
created: "2022-09-27T03:33:57+08:00"
updated: "2022-09-27T03:33:57+08:00"
upvotes: 0
comments: 0
---

# 2411. 按位或最大的最小子数组长度

> **[yiduobo的每日leetcode 2411.按位或最大的最小子数组长度](https://zhuanlan.zhihu.com/p/568474032) · 知乎 · 2022-09-27 · 赞同 0**
> 力扣：[2411. 按位或最大的最小子数组长度](https://leetcode.cn/problems/smallest-subarrays-with-maximum-bitwise-or/) · Medium · 灵茶山艾府：[从 O(nlogU) 到 O(n)：LogTrick / 滑动窗口 + 栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2411.按位或最大的最小子数组长度

[力扣](https://leetcode.cn/problems/smallest-subarrays-with-maximum-bitwise-or/)

对于这类子数组长度有关的问题，通常的做法就是使用滑动窗口。

对于本题，首先可以明确的一点是当窗口的左边界向右移动时，右边界要么保持不变，要么也跟着向右移动，这也是使用滑动窗口的前提。

简单的证明如下：不妨设某一轮左边界滑动到下标left，其对应的右边界下标为right，那么对于左边界为left + 1的子数组而言，其右边界必然大于等于right，因为若此时对应的右边界right'小于right，那么意味着将nums[right]加入到当前子数nums[left + 1: right' + 1]是不影响这个子数组的按位或的结果。另一方面，由于nums[left + 1: right']是nums[left: right]的一个子数组，那么nums[left : right]的按位或的结果必然是包含了nums[left : right' + 1]的按位或结果在内，这也就意味着对于nums[left : right]而言，加入nums[right]并不会影响到按位或的结果，因此left对应的右边界就不应该是right，产生了矛盾。

根据上面的结论，在确定了右边界必然随着左边界向右移动后，接下来要解决的问题就是新的右边界在向右移动的过程中应该在何处停下。一个直观的理解就是停下的时刻，新的右边界右侧的所有数都没有加入到子数组中的必要了，在位运算的角度就是右侧所有的数的二进制表示中，所有为1的位都在现有子数组中出现过。当然，在这里一个一个判断效率是很低的，注意到或运算的性质，在这里可以一次性全部算了，即使用当前子数组中所有数的按位或结果now，与当前右边界右侧所有数的按位或结果suffix，再取或运算。若这个结果等于now，说明suffix中所有为1的位都在now中出现过，此时子数组的右边界就没有必要向后移动的。而对于suffix的计算，则是一个典型的后缀和问题，可以实现一趟遍历预处理出来。

到了这里，寻找新的右边界就已经解决了。剩下的问题就是当左边界向右移动时，如何将老的左边界对应的值从当前子数组的按位或结果中排除出去。需要注意的是，在这里不能直接使用异或运算，因为当前子数组中的数，在某些二进制位上可能出现了多次，仅排除掉老的左边界这一次该位上依然为1而不是0。

因此在这里就需要再加入一个数组cnt，其中cnt[pos]表示当前子数组中，在pos这一位上为1的数有多少个。当右边界向右扩展时，就将新加入的数按位拆分出来并更新cnt。而当左边界向右移动时，则先考察老的左边界对应的数，同样是将其拆分后更新cnt，而此时若cnt中某一位从1变成了0，说明当前这一位由于老的左边界被移除数组后，子数组中已经没有这一位上为1的数了，因此需要将子数组的按位或结果now也去除掉这一位。

最后附上python代码：

```python
class Solution(object):
    def smallestSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        suffix = [nums[-1]]
        n = len(nums)
        for index in range(n - 2, -1, -1):
            suffix.append(suffix[-1] | nums[index])
        suffix.reverse()

        res = []
        cnt = [0] * 31
        p = -1
        now = 0

        for index in range(n):
            if p < index:
                p = index
                now = nums[index]
                tmp = now
                pos = 0
                while tmp:
                    if tmp % 2 == 1:
                        cnt[pos] += 1
                    tmp /= 2
                    pos += 1
            
            while p + 1 < n and (now | suffix[p + 1]) != now:
                p += 1
                now |= nums[p]
                tmp = nums[p]
                pos = 0
                while tmp:
                    if tmp % 2 == 1:
                        cnt[pos] += 1
                    tmp /= 2
                    pos += 1
            
            res.append(p - index + 1)
            remove = 0
            tmp = nums[index]
            pos = 0
            while tmp:
                if tmp % 2 == 1:
                    cnt[pos] -= 1
                    if cnt[pos] == 0:
                        remove |= (1 << pos)
                tmp /= 2
                pos += 1
            
            now ^= remove
        
        return res
```
