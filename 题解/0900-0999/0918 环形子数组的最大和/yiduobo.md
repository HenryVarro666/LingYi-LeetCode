---
title: "918. 环形子数组的最大和"
aliases: ["yiduobo的每日leetcode 918.环形子数组的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/一-入门-DP", "题单/面试经典-150-题/Kadane-算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355595375"
zhihu_id: "355595375"
zhihu_title: "yiduobo的每日leetcode 918.环形子数组的最大和"
question_id: "918"
question: "环形子数组的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-circular-subarray/"
difficulty: "Medium"
rating: 1777
created: "2021-03-08T23:07:17+08:00"
updated: "2021-03-08T23:07:17+08:00"
upvotes: 0
comments: 0
---

# 918. 环形子数组的最大和

> **[yiduobo的每日leetcode 918.环形子数组的最大和](https://zhuanlan.zhihu.com/p/355595375) · 知乎 · 2021-03-08 · 赞同 0**
> 力扣：[918. 环形子数组的最大和](https://leetcode.cn/problems/maximum-sum-circular-subarray/) · Medium · 灵茶山艾府：[【图解】正难则反，一张图秒懂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

918.环形子数组的最大和

[力扣](https://leetcode-cn.com/problems/maximum-sum-circular-subarray/)

首先，我们考虑特殊情况。当数组中的所有数到小于等于0时，此时的答案就是数组中的最大值，那么我们应当首先通过一次循环判断这种情况。

接下来，最大子段和问题在环形数组的情况下，无外乎两种可能。第一种就是普通的连续一段，而另一种则是首尾两段。

对于普通的连续一段这个问题，可以使用的经典的贪心法来处理。贪心法的思路为加入当前数之后若子段和小于0，那么就应该从下一个数重新开始，因此将当前子段和置为0，否则就将当前数加入当前子段，然后更新答案。

对于后面这种首尾两段的问题，则可以将其看成一个数组，我们需要从中间去除掉一个子段，同时要求这个子段和最小。那么去除掉这个子段之后，剩下的首尾两段之后自然就是最大的。于是问题转化成了一个最小子段和问题，同样可以使用经典的贪心法来处理。求解出最小子段和之后，用整个数组的和减去最小子段和即为首尾两段的最大子段和。

最后附上python代码：

```python
class Solution(object):
    def maxSubarraySumCircular(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        flag = True
        for num in A:
            if num > 0:
                flag = False
                break
            
        if flag:
            return max(A)

        res = 0
        now = 0
        for num in A:
            now += num
            if now < 0:
                now = 0
            res = max(res, now)

        now = 0
        s = sum(A)
        for num in A:
            now += num
            if now > 0:
                now = 0
            res = max(res, s - now)

        return res
```
