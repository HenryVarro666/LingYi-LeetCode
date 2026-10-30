---
title: "523. 连续的子数组和"
aliases: ["yiduobo的每日leetcode 523.连续的子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261032244"
zhihu_id: "261032244"
zhihu_title: "yiduobo的每日leetcode 523.连续的子数组和"
question_id: "523"
question: "连续的子数组和"
problem_url: "https://leetcode.cn/problems/continuous-subarray-sum/"
created: "2020-10-01T23:33:06+08:00"
updated: "2020-10-01T23:33:06+08:00"
upvotes: 0
comments: 0
---

# 523. 连续的子数组和

> **[yiduobo的每日leetcode 523.连续的子数组和](https://zhuanlan.zhihu.com/p/261032244) · 知乎 · 2020-10-01 · 赞同 0**
> 力扣：[523. 连续的子数组和](https://leetcode.cn/problems/continuous-subarray-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

523.连续的子数组和<https://leetcode-cn.com/problems/continuous-subarray-sum/>

题目需要判断数组中是否存在一组l和r，满足r >\= l + 1，且

S \= nums[l] + nums[l + 1] + ... + nums[r] \= n \* k

我们将这个式子变形，加上l之前的项，就可以得到

S \= nums[0] + nums[1] + ... + nums[l - 1] + nums[l] + ... + nums[r] -

nums[0] - nums[1] - ... - nums[l - 1]

可以看出，上面这一行就是prefix_sum[r]，而下面这一行则是prefix[l - 1]，即

S \= prefix_sum[r] - prefix_sum[l - 1] \= n \* k

到了这里，目标就是找出一组l和r，满足r >\= l + 1，且

prefix_sum[l - 1] \= x \* k + m

prefix_sum[r] \= y \* k + m

于是现在的思路就是从头到尾一趟扫描，求前缀和的同时将其对k取模得到余数m，并使用dict将保存这些余数首次出现的位置。当某个余数已经在dict中出现过时，检测当前的位置与上次出现的位置之间的间隔是否大于等于2即可。

另外，需要特别注意k\=0的情况，此时不能通过模k来做。由于题目保证数组中的数非负，那么此时如果有解，就必然存在两个连续出现的0，直接进行特殊判断即可。

最后附上python代码：

```python
class Solution(object):
    def checkSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        if len(nums) < 2:
            return False
        
        if k == 0:
            for index in range(1, len(nums)):
                if nums[index] == 0 and nums[index - 1] == 0:
                    return True
            return False

        sum_dict = {0: -1}
        now = nums[0] % k
        if now not in sum_dict:
            sum_dict[now] = 0

        for index in range(1, len(nums)):
            now += nums[index]
            now %= k
            if now in sum_dict:
                if index - sum_dict[now] >= 2:
                    return True
            else:
                sum_dict[now] = index

        return False
```
