---
title: "689. 三个无重叠子数组的最大和"
aliases: ["yiduobo的每日leetcode 689.三个无重叠子数组的最大和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/308453808"
zhihu_id: "308453808"
zhihu_title: "yiduobo的每日leetcode 689.三个无重叠子数组的最大和"
question_id: "689"
question: "三个无重叠子数组的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-3-non-overlapping-subarrays/"
created: "2020-11-23T21:27:30+08:00"
updated: "2020-11-23T21:27:30+08:00"
upvotes: 0
comments: 0
---

# 689. 三个无重叠子数组的最大和

> **[yiduobo的每日leetcode 689.三个无重叠子数组的最大和](https://zhuanlan.zhihu.com/p/308453808) · 知乎 · 2020-11-23 · 赞同 0**
> 力扣：[689. 三个无重叠子数组的最大和](https://leetcode.cn/problems/maximum-sum-of-3-non-overlapping-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

689.三个无重叠子数组的最大和

[力扣](https://leetcode-cn.com/problems/maximum-sum-of-3-non-overlapping-subarrays/)

题目要求从nums中找出三段连续的长为k的子数组，使得这三段子数组的和最大。由于k是确定的，因此我们可以先预处理出一个子数组和数组f，f[index]表示从index到index + k - 1这一段子数组之和。

那么首先最朴素的做法自然是枚举三段的起始位置，这个做法是O(n^3)的。

注意到我们在枚举完第一段和第二段的起始位置之后，设第二段的起始位置为index，那么我们接下来需要从index + k到数组尾部这一段中找出p，使得f[p]最大。于是我们可以使用一个数组right_max来记录这个位置。

设right_max\[index\]表示从index到数组尾部这一段中最大的f的位置，那么对于index而言，若f\[right_max\[index + 1\]\] \<\= f\[index\]，那么right_max\[index\] \= index，否则right_max\[index\] \= right_max\[index + 1\]。这里的小于等于是因为题目要求字典序最小的结果，因此我们要尽量让right_max的位置往前靠。

有了right_max，我们现在的做法就是枚举第一段和第二段的起始位置，设第二段的起始位置为index，那么第三段的起始位置就必然是right_max[index + k]了。成功将时间复杂度优化到了O(n^2)。

更进一步的，既然能有right_max，那么自然也可以求出left_max，其中left_max\[index\]表示从0到index这一段中最大的f的位置。对于index而言，若f\[left_max\[index - 1\]\] \< f\[index\]，那么left_max\[index\] \= index，否则left_max\[index\] \= left_max\[index - 1\]。注意这里的比较条件应该是严格小于，理由同样是为了满足字典序最小。

到了这里，我们就只需要枚举第二段的起始位置index，那么第一段的起始位置就是left_max[index - k]，而第三段的起始位置则是right_max[index + k]，最终的时间复杂度就优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def maxSumOfThreeSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        f = [0]
        for index in range(k):
            f[0] += nums[index]
        for index in range(k, len(nums)):
            f.append(f[-1] + nums[index] - nums[index - k])
        
        left_max = [0]
        for index in range(1, len(f)):
            if f[index] > f[left_max[-1]]:
                left_max.append(index)
            else:
                left_max.append(left_max[-1])
        
        right_max = [len(f) - 1]
        for index in range(len(f) - 1, -1, -1):
            if f[index] >= f[right_max[-1]]:
                right_max.append(index)
            else:
                right_max.append(right_max[-1])
        
        right_max.reverse()

        max_sum = 0
        max_pos = []

        for index in range(k, len(f) - k):
            left_pos = left_max[index - k]
            right_pos = right_max[index + k]
            if f[left_pos] + f[right_pos] + f[index] > max_sum:
                max_sum = f[left_pos] + f[right_pos] + f[index]
                max_pos = [left_pos, index, right_pos]
        
        return max_pos
```
