---
title: "2289. 使数组按非递减顺序排列"
aliases: ["yiduobo的每日leetcode 2289.使数组按非递减顺序排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553056299"
zhihu_id: "553056299"
zhihu_title: "yiduobo的每日leetcode 2289.使数组按非递减顺序排列"
question_id: "2289"
question: "使数组按非递减顺序排列"
problem_url: "https://leetcode.cn/problems/steps-to-make-array-non-decreasing/"
difficulty: "Medium"
rating: 2482
created: "2022-08-13T01:03:29+08:00"
updated: "2022-08-13T01:03:29+08:00"
upvotes: 1
comments: 0
---

# 2289. 使数组按非递减顺序排列

> **[yiduobo的每日leetcode 2289.使数组按非递减顺序排列](https://zhuanlan.zhihu.com/p/553056299) · 知乎 · 2022-08-13 · 赞同 1**
> 力扣：[2289. 使数组按非递减顺序排列](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/) · Medium · 灵茶山艾府：[等价转换 + 利用单调性（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2289.使数组按非递减顺序排列

[力扣](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/)

由于题目的数据规模比较大，因此不能直接模拟删除的过程，需要从中找一些规律。

一个比较直观的思路是，从左向右一趟遍历，对于当前的数nums[index]，设其右侧第一个大于等于nums[index]为nums[p]，那么nums[index + 1]到nums[p - 1]之间的数最终都会被删除。这些数可能被nums[index]直接删除，也可能被nums[index + 1]到nums[p - 1]中的另外一些数删除掉。

也正是由于有后面这种情况存在，使得判断删除的轮次有一定的困难。不妨观察下面三个例子：

[6, 1, 2, 3, 4, 5]

[6, 1, 2, 5, 3, 4]

[6, 1, 5, 2, 4, 3]

需要的删除轮次分别为5、3、2。造成这种差异的原因就是上面说的后面这种情况，即在6删除其他数的同时，数组中的某些数也在删除其他数，直到这些数自身被删除为止。

也就是说，有一个问题是避不开的，即每个数将在第几轮被删除。实际上，知道了这个问题的结果也就知道了最终的答案，因为最终答案就是所有数被删除轮次中的最大值。

问题的变化带来了视角的转换，不妨从被删除的数的角度来看这个问题。对于数组中的数nums[index]而言，若其左侧没有任何数比它大，那么nums[index]就不会被删除，否则设其左侧大于nums[index]且最靠近nums[index]为nums[p]，那么在nums[p + 1]到nums[index - 1]都被删除之后，nums[index]将被nums[p]删除。

这里有一种情况是如果在nums[p + 1]到nums[index - 1]被删除完之前，nums[p]就被更前面的数删除掉了。可以发现，这种情况并不会影响到nums[index]的删除轮次，因为nums[index]此时只要等nums[p + 1]到nums[index - 1]被删除完之后，就会被删除掉nums[p]的那个数删除。

于是可以令use_step[i]表示第i个数被删除的轮次，那么当存在p时，就有use_step[index] \= max(use_step[p + 1], use_step[p + 2], ..., use_step[index - 1]) + 1，否则就有use_step[index] \= 0。

而对于找到每个index对应的p这个问题，则可以利用经典的单调栈。

最后附上python代码：

```python
class Solution(object):
    def totalSteps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        use_step = []
        stack = []
        res = 0
        for index, num in enumerate(nums):
            now = 0
            while stack and nums[stack[-1]] <= num:
                now = max(now, use_step[stack[-1]])
                stack.pop()

            if stack:
                now += 1
            else:
                now = 0
            
            use_step.append(now)
            stack.append(index)

        return max(use_step)
```
