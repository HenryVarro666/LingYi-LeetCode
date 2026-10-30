---
title: "2654. 使数组所有元素变成1的最少操作次数"
aliases: ["yiduobo的每日leetcode 2654.使数组所有元素变成1的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/位运算", "题单/数学算法", "题单/位运算/三-与或-AND/OR-的性质", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647642158"
zhihu_id: "647642158"
zhihu_title: "yiduobo的每日leetcode 2654.使数组所有元素变成1的最少操作次数"
question_id: "2654"
question: "使数组所有元素变成 1 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/"
difficulty: "Medium"
rating: 1929
created: "2023-08-03T02:43:49+08:00"
updated: "2023-08-03T02:43:49+08:00"
upvotes: 2
comments: 0
---

# 2654. 使数组所有元素变成1的最少操作次数

> **[yiduobo的每日leetcode 2654.使数组所有元素变成1的最少操作次数](https://zhuanlan.zhihu.com/p/647642158) · 知乎 · 2023-08-03 · 赞同 2**
> 力扣：[2654. 使数组所有元素变成 1 的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/) · Medium · 灵茶山艾府：[两种方法：暴力枚举/利用GCD性质，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2654.使数组所有元素变为1的最少操作次数

[力扣](https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/)

首先，1和任意大于1的数的最大公约数都为1，因此只要数组中存在1，那么这个1就可以不断感染相邻的数，最终使得数组全都变为1。若数组中存在至少一个1，那么所需的操作次数就是数组的长度减去1的个数。

接下来对于数组中不存在1的情况，若数组中所有数的最大公约数大于1，那么无论怎么操作都无法得到1，此时直接返回-1。

若上面两种情况都不满足，那么就说明某个子数组的最大公约数为1，此时只需从这个子数组左边界开始，向右侧不断计算相邻数的最大公约数，同时使用这个得到的最大公约数替代靠右的这个数，那么最终在子数组的右边界上就会得到一个1，此时只需将这个1向两侧不断传播即可。不妨设这个子数组的长度为k，那么想得到1就需要k - 1次操作，而将1传播到整个数组则需要n - 1次操作，因此最终答案就是n + k - 2。

为了使得答案最小，就需要使得k最小，也就是说需要找出一个最大公约数为1的最短子数组。由于本题的数据规模比较小，因此直接枚举子数组的左右边界暴力计算就可以了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        cnt = 0
        for v in nums:
            if v == 1:
                cnt += 1
        
        if cnt > 0:
            return len(nums) - cnt

        g = nums[0]
        for v in nums[1:]:
            g = gcd(g, v)
        
        if g > 1:
            return -1
        
        mi = len(nums)
        for left in range(len(nums) - 1):
            g = nums[left]
            for right in range(left + 1, len(nums)):
                g = gcd(g, nums[right])
                if g == 1:
                    mi = min(mi, right - left + 1)
                    break
        
        return len(nums) + mi - 2
```
