---
title: "3354. 使数组元素等于零"
aliases: ["yiduobo的每日leetcode 3354.使数组元素等于零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26658082877"
zhihu_id: "26658082877"
zhihu_title: "yiduobo的每日leetcode 3354.使数组元素等于零"
question_id: "3354"
question: "使数组元素等于零"
problem_url: "https://leetcode.cn/problems/make-array-elements-equal-to-zero/"
difficulty: "Easy"
created: "2025-02-27T00:49:53+08:00"
updated: "2025-02-27T00:49:53+08:00"
upvotes: 1
comments: 0
---

# 3354. 使数组元素等于零

> **[yiduobo的每日leetcode 3354.使数组元素等于零](https://zhuanlan.zhihu.com/p/26658082877) · 知乎 · 2025-02-27 · 赞同 1**
> 力扣：[3354. 使数组元素等于零](https://leetcode.cn/problems/make-array-elements-equal-to-zero/) · Easy · 灵茶山艾府：[小球打砖块，O(n) 前后缀分解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3354.使数组元素等于零

[3354. 使数组元素等于零 - 力扣（LeetCode）](https://leetcode.cn/problems/make-array-elements-equal-to-zero/description/)

题目给出一个长度为n的整数数组nums，接下来需要从中选出某个起始位置curr，满足nums[curr]为0，同时选择一个移动方向，方向只能是向左或者向右。

选定了起点和方向后，需要重复一下过程：

1、若当前的curr超出了范围[0, n - 1]，则过程结束

2、若nums[curr]为0，则延当前方向继续移动。如果方向为向右，则将curr加上1，否则减去1

3、若nums[curr] > 0，则将nums[curr]减去1，然后反转方向，并延反转后的方向移动一步

若过程结束后nums中的所有元素都变为0，则认为选择的初始位置和移动方向有效。

问有多少种选择方案是有效的。

首先分析题目中的操作。

1、如果一开始是向左走，且一共向左走了k次，那么向右走的次数要么是k，要么是k - 1。

1-1）如果向右走了k次：

说明行走的方向就是左右左右这样交替，而最后一次沿着右侧走出了边界。这样一来，所有的向左走的操作将会在curr左侧执行减1的操作，一共k次，而所有的向右走的操作中，最后这次操作不会执行减1操作，因此一共会执行k - 1次减1的操作。

如果要使得nums中所有元素都变为0，那么nums[0]到nums[curr - 1]之间的元素之和就必须等于k，而nums[curr + 1]到nums[n - 1]之间的元素之和就必须等于k - 1。

1-2）如果想右走了k - 1次：

说明行走的方向就是左右左右交替，但最后这次则是沿着左侧走出了边界。这样一来，除了最后这次操作之外，所有向左的操作将会在curr左侧执行减1的操作，一共k - 1次，而所有的向右走的操作都会在curr右侧执行减1操作，一共会执行k - 1次减1的操作。

同样的，只有当nums[0]到nums[curr - 1]之间的元素之和以及nums[curr + 1]到nums[n - 1]之间的元素之和都等于k - 1时才能使得nums中的所有元素都变为0。

综合起来可以发现，对于某个nums[curr]为0的下标位置curr，若nums[0]到nums[curr - 1]之间的元素之和left等于nums[curr + 1]到nums[n - 1]之间的元素之和right，或者left恰好等于right + 1，那么选择在curr处开始向左走就是有效的方案。

2、如果一开始是向右走，且一共向右走了k次，那么向左走的次数要么是k，要么是k - 1。

与情况1对称，不需要具体分析就可以知道在这种情况下，若nums[0]到nums[curr - 1]之间的元素之和left等于nums[curr + 1]到nums[n - 1]之间的元素之和right，或者left恰好等于right - 1，那么选择在curr处开始向右走就是有效的方案。

更进一步的，对于下标位置curr，对比左侧元素之和left以及右侧元素之和right，若二者相等，那么从curr开始向左或者向右走都是有效的方案，应该将答案加上2；若二者相差1，那么一定有一个方向是有效的方案，应该将答案加上1。

问题到了这里就转化成了前缀和与后缀和对比的问题，而后缀和可以通过总和减去前缀和得到，于是可以先计算出数组总和s，然后一趟遍历，一边计算前缀和now，一边对于值为0的下标位置，对比当前的now和s - now的大小来更新答案。

最后附上python代码：

```python
class Solution(object):
    def countValidSelections(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        s = sum(nums)
        now = 0
        for v in nums:
            if v == 0:
                if s - now == now:
                    res += 2
                elif abs(s - now - now) == 1:
                    res += 1
            now += v
        
        return res
```
