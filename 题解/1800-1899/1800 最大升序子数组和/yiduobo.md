---
title: "1800. 最大升序子数组和"
aliases: ["yiduobo的每日leetcode 1800.最大升序子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463833231"
zhihu_id: "463833231"
zhihu_title: "yiduobo的每日leetcode 1800.最大升序子数组和"
question_id: "1800"
question: "最大升序子数组和"
problem_url: "https://leetcode.cn/problems/maximum-ascending-subarray-sum/"
created: "2022-02-03T21:34:08+08:00"
updated: "2022-02-03T21:34:09+08:00"
upvotes: 0
comments: 0
---

# 1800. 最大升序子数组和

> **[yiduobo的每日leetcode 1800.最大升序子数组和](https://zhuanlan.zhihu.com/p/463833231) · 知乎 · 2022-02-03 · 赞同 0**
> 力扣：[1800. 最大升序子数组和](https://leetcode.cn/problems/maximum-ascending-subarray-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1800.最大升序子数组和

[力扣](https://leetcode-cn.com/problems/maximum-ascending-subarray-sum/)

题目要求的是升序的子数组和，因此可以直接一趟遍历。对于当前的nums[index]，若其大于nums[index - 1]，那么将其加入到当前子数组和当中，否则使用当前子数组和更新答案，然后将当前子数组和重置为nums[index]。

遍历完成后，需要注意还需要使用最后这一个子数组的和更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxAscendingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = nums[0]
        res = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index - 1] >= nums[index]:
                res = max(res, now)
                now = nums[index]
            else:
                now += nums[index]
        
        return max(res, now)
```
