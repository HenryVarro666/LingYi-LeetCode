---
title: "1856. 子数组最小乘积的最大值"
aliases: ["yiduobo的每日leetcode 1856.子数组最小乘积的最大值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/472121773"
zhihu_id: "472121773"
zhihu_title: "yiduobo的每日leetcode 1856.子数组最小乘积的最大值"
question_id: "1856"
question: "子数组最小乘积的最大值"
problem_url: "https://leetcode.cn/problems/maximum-subarray-min-product/"
created: "2022-02-25T00:10:19+08:00"
updated: "2022-02-25T00:10:19+08:00"
upvotes: 0
comments: 0
---

# 1856. 子数组最小乘积的最大值

> **[yiduobo的每日leetcode 1856.子数组最小乘积的最大值](https://zhuanlan.zhihu.com/p/472121773) · 知乎 · 2022-02-25 · 赞同 0**
> 力扣：[1856. 子数组最小乘积的最大值](https://leetcode.cn/problems/maximum-subarray-min-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1856.子数组最小乘积的最大值

[力扣](https://leetcode-cn.com/problems/maximum-subarray-min-product/)

题目对于区间[l, r]的最小乘积定义为min(nums[l : r + 1]) \* sum(nums[l : r + 1])。由于题目中数组的规模比较大，那么直接枚举l和r的算法肯定是行不通的。观察上面的式子，很自然就想到将突破口定位在min(nums[l : r + 1])上了。

在这里直到l和r的情况下可以求解出这个最小值，反过来，如果知道了这个最小值，又因为数组中的数都是正数，因此肯定是将l和r扩展得越远最小乘积就越大。于是问题就变成了给定数组中的一个数，找出其左侧和右侧距离这个数最近，且值比这个数要大的数的位置。

对于这个问题之前经常遇到，经典的做法就是一趟遍历，利用单调栈来维护所有的备选答案。由于求解左侧和右侧实际上是等价的，那么在这里以求解左侧的位置来进行说明。

对于数组中的两个位置i和j而言，若i \< j且nums[i] \<\= nums[j]，那么对于j + 1以及更后面的数nums[k]而言，若nums[i] > nums[k]，那么必然就有nums[j] > nums[k]，且此时j距离k明显比i距离k要近。换言之，在将j + 1以及之后位置作为最小值，求解左侧最近且更大的数的位置时，这里的nums[i]就没有保留下来的必要了。这样一来，就可以使用一个单调递减的栈来储存当前依然可能成为备选答案的数。

对于当前求解的数，若栈不为空，且栈顶元素小于等于当前的数，那么就将栈顶元素弹出，直到栈为空或者栈顶元素大于当前的数。接下里，若栈不为空，那么当前的数左侧最近的更大的数就是栈顶元素，否则说明当前这个数左侧可以扩展到数组的左边界。最后，将当前的数加入栈中然后继续向后遍历求解。

由于每个数最多出入栈一次，因此就可以在O(n)的时间复杂度内求出左侧最近的更大数的位置。

反过来一趟扫描，同样的方式就可以求解右侧最近的更大数的位置。

接下来对于数组中某个数而言，就可以通过上面预处理出来的两个栈确定可以向两侧延伸的区间的左右边界，记为[l, r]。此时还需要求出sum(nums[l : r + 1])。这个问题是一个经典的区间和问题，直接使用前缀和来求解就行了，即为prefix_s[r] - prefix_s[l - 1]。这样一来，对于当前这个数而言，确认区间左右边界的操作通过上面预处理的栈只需要O(1)的时间，求解区间和的操作利用前缀和优化后也是O(1)的时间，也就是说只需要O(1)的时间就可以求出某个数作为区间最小值时可能得到的最大的最小乘积。于是只需要一趟遍历，求出每个数作为区间最小值时可以得到的最大最小乘积，取其中的最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumMinProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        stack = []
        left_pos = []
        for index in range(n):
            while stack and nums[stack[-1]] >= nums[index]:
                stack.pop()
            if not stack:
                left_pos.append(-1)
            else:
                left_pos.append(stack[-1])
            stack.append(index)
        
        stack = []
        right_pos = []
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[index]:
                stack.pop()
            if not stack:
                right_pos.append(n)
            else:
                right_pos.append(stack[-1])
            stack.append(index)
        right_pos.reverse()

        mod = 10 ** 9 + 7
        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        res = 0
        for index in range(n):
            delta = s[right_pos[index] - 1]
            if left_pos[index] >= 0:
                delta -= s[left_pos[index]]
            res = max(res, nums[index] * delta)
        
        return res % mod
```
