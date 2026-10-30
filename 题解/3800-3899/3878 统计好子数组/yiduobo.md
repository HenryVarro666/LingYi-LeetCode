---
title: "3878. 统计好子数组"
aliases: ["yiduobo的每日leetcode 3878.统计好子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/monotonic-stack", "题单/单调栈", "题单/位运算", "题单/单调栈/三-贡献法", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019899518762664584"
zhihu_id: "2019899518762664584"
zhihu_title: "yiduobo的每日leetcode 3878.统计好子数组"
question_id: "3878"
question: "统计好子数组"
problem_url: "https://leetcode.cn/problems/count-good-subarrays/"
difficulty: "Hard"
rating: 2230
created: "2026-03-24T22:39:02+08:00"
updated: "2026-03-24T22:39:03+08:00"
upvotes: 1
comments: 0
---

# 3878. 统计好子数组

> **[yiduobo的每日leetcode 3878.统计好子数组](https://zhuanlan.zhihu.com/p/2019899518762664584) · 知乎 · 2026-03-24 · 赞同 1**
> 力扣：[3878. 统计好子数组](https://leetcode.cn/problems/count-good-subarrays/) · Hard · 灵茶山艾府：[两种方法：LogTrick / 单调栈+贡献法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3878.统计好子数组

<https://leetcode.cn/problems/count-good-subarrays/description/>

题目给出一个整数数组nums。

若一个子数组中所有元素的按位或等于该子数组中至少出现一次的元素，那么就称其为好子数组。

要求找出nums中好子数组的数量。

由于按位或是越或越大的，因此如果一个子数组是好子数组，其中元素的按位或必然等于其中的最大值，同时其中的最大值与其他元素按位或的结果也恰好就等于这个最大值。

基于这一点，就可以对每个nums[index]都找以nums[index]作为好子数组中最左侧的最大值时，可以向左最远扩展的位置以及向右最远扩展的位置。

更具体的，令left\[index\]表示处于index左侧第一个满足nums\[index\] | nums\[left\[index\]\] !\= nums\[index\]或者满足nums\[index\] \= nums\[left\[index\]\]的位置，令right\[index\]表示处于index右侧第一个满足nums\[index\] | nums\[right\[index\]\] !\= nums\[index\]的位置，那么从left\[index\] + 1到index之间任取一个位置作为子数组的左边界，从right\[index\] - 1到index之间任取一个位置作为子数组的右边界，都可以得到一个好子数组。这个好子数组中的所有元素与nums\[index\]按位或的结果都恰好等于nums\[index\]，同时nums\[index\]也是子数组中最左侧的最大值。可以发现，一共就是(index - left\[index\]) \* (right\[index\] - index)种可行的方案。

这样一来，只需要想办法计算出每个index对应的left[index]以及right[index]，就可以一趟遍历，通过上面的式子计算出最终结果了。

接下来的问题就是如何计算left和right数组。

注意到大数与小数按位或恰好等于大数是具有传递性的，也就是说对于一组a >\= b >\= c，若a | b \= a，b | c \= b，那么必然有a | c \= a。在计算left和right时就可以利用这一点。

更进一步的，对于nums\[index\]，若nums\[index\]cover不住nums\[index - 1\]，那么其对应的left\[index\]就是index - 1；反之，其对应的left\[index\]，就可以在left\[index - 1\]的基础上继续向左计算，理由是nums\[index\]可以cover住nums\[index - 1\]，而nums\[index - 1\]可以cover住nums\[index - 2\]到nums\[left\[index - 1\] + 1\]之间的所有元素，因此nums\[index\]也必然可以cover住这些元素，接下来就可以从left\[index - 1\]这一关开始继续向左检测。若nums\[index\]可以cover住left\[index - 1\]，那么还可以继续往前走到left\[left\[index - 1\]\]，以此类推，直到被卡住，或者cover住整个左侧部分。

更进一步的，在这里可以使用一个单调栈来储存所有这些卡壳的位置，那么对于当前遍历到nums[index]：

- 若其能cover住栈顶的位置，那么就将栈顶的位置弹出，表示这个卡壳的位置并没有卡住nums[index]。重复此过程直到栈为空，或者栈顶元素卡主了nums[index]。
- 若栈为空，说明没有元素可以卡住nums[index]，即nums[index]可以cover其左侧所有的元素，此时的left[index]可以置为-1；反之，就有left[index] \= stack[-1]，即nums[index]被stack[-1]卡住了。
- 最后，还需要将index加入到栈中。这样做没有问题的理由是如果后续的元素可以cover住nums[index]，那么也可以cover住被nums[index]cover的这些元素，因此之前弹出的元素没必要再储存在栈中。

对于right的计算也是类似，不过由于没有第一个的限制，在这里只需要判断异或结果，不需要判断是否相等。

这样一来，就可以先正反两趟遍历，通过单调栈计算出left和right，然后再一趟遍历得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def countGoodSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)

        stack = []
        left = [-1] * n
        for index in range(n):
            while stack and nums[stack[-1]] < nums[index] and (nums[stack[-1]] | nums[index]) == nums[index]:
                stack.pop()
            if stack:
                left[index] = stack[-1]
            else:
                left[index] = -1
            stack.append(index)
        
        stack = []
        right = [n] * n
        for index in range(n - 1, -1, -1):
            while stack and (nums[stack[-1]] | nums[index]) == nums[index]:
                stack.pop()
            if stack:
                right[index] = stack[-1]
            else:
                right[index] = n
            stack.append(index)
        
        res = 0
        for index in range(n):
            res += (index - left[index]) * (right[index] - index)
        
        return res
```
