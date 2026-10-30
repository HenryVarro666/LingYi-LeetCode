---
title: "4072. 一次删除后的最大交替子数组和"
aliases: ["yiduobo的每日leetcode 4072.一次删除后的最大交替子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2090613387118039266"
zhihu_id: "2090613387118039266"
zhihu_title: "yiduobo的每日leetcode 4072.一次删除后的最大交替子数组和"
question_id: "4072"
question: "一次删除后的最大交替子数组和"
problem_url: "https://leetcode.cn/problems/maximum-alternating-subarray-sum-with-one-deletion/"
created: "2026-10-07T01:14:16+08:00"
updated: "2026-10-07T01:14:16+08:00"
upvotes: 1
comments: 0
---

# 4072. 一次删除后的最大交替子数组和

> **[yiduobo的每日leetcode 4072.一次删除后的最大交替子数组和](https://zhuanlan.zhihu.com/p/2090613387118039266) · 知乎 · 2026-10-07 · 赞同 1**
> 力扣：[4072. 一次删除后的最大交替子数组和](https://leetcode.cn/problems/maximum-alternating-subarray-sum-with-one-deletion/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4072.一次删除后的最大交替子数组和

<https://leetcode.cn/problems/maximum-alternating-subarray-sum-with-one-deletion/description/>

题目给出一个整数数组nums。现在可以从nums中删除至多一个元素，然后在剩下的数组中选取一个子数组。

问这个子数组的交替和最大可能是多少。

交替和指的是对于一个数组(下标从0开始)，其中偶数下标处的元素之和减去奇数下标处的元素之和。

如果不考虑删除操作，那么在这里就可以令f[index]和g[index]分别表示以index结尾的子数组，且子数组中最后一个元素是被加进去/减掉时的最大交替子数组和。那么对于f[index]，可以从nums[index]起另立门户，也可以接在g[index - 1]后面，而对于g[index]，则只能接在f[index - 1]的后面。这样一趟遍历迭代下来，取f和g中的最大值即为最终答案。

对于本题， 可以执行最多一次删除操作，那么最直观的思路就是将其融入到状态表示中：f[index]与g[index]在没有执行过删除操作这一前提下保持原意，另外h[index]与t[index]则表示执行过删除操作后，以index结尾的子数组(这里的index可能在这一轮被删掉，但是不影响)，且子数组中最后一个元素是被加进去/减掉时的最大交替子数组和。那么:

1、f和g的更新保持不变

2、对于h[index]，可以接在t[index - 1]后面，也可以是在f[index - 1]的前提下删掉nums[index]，因此在这里就应该用f[index - 1]以及t[index - 1] + nums[index]中的较大值来更新h[index]

3、对于t[index]，可以接在h[index - 1]后面，也可以是在g[index - 1]的前提下删掉nums[index]，因此在这里就应该用g[index - 1]以及h[index - 1] - nums[index]中的较大值来更新t[index]

于是依然是一趟遍历，取这四个数组中的最大值即可。

注意到这四个数组每一轮都是从上一轮互相迭代过来的，因此在这里可以使用四个变量进行迭代来节省空间。

最后附上python代码：

```python
class Solution(object):
    def maxAlternatingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        f, g, h, t = nums[0], None, None, None
        res = nums[0]
        for v in nums[1:]:
            pre_f, pre_g, pre_h, pre_t = f, g, h, t
            f = v
            if pre_g is not None and pre_g > 0:
                f += pre_g
            res = max(res, f)

            g = pre_f - v
            res = max(res, g)

            h = pre_f
            if pre_t is not None:
                h = max(h, pre_t + v)
            res = max(res, h)

            t = None
            if pre_g is not None:
                t = pre_g
            if pre_h is not None and (t is None or t < pre_h - v):
                t = pre_h - v
                
            if t is not None:
                res = max(res, t)

        return res
```
