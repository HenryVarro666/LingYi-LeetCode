---
title: "1262. 可被三整除的最大和"
aliases: ["yiduobo的每日leetcode 1262.可被三整除的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/贪心算法", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386932766"
zhihu_id: "386932766"
zhihu_title: "yiduobo的每日leetcode 1262.可被三整除的最大和"
question_id: "1262"
question: "可被三整除的最大和"
problem_url: "https://leetcode.cn/problems/greatest-sum-divisible-by-three/"
difficulty: "Medium"
rating: 1762
created: "2021-07-05T22:37:48+08:00"
updated: "2021-07-05T22:37:48+08:00"
upvotes: 0
comments: 0
---

# 1262. 可被三整除的最大和

> **[yiduobo的每日leetcode 1262.可被三整除的最大和](https://zhuanlan.zhihu.com/p/386932766) · 知乎 · 2021-07-05 · 赞同 0**
> 力扣：[1262. 可被三整除的最大和](https://leetcode.cn/problems/greatest-sum-divisible-by-three/) · Medium · 灵茶山艾府：[两种算法：贪心/动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1262.可被三整除的最大和

[力扣](https://leetcode-cn.com/problems/greatest-sum-divisible-by-three/)

我们先计算出所有数之和s，那么s有三种可能：

1、s可以被三整除，那么此时s就是最终答案

2、s模三余一，那么此时我们可以从数组中剔除一个模三余一的数，或者剔除两个模三余二的数，原因是两个模三余二的数之和模三是余一的。

3、s模三余二，那么此时我们可以从数组中剔除一个模三余二的数，或者剔除两个模三余一的数，原因是两个模三余一的数之和模三是余二的。

为了使得和最大，因此我们自然是选择剔除最小的数，于是我们可以先一趟扫描，找出所有数中最小的两个模三余一的数以及最小的两个模三余二的数，同时算出所有数之和。接下来我们只需根据s模三的余数，按照上面三种情况剔除掉需要对应的数即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumDivThree(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = 0
        min1 = [0, 0]
        min2 = [0, 0]
        for num in nums:
            s += num
            if num % 3 == 1:
                if min1[0] == 0 or min1[0] > num:
                    min1[1] = min1[0]
                    min1[0] = num
                elif min1[1] == 0 or min1[1] > num:
                    min1[1] = num
            elif num % 3 == 2:
                if min2[0] == 0 or min2[0] > num:
                    min2[1] = min2[0]
                    min2[0] = num
                elif min2[1] == 0 or min2[1] > num:
                    min2[1] = num
        
        if s % 3 == 0:
            return s

        res = 0

        if s % 3 == 1:
            if min1[0] > 0:
                res = max(res, s - min1[0])
            if min2[1] > 0:
                res = max(res, s - min2[0] - min2[1])
            return res
        
        if s % 3 == 2:
            if min2[0] > 0:
                res = max(res, s - min2[0])
            if min1[1] > 0:
                res = max(res, s - min1[0] - min1[1])
            return res
```
