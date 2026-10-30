---
title: "3284. 连续子数组的和"
aliases: ["yiduobo的每日leetcode 3284.连续子数组的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/841969064"
zhihu_id: "841969064"
zhihu_title: "yiduobo的每日leetcode 3284.连续子数组的和"
question_id: "3284"
question: "连续子数组的和"
problem_url: "https://leetcode.cn/problems/sum-of-consecutive-subarrays/"
created: "2024-10-06T22:01:57+08:00"
updated: "2024-10-06T22:01:57+08:00"
upvotes: 1
comments: 0
---

# 3284. 连续子数组的和

> **[yiduobo的每日leetcode 3284.连续子数组的和](https://zhuanlan.zhihu.com/p/841969064) · 知乎 · 2024-10-06 · 赞同 1**
> 力扣：[3284. 连续子数组的和](https://leetcode.cn/problems/sum-of-consecutive-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3284.连续子数组的和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-consecutive-subarrays/description/)

题目定义对于一个长度为n的数组arr，若对于所有的1 \<\= i \< n，都满足arr[i] - arr[i - 1] \=\= 1，或者对于所有的1 \<\= i \< n，都满足arr[i] - arr[i - 1] \=\= -1，那么就称arr是连续的。

给出一个整数数组nums，要求找出其中所有连续子数组的值之和。其中数组的值指的是数组元素之和。

需要注意，长度为1的数组也被认为是连续的。

题目的数据规模较大，直接暴力枚举肯定是不行的。注意到对于一个起点在p，终点在q的连续数组而言，任何满足p \<\= i \< j \< \= q的子数组nums[i : j + 1]依然是连续数组，也就是说在这里可以先将nums切分成尽量长的连续数组，然后对于每个连续数组计算其中所有子数组的值的和。

需要特别注意的是，题目中虽然表明了[3, 4, 3]不是连续数组，但是[3, 4]和[4, 3]都是连续数组，而长度为1的数组也被认为是连续的，那么如果对于[3, 4]和[4, 3]都计算了长度为1的子数组，那么[4]将会被计算两次，产生了重复。因此对于所有分离出来的子数组，应该先计算所有长度大于等于2的子数组的值的和，再将nums的和累加到答案中，也就是所有长度为1的子数组的和。

接下来需要解决的问题就是对于一个分离出的起点在p，终点在q的连续数组，应该如何计算其中所有长度大于等于2的子数组的值的和。

直接计算并不是很方便，我在这里采用的是贡献法，即计算p到q之间的每个元素出现在多少个长度大于等于2的子数组中，这个出现的次数乘以元素值就是这个元素的贡献。

具体来说，对于p到q之间的下标index，其所在子数组的左边界可以在p到index之间，一共有index - p + 1种可行的取值；而右边界则可以在index到q之间，一共有q - index + 1种可行的取值。综合起来，nums[index]将会出现在(index - p + 1) \* (q - index + 1)个子数组中。需要特别注意的是，当左边界和右边界同时取index时，得到的子数组长度为1，需要排除掉这种情况，因此nums[index]在所有长度大于等于2的子数组中的贡献值就是nums[index] \* ((index - p + 1) \* (q - index + 1) - 1)。

到了这里就得到了一种可行的处理方法。使用两个变量p和q向后迭代，将所有长度大于等于2的连续数组分离出来。对于当前分离出来的连续数组nums[p : q + 1]，枚举p到q之间的所有下标index，通过上面的式子计算nums[index]的贡献。计算完所有连续子数组后，再将nums之和累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def getSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        res = sum(nums) % mod

        p = 0
        while p < len(nums):
            if p + 1 == len(nums) or abs(nums[p] - nums[p + 1]) != 1:
                p += 1
            else:
                q = p + 1
                diff = nums[q] - nums[p]
                while q + 1 < len(nums) and nums[q + 1] - nums[q] == diff:
                    q += 1
                for index in range(p, q + 1):
                    res += nums[index] * ((index - p + 1) * (q - index + 1) - 1)
                    res %= mod
                
                p = q
        
        return res
```
