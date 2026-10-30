---
title: "2009. 使数组连续的最少操作数"
aliases: ["yiduobo的每日leetcode 2009.使数组连续的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/503783586"
zhihu_id: "503783586"
zhihu_title: "yiduobo的每日leetcode 2009.使数组连续的最少操作数"
question_id: "2009"
question: "使数组连续的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-continuous/"
difficulty: "Hard"
rating: 2084
created: "2022-04-23T22:05:37+08:00"
updated: "2022-04-23T22:05:37+08:00"
upvotes: 1
comments: 0
---

# 2009. 使数组连续的最少操作数

> **[yiduobo的每日leetcode 2009.使数组连续的最少操作数](https://zhuanlan.zhihu.com/p/503783586) · 知乎 · 2022-04-23 · 赞同 1**
> 力扣：[2009. 使数组连续的最少操作数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-continuous/) · Hard · 灵茶山艾府：[正难则反 + 滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2009.使数组连续的最少操作数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-operations-to-make-array-continuous/)

题目要求让数组中的数连续，如果换一个角度来看，可以认为是给出了数轴上的一些点，然后需要找出一个大小为n的窗口，其中包含尽量多的点，即为k，最终答案就是n - k。

这样一来，就转化成了一个常规的滑动窗口问题，不过在这里直接用长度为n的窗口在数轴上滑时间复杂度太高了，需要进行一些优化。

可以证明的是，以数轴上某个点作为窗口右边界时必然能找到最优解。

不妨设现在某个窗口不是以数轴上某个点为右边界，那么完全可以将窗口整体向左移动一段，直到右边界与数轴上的点重合。窗口右侧移出的这些部分不包含任何点，而左侧新加入的部分反而可能会往窗口中加入新的点，这样就保证了窗口中包含的点不会变少。

有了上面的结论，就可以将数轴上的点从小到大进行排序，然后一趟遍历，枚举每个点作为窗口的右边界，并判断有哪些点在窗口中。

随着右边界的向后移动，窗口包含的最左侧的点必然也跟着向右移动，因此可以利用单调性，在均摊O(1)的时间内找出每个窗口包含的最左侧的点，并通过这两个边界对应点的下标更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        sorted_nums = sorted(set(nums))
        m = len(sorted_nums)

        res = n - 1
        now = 1
        left = 0

        while now < m:
            while sorted_nums[now] - sorted_nums[left] >= n:
                left += 1

            res = min(res, n - (now - left + 1))
            now += 1

        return res
```
