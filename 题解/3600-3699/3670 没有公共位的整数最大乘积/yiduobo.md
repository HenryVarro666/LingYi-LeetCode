---
title: "3670. 没有公共位的整数最大乘积"
aliases: ["yiduobo的每日leetcode 3670.没有公共位的整数最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/bao-li", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950333634444759702"
zhihu_id: "1950333634444759702"
zhihu_title: "yiduobo的每日leetcode 3670.没有公共位的整数最大乘积"
question_id: "3670"
question: "没有公共位的整数最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-two-integers-with-no-common-bits/"
difficulty: "Medium"
rating: 2234
created: "2025-09-20T01:48:25+08:00"
updated: "2025-09-20T01:48:27+08:00"
upvotes: 0
comments: 0
---

# 3670. 没有公共位的整数最大乘积

> **[yiduobo的每日leetcode 3670.没有公共位的整数最大乘积](https://zhuanlan.zhihu.com/p/1950333634444759702) · 知乎 · 2025-09-20 · 赞同 0**
> 力扣：[3670. 没有公共位的整数最大乘积](https://leetcode.cn/problems/maximum-product-of-two-integers-with-no-common-bits/) · Medium · 灵茶山艾府：[两种方法：普通状压 DP / 高维前缀和（SOS DP）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3670.没有公共位的整数最大乘积

<https://leetcode.cn/problems/maximum-product-of-two-integers-with-no-common-bits/description/>

题目给出一个整数数组nums，长度可达10^5，其中元素的大小在1到10^6之间。现在要求从中找出两个不同的下标i和j，使得nums[i]与nums[j]的乘积最大化，且nums[i]和nums[j]的二进制表示中没有任何公共的置位。

返回最大的乘积，若不存在合法的数对，则返回0。

题目的数据规模较大，直接暴力显然是不行的。如果从数对的角度考虑，就只能枚举其中一个元素nums[i]，找出能与之配对的最优元素nums[j]是什么；如果从值域的角度考虑，那么就是枚举第一个元素的值，考虑能与之配对且存在的最大值是什么。我在这里只考虑了第一种处理方法，不过也找到了可行的方案。

由于题目合法数对与二进制的置位有关，那么在这里就可以先通过nums中最大值的二进制表示的长度m，来确定二进制表示的上界max_state，也就是(1 \<\< m) - 1。接下来，对于nums[i]和nums[j]的二进制置位中没有任何公共的置位，可以理解成对于nums[i]，其消耗掉了nums[i]的这些位，剩下的位为max_state ^ nums[i]，而nums[j]就是max_state ^ nums[i]的所有子状态中数值最大的那一个。

接下来的问题就是如何找到这些子状态中的最大值。令f[state]表示state的所有子状态中的最大值，那么对于f[state]，若state本身是nums中的某个元素，那么就有f[state] \= state，否则就需要从state所有子状态中选取f值最大的那一个作为f[state]的值。直接暴力遍历所有的子状态复杂度就太高了，在这里可以尝试遍历state二进制中所有1所在的位p，使用f[state ^ (1 \<\< p)]中的最大值来更新f[state]。理由是state的所有子状态都可以通过从state中去掉某些1得到，而去掉多个1的状态必然是某个只去掉一个1的状态的子状态，也就是说在这里不需要一步到位，从具体的最优子状态更新到f[state]，而是只需要使用所有的f[state ^ (1 \<\< p)]来更新f[state]就行了。

在具体实现上，可以通过lowbit来分离所有值为1的位，而不需要遍历所有的位。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = max(nums)
        max_state = 1
        while max_state <= ma:
            max_state <<= 1
        max_state -= 1
        
        f = [0] * (max_state + 1)
        num_set = set(nums)
        for x in range(1, max_state + 1):
            if x in num_set:
                f[x] = x
            else:
                v = x
                while v:
                    b = v & -v
                    pre = f[x ^ b]
                    if pre > f[x]:
                        f[x] = pre
                    v ^= b
        
        res = 0
        for x in num_set:
            res = max(res, f[max_state ^ x] * x)
        return res
```
