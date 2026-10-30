---
title: "238. 除自身以外数组的乘积"
aliases: ["yiduobo的每日leetcode 238.除自身以外数组的乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/专题-前后缀分解", "题单/LeetCode-热题-100/普通数组", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150602411"
zhihu_id: "150602411"
zhihu_title: "yiduobo的每日leetcode 238.除自身以外数组的乘积"
question_id: "238"
question: "除了自身以外数组的乘积"
problem_url: "https://leetcode.cn/problems/product-of-array-except-self/"
difficulty: "Medium"
created: "2020-06-24T23:20:31+08:00"
updated: "2020-06-24T23:20:31+08:00"
upvotes: 0
comments: 0
---

# 238. 除自身以外数组的乘积

> **[yiduobo的每日leetcode 238.除自身以外数组的乘积](https://zhuanlan.zhihu.com/p/150602411) · 知乎 · 2020-06-24 · 赞同 0**
> 力扣：[238. 除了自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/) · Medium · 灵茶山艾府：[前后缀分解，附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

238.除自身以外数组的乘积<https://leetcode-cn.com/problems/product-of-array-except-self/>

由于题目要求不使用除法，那么对于第k个数，其结果就需要通过

nums[0] \* nums[1] \* ... \* nums[k - 1] \* nums[k + 1] \* ... \* nums[-2] \* nums[-1]

注意到这里从k分开，可以得到两个连续乘法的式子，于是可以利用前缀乘积和后缀乘积来进行优化，即从头到尾计算前缀乘积，然后从尾到头计算后缀乘积，然后一趟扫描逐个计算最终结果即可。

但是前缀乘积与后缀乘积都是需要O(n)的空间去储存的，要达成题目要求的O(1)空间，那么可以运用答案数组来储存其中一个乘积的结果，然后从另一侧使用一个数维护当前的乘积来替代数组。

于是现在的做法就变成：

1、从头到尾一趟扫描，将前缀乘积计算好并储存在答案数组res中。

2、从尾到头一趟扫描，使用一个变量now维护后缀乘积，那么对于第k个数，此时res[k - 1]储存了0到k - 1的前缀乘积，而now储存了k + 1到末尾的后缀乘积，于是有

res[k] \= res[k - 1] \* now

最后附上python代码：

```python
class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        if len(nums) < 2:
            return nums

        res = [nums[0]]
        for index in range(1, len(nums)):
            res.append(res[index - 1] * nums[index])

        now = 1
        for index in range(len(nums) - 1, 0, -1):
            res[index] = res[index - 1] * now
            now *= nums[index]
        
        res[0] = now

        return res
```
