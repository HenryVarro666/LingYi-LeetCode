---
title: "2524. 子数组的最大频率分数"
aliases: ["yiduobo的每日leetcode 2524.子数组的最大频率分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636190668"
zhihu_id: "636190668"
zhihu_title: "yiduobo的每日leetcode 2524.子数组的最大频率分数"
question_id: "2524"
question: "子数组的最大频率分数"
problem_url: "https://leetcode.cn/problems/maximum-frequency-score-of-a-subarray/"
difficulty: "Hard"
created: "2023-06-11T01:12:37+08:00"
updated: "2023-06-11T01:12:37+08:00"
upvotes: 0
comments: 0
---

# 2524. 子数组的最大频率分数

> **[yiduobo的每日leetcode 2524.子数组的最大频率分数](https://zhuanlan.zhihu.com/p/636190668) · 知乎 · 2023-06-11 · 赞同 0**
> 力扣：[2524. 子数组的最大频率分数](https://leetcode.cn/problems/maximum-frequency-score-of-a-subarray/) · Hard · 灵茶山艾府：[线性做法，不用快速幂（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2524.子数组的最大频率分数

[力扣](https://leetcode.cn/problems/maximum-frequency-score-of-a-subarray/)

题目要计算每个长度为k的子数组的频率分数，很明显是一个滑动窗口的题目。

最初始的由数组中前k个数组成的滑动窗口的频率分数是很好计算的，只需遍历数组中的前k个数，使用一个哈希表cnt记录每种数字出现的次数，然后按照题目给出的计算方法计算初始状态下的频率分数就行了。

接下来需要解决的问题则是当窗口开始向后滑动时，如何根据上一轮的频率分数计算本轮的频率分数。

首先考虑特殊情况。若窗口滑动时新进入的数字与被滑出的数字相同，那么频率分数就不会发生变化，此时无需进行任何处理。

接下来是一般情况。

不妨设新进入的数字为x，若其之前没有在滑动窗口中出现过，那么频率分数就需要加上x的1次方，也就是x。若其之前出现过，不妨设之前出现了cnt[x]次，那么x对频率分数的贡献就由x^cnt[x]变成了x^(cnt[x] + 1)，在这里只需减去前者然后加上后者就行了。需要注意的是cnt[x]可能很大，所以在这里需要使用快速幂来计算这个乘方。

另一方面，对于被滑出的数字，不妨设其为y，那么同样是讨论其在上一轮的出现次数cnt[y]。在这里需要先减去y^cnt[y]，接下来若cnt[y]等于1，那么说明y不会再对频率分数产生影响，否则的话y产生的影响就从y^cnt[y]变成了y^(cnt[y] - 1)，在这里需要额外再加上y^(cnt[y] - 1)。同样的，在这里也需要使用快速幂。

当频率分数被更新后，使用当前的频率分数更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxFrequencyScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """            

        mod = 10 ** 9 + 7
        cnt = {}
        for num in nums[:k]:
            cnt[num] = cnt.get(num, 0) + 1

        def quickPow(base, x):
            if x == 1:
                return base
            
            p = quickPow(base, x / 2)
            p *= p
            if x & 1:
                p *= base
            
            return p % mod

        now = 0
        for num in cnt:
            now += quickPow(num, cnt[num])
            if now >= mod:
                now -= mod
        
        res = now
        for index, num in enumerate(nums[k:]):
            if num == nums[index]:
                continue
            
            if num not in cnt:
                now += num
                if now >= mod:
                    now -= mod
                cnt[num] = 1
            else:               
                now -= quickPow(num, cnt[num])
                if now < 0:
                    now += mod
                cnt[num] += 1
                now += quickPow(num, cnt[num])
                if now >= mod:
                    now -= mod
            
            now -= quickPow(nums[index], cnt[nums[index]])
            if now < 0:
                now += mod
            cnt[nums[index]] -= 1
            if cnt[nums[index]] == 0:
                cnt.pop(nums[index])
            else:
                now += quickPow(nums[index], cnt[nums[index]])
                if now >= mod:
                    now -= mod

            res = max(res, now)
        
        return res
```
