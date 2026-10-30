---
title: "2470. 最小公倍数为K的子数组数目"
aliases: ["yiduobo的每日leetcode 2470.最小公倍数为K的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587876991"
zhihu_id: "587876991"
zhihu_title: "yiduobo的每日leetcode 2470.最小公倍数为K的子数组数目"
question_id: "2470"
question: "最小公倍数等于 K 的子数组数目"
problem_url: "https://leetcode.cn/problems/number-of-subarrays-with-lcm-equal-to-k/"
difficulty: "Medium"
created: "2022-11-29T23:41:00+08:00"
updated: "2022-11-29T23:41:00+08:00"
upvotes: 1
comments: 0
---

# 2470. 最小公倍数为K的子数组数目

> **[yiduobo的每日leetcode 2470.最小公倍数为K的子数组数目](https://zhuanlan.zhihu.com/p/587876991) · 知乎 · 2022-11-29 · 赞同 1**
> 力扣：[2470. 最小公倍数等于 K 的子数组数目](https://leetcode.cn/problems/number-of-subarrays-with-lcm-equal-to-k/) · Medium · 灵茶山艾府：[两种做法：暴力 / 利用 LCM 的性质](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2470.最小公倍数为K的子数组数目

[力扣](https://leetcode.cn/problems/number-of-subarrays-with-lcm-equal-to-k/)

与之前的2447题类似，不过本题求要找的是最小公倍数为K的子数组。虽然看上去可以用滑动窗口，但是在窗口左边界移动向右移动时，很难直接得出新的子数组的最小公倍数是多少。分解质因数之后统计质因子的数目依然是可行的做法，不过比较麻烦，所以最后还是采用的暴力算法。

枚举子数组的左边界i，然后从i开始向后枚举子数组的右边界j并判断当前子数组的最小公倍数是否等于K。

最后附上python代码：

```python
class Solution(object):
    def subarrayLCM(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        res = 0
        for i in range(len(nums)):
            now = 1
            for j in range(i, len(nums)):
                g = gcd(now, nums[j])
                now = now * nums[j] / g
                if now == k:
                    res += 1
        
        return res
```
