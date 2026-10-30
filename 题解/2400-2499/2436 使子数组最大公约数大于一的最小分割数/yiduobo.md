---
title: "2436. 使子数组最大公约数大于一的最小分割数"
aliases: ["yiduobo的每日leetcode 2436.使子数组最大公约数大于一的最小分割数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631686957"
zhihu_id: "631686957"
zhihu_title: "yiduobo的每日leetcode 2436.使子数组最大公约数大于一的最小分割数"
question_id: "2436"
question: "使子数组最大公约数大于一的最小分割数"
problem_url: "https://leetcode.cn/problems/minimum-split-into-subarrays-with-gcd-greater-than-one/"
created: "2023-05-23T23:35:43+08:00"
updated: "2023-05-23T23:35:43+08:00"
upvotes: 0
comments: 0
---

# 2436. 使子数组最大公约数大于一的最小分割数

> **[yiduobo的每日leetcode 2436.使子数组最大公约数大于一的最小分割数](https://zhuanlan.zhihu.com/p/631686957) · 知乎 · 2023-05-23 · 赞同 0**
> 力扣：[2436. 使子数组最大公约数大于一的最小分割数](https://leetcode.cn/problems/minimum-split-into-subarrays-with-gcd-greater-than-one/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2436.使子数组最大公约数大于一的最小分割数

[力扣](https://leetcode.cn/problems/minimum-split-into-subarrays-with-gcd-greater-than-one/)

对于一个最大公约数大于一的子数组而言，如果往里面添加更多的数，这个子数组的最大公约数必然是越来越小的。不妨考虑第一个子数组：对于这个子数组，如果其右侧的第一个数加入该子数组后最大公约数依然大于一，那么就应该将其加入其中，减轻后续子数组划分的压力。更进一步的，可以从头开始向后一趟遍历，对于每个数都尽量将其加入到当前的子数组中，若无法加入，那么就另起一个新的子数组。

最后附上python代码：

```python
class Solution(object):
    def minimumSplits(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 1
        now = nums[0]

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for num in nums[1:]:
            g = gcd(num, now)
            if g == 1:
                res += 1
                now = num
            else:
                now = g
        
        return res
```
