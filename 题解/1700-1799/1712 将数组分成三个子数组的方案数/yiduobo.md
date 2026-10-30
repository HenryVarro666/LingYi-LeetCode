---
title: "1712. 将数组分成三个子数组的方案数"
aliases: ["yiduobo的每日leetcode 1712.将数组分成三个子数组的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449884694"
zhihu_id: "449884694"
zhihu_title: "yiduobo的每日leetcode 1712.将数组分成三个子数组的方案数"
question_id: "1712"
question: "将数组分成三个子数组的方案数"
problem_url: "https://leetcode.cn/problems/ways-to-split-array-into-three-subarrays/"
difficulty: "Medium"
rating: 2079
created: "2021-12-25T23:12:02+08:00"
updated: "2021-12-25T23:12:02+08:00"
upvotes: 0
comments: 0
---

# 1712. 将数组分成三个子数组的方案数

> **[yiduobo的每日leetcode 1712.将数组分成三个子数组的方案数](https://zhuanlan.zhihu.com/p/449884694) · 知乎 · 2021-12-25 · 赞同 0**
> 力扣：[1712. 将数组分成三个子数组的方案数](https://leetcode.cn/problems/ways-to-split-array-into-three-subarrays/) · Medium · 灵茶山艾府：[Golang 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1712.将数组分成是三个子数组的方案数

[力扣](https://leetcode-cn.com/problems/ways-to-split-array-into-three-subarrays/)

最朴素的想法当然是从左向右枚举第一个子数组的右边界l，并计算这个子数组之和l_sum。

接下来从l + 1开始向后枚举第二个区间的右边界r，并计算这个子数组之和m_sum，那么第三个区间之和就是s - l_sum - m_sum，这里s表示的是整个数组之和。若此时l_sum \<\= m_sum \<\= s - l_sum - m_sum，那么将答案加上1。

上面做法的时间复杂度为O(n^2)，显然是不能接受的。注意到数组中的数都是非负数，那么在枚举了l之后，可以利用双指针确定中间这个区间的最小右边界min_r以及最大右边界max_r。这里min_r表示的是最小的r，使得m_sum >\= l_sum且s - m_sum - l_sum >\= m_sum，而max_r表示的则是最大的满足上面这个条件的r。此时就可以提供max_r - min_r + 1组可行的答案。

由于数组中都是非负数，那么虽然l的向后推移，min_r以及max_r都是单调不减的，也就是说枚举min_r和max_r的均摊复杂度为O(1)，整体的时间复杂度为O(n)。

在这里需要一种特殊情况，即l移动到min_r之后，必须立即更新min_r，而不能靠m_sum来更新min_r，这是因为数组中有0存在，那么在l_sum为0的情况下，min_r就不会向后更新了。

最后附上python代码：

```python
class Solution(object):
    def waysToSplit(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        l = 0
        min_r = max_r = 1
        l_sum = nums[0]
        m_sum_min = m_sum_max = nums[1]
        s = sum(nums)

        res = 0
        mod = 10 ** 9 + 7
        n = len(nums)

        while l < n - 2:
            while min_r + 1 < n - 1 and m_sum_min < l_sum:
                min_r += 1
                m_sum_min += nums[min_r]

            if m_sum_min >= l_sum and s - l_sum - m_sum_min >= m_sum_min:
                if min_r > max_r:
                    max_r = min_r
                    m_sum_max = m_sum_min
            
                while max_r + 1 < n - 1 and s - l_sum - m_sum_max - nums[max_r + 1] >= m_sum_max + nums[max_r + 1]:
                    max_r += 1
                    m_sum_max += nums[max_r]

                res += max_r - min_r + 1
                if res >= mod:
                    res -= mod

            l += 1
            m_sum_min -= nums[l]
            m_sum_max -= nums[l]
            l_sum += nums[l]
            if min_r == l:
                min_r = l + 1
                m_sum_min = nums[min_r]
                
        return res
```
