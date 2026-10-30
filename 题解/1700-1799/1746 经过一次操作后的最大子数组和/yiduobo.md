---
title: "1746. 经过一次操作后的最大子数组和"
aliases: ["yiduobo的每日leetcode 1746.经过一次操作后的最大子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620573019"
zhihu_id: "620573019"
zhihu_title: "yiduobo的每日leetcode 1746.经过一次操作后的最大子数组和"
question_id: "1746"
question: "经过一次操作后的最大子数组和"
problem_url: "https://leetcode.cn/problems/maximum-subarray-sum-after-one-operation/"
created: "2023-04-09T18:59:45+08:00"
updated: "2023-04-09T18:59:45+08:00"
upvotes: 0
comments: 0
---

# 1746. 经过一次操作后的最大子数组和

> **[yiduobo的每日leetcode 1746.经过一次操作后的最大子数组和](https://zhuanlan.zhihu.com/p/620573019) · 知乎 · 2023-04-09 · 赞同 0**
> 力扣：[1746. 经过一次操作后的最大子数组和](https://leetcode.cn/problems/maximum-subarray-sum-after-one-operation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1746.经过一次操作后的最大子数组和

[力扣](https://leetcode.cn/problems/maximum-subarray-sum-after-one-operation/)

经典问题最大子段和的升级版，可以使用动态规划来求解。

令f[i]表示以nums[i]结尾的最大子段和，这里的子段长度可以为0。令g[i]表示以nums[i]为结尾，且已经进行过一次操作的最大子段和。

那么对于f[i]和g[i]：

1、f[i]只能在f[i - 1]的基础上将nums[i]加入进来，那么就有f[i] \= max(f[i - 1] + nums[i], 0)

2、g[i]则可以选择在g[i - 1]的基础上将nums[i]加入进来，或者在f[i - 1]的基础上将nums[i] \* nums[i]加入景来，那么就有g[i] \= max(g[i - 1] + nums[i], f[i - 1] + nums[i] \* nums[i])

计算完成后，max(g)即为最终答案。

另外注意到f和g都只与上一轮的结果有关，因此在这里可以使用遍历迭代节省数组空间。

最后附上python代码：

```python
class Solution(object):
    def maxSumAfterOperation(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = g = res = 0
        for num in nums:
            g = max(g + num, f + num * num)
            f = max(f + num, 0)
            res = max(res, g)

        return res
```
