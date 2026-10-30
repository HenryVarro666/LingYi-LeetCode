---
title: "239. 滑动窗口最大值"
aliases: ["yiduobo的每日leetcode 239.滑动窗口最大值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/常用数据结构/四-队列", "题单/LeetCode-热题-100/子串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150719702"
zhihu_id: "150719702"
zhihu_title: "yiduobo的每日leetcode 239.滑动窗口最大值"
question_id: "239"
question: "滑动窗口最大值"
problem_url: "https://leetcode.cn/problems/sliding-window-maximum/"
difficulty: "Hard"
created: "2020-06-25T21:29:03+08:00"
updated: "2020-06-25T21:29:03+08:00"
upvotes: 1
comments: 1
---

# 239. 滑动窗口最大值

> **[yiduobo的每日leetcode 239.滑动窗口最大值](https://zhuanlan.zhihu.com/p/150719702) · 知乎 · 2020-06-25 · 赞同 1**
> 力扣：[239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) · Hard · 灵茶山艾府：[降本增笑，秒懂单调队列！附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

239.滑动窗口最大值<https://leetcode-cn.com/problems/sliding-window-maximum/>

设当前窗口的范围为l到r，那么若存在x，y，满足l \<\= x \< y \<\= r，且nums[x] \< nums[y]，那么在窗口在持续往右滑动的过程中，nums[x]是一定不可能成为某个窗口的最大值的。原因是在窗口往右滑动直到l抵达x时，nums[y]一定是在l到r之间的，因此至少有nums[y]比nums[x]大，因此nums[x]一定不可能成为滑动窗口的最大值。

有了上面这个结论，我们就可以维护一个栈，每当窗口往右滑动时，将栈内小于nums[r]的数全部弹出，因为这些数已经不可能成为答案了，然后再将nums[r]压入栈中即可。此时栈中最大的数一定是栈底元素，同时也就是当前窗口的最大值。

不过随着窗口的滑动，l也在往右移动，于是栈底元素可能在某个时刻就不再处于滑动窗口内了。于是在执行上面操作的同时，需要判断栈底如果是第l - 1个数，那么也需要将其弹出栈。显然，栈是无法高效地完成这个操作的，于是可以改为使用双向队列来执行上面的操作，或者使用数组和左右指针来模拟双向队列来实现。

一趟扫描，每个数最多进出双向队列一次，于是最终的时间复杂度为O(n)。

最后附上python代码，我这里使用的是数组和双指针来模拟双向队列，l和r分别表示双向队列的左右边界：

```python
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        q = []
        pos = []
        l = 0
        r = 0

        for index in range(k):
            while r > l and q[r - 1] < nums[index]:
                pos.pop()
                q.pop()
                r -= 1
            
            q.append(nums[index])
            pos.append(index)
            r += 1

        res = [q[0]]

        for index in range(k, len(nums)):
            if pos[l] + k == index:
                l += 1
            while r > l and q[r - 1] < nums[index]:
                pos.pop()
                q.pop()
                r -= 1
            
            q.append(nums[index])
            pos.append(index)
            r += 1
            res.append(q[l])

        return res
```
