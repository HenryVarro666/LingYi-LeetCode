---
title: "1749. 任意子数组和的绝对值的最大值"
aliases: ["yiduobo的每日leetcode 1749.任意子数组和的绝对值的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/一-前缀和", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454878671"
zhihu_id: "454878671"
zhihu_title: "yiduobo的每日leetcode 1749.任意子数组和的绝对值的最大值"
question_id: "1749"
question: "任意子数组和的绝对值的最大值"
problem_url: "https://leetcode.cn/problems/maximum-absolute-sum-of-any-subarray/"
difficulty: "Medium"
rating: 1542
created: "2022-01-08T19:50:22+08:00"
updated: "2022-01-08T19:50:22+08:00"
upvotes: 0
comments: 0
---

# 1749. 任意子数组和的绝对值的最大值

> **[yiduobo的每日leetcode 1749.任意子数组和的绝对值的最大值](https://zhuanlan.zhihu.com/p/454878671) · 知乎 · 2022-01-08 · 赞同 0**
> 力扣：[1749. 任意子数组和的绝对值的最大值](https://leetcode.cn/problems/maximum-absolute-sum-of-any-subarray/) · Medium · 灵茶山艾府：[两种方法：动态规划/前缀和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1749.任意子数组和的绝对值的最大值

[力扣](https://leetcode-cn.com/problems/maximum-absolute-sum-of-any-subarray/)

子数组和的绝对值最大可以分为子数组和为正数以及子数组和为负数这两种情况。对于第一种情况，就是常规的最大子段和，可以使用贪心法来做。对于第二种情况，同样可以利用贪心法来做，将维护的值从当前位置结束的子数组和的最大值改成当前位置结束的子数组和的最小值就行了。

于是现在的做法就是一趟扫描，计算以每个位置结束的子数组和的最大值ma和最小值mi。若某一时刻ma小于0，那么就将其置为0；类似的，若某一时刻mi大于0，那么同样也将其置为0。得到当前位置的ma和mi之后，记得使用ma和-mi更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxAbsoluteSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = mi = 0
        res = 0
        for num in nums:
            ma += num
            if ma < 0:
                ma = 0
            mi += num
            if mi > 0:
                mi = 0
            
            res = max(res, ma, -mi)
        
        return res
```
