---
title: "2495. 乘积为偶数的子数组数"
aliases: ["yiduobo的每日leetcode 2495.乘积为偶数的子数组数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632746656"
zhihu_id: "632746656"
zhihu_title: "yiduobo的每日leetcode 2495.乘积为偶数的子数组数"
question_id: "2495"
question: "乘积为偶数的子数组数"
problem_url: "https://leetcode.cn/problems/number-of-subarrays-having-even-product/"
created: "2023-05-28T02:00:55+08:00"
updated: "2023-05-28T02:00:55+08:00"
upvotes: 1
comments: 0
---

# 2495. 乘积为偶数的子数组数

> **[yiduobo的每日leetcode 2495.乘积为偶数的子数组数](https://zhuanlan.zhihu.com/p/632746656) · 知乎 · 2023-05-28 · 赞同 1**
> 力扣：[2495. 乘积为偶数的子数组数](https://leetcode.cn/problems/number-of-subarrays-having-even-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2495.乘积为偶数的子数组数

[力扣](https://leetcode.cn/problems/number-of-subarrays-having-even-product/)

对于数组中的任意子数组，只需其中存在一个偶数，该子数组的乘积就是偶数。为了避免重复计算，在这里可以对于数组中的每个偶数，统计以该偶数为最右侧偶数的子数组数量。

对于某个偶数出现的位置p，找出其左侧最近的偶数下标pre，那么如果pre是子数组中的最右侧偶数，其左边界可以延伸到原数组的最左侧，也就是下标0，而右边界则只能延伸到p - 1，因为p是偶数。综合起来，就一共有(pre + 1) \* (p - pre)种可能的子数组。

根据这个结论，就只需一趟遍历，对于每个pre找到对应的p，计算子数组数量并累加到答案后将pre迭代为p，然后重复此过程直到来到数组末尾。

```python
class Solution(object):
    def evenProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        pre = 0
        while pre < len(nums) and nums[pre] % 2 == 1:
            pre += 1
        
        p = pre + 1
        res = 0
        while pre < len(nums):
            while p < len(nums) and nums[p] % 2 == 1:
                p += 1
            
            res += (p - pre) * (pre + 1)
            pre = p
            p += 1
        
        return res
```
