---
title: "2818. 操作使得分最大"
aliases: ["yiduobo的每日leetcode 2818.操作使得分最大"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/number-theory", "leetcode/monotonic-stack", "题单/单调栈", "题单/数学算法", "题单/单调栈/三-贡献法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658814104"
zhihu_id: "658814104"
zhihu_title: "yiduobo的每日leetcode 2818.操作使得分最大"
question_id: "2818"
question: "操作使得分最大"
problem_url: "https://leetcode.cn/problems/apply-operations-to-maximize-score/"
difficulty: "Hard"
rating: 2397
created: "2023-09-28T04:32:18+08:00"
updated: "2023-09-28T04:32:18+08:00"
upvotes: 0
comments: 0
---

# 2818. 操作使得分最大

> **[yiduobo的每日leetcode 2818.操作使得分最大](https://zhuanlan.zhihu.com/p/658814104) · 知乎 · 2023-09-28 · 赞同 0**
> 力扣：[2818. 操作使得分最大](https://leetcode.cn/problems/apply-operations-to-maximize-score/) · Hard · 灵茶山艾府：[贡献法+单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2818.操作使得分最大

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/apply-operations-to-maximize-score/description/)

题目的描述比较复杂，不妨从结果出发一步步反推。

题目要求经过k步操作，使得最终得分最大，其中的操作就是简单的乘法，而nums中的数都是正数，这也就意味着应该尽量选择数值较大的数进行操作。

不过根据题目的描述，每个位置上的数的使用次数是有限制的，具体来说，对于位置index上的数，一共有(index + 1) \* (n - index)个子数组包含这个数，而对于这些子数组，若其中有m个子数组中拥有最多质因子的数都是nums[index]，那么nums[index]就可以使用m次。那么对于这个问题，就有两个子问题需要处理：

1、对数组中的每个数分解质因数，计算出质因子的数量

对于这个问题，直接计算的复杂度较高，不过注意到所有数的大小不超过10^5，那么可以先计算出这个范围内的质数。另外由于是用作分解质因数，那么实际上只需要计算出范围在sqrt(10^5)内的质数就行了，我在这里取了个大概，计算了400之内的质数。

接下来只需一趟遍历，对于数组中的每个数v，利用上面计算出来的质数表进行分解质因数就行了。需要注意的是这里的v可能由一个较小的质数与一个较大的质数相乘得到，因此最终分解的结果可能不为1，那么此时剩下的一定是一个大于400的质数，因此还需要将其质因子的数量加上1。

全部计算完成后，记nums[index]的质因子数量为cnt[index]。

2、对于上一步中计算得到的cnt[index]，计算有多少个子数组中的最大值是cnt[index]

对于这个问题，可以转化为经典的左侧和右侧第一个更大值的位置。具体来说，设left为index左侧最大的，且满足cnt[left] >\= cnt[index]的位置left，设right为index右侧最大的，且满足cnt[right] > cnt[index]的位置right，那么左边界在left + 1到index之间，同时右边界在index到right - 1之间的所有子数组都是满足条件的子数组。

需要注意这里左侧是大于等于，而右侧是严格大于，这是因为题目对于质因子数量相同的数只能选择最左侧的那个数。而对于上面的问题，则是经典的单调栈问题，可以参考之前的496题

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

到了这里，就可以计算出数组中的每个数可以使用多少次，接下来只需将数值和可用次数打包后，按数值从大到小进行排序，然后一趟遍历。对于当前遍历到的数值v和可用次数freq，若freq小于可操作次数k，那么就将v^freq累乘到答案中然后将k减去freq，否则将v^k累乘到答案中并返回。由于这里的freq和k可能很大，因此还需要使用快速幂来计算这个乘方。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        p = range(400)
        x = 2
        while x * x <= 400:
            if p[x] == x:
                for y in range(x + x, 400, x):
                    p[y] = x
            
            if x == 2:
                x += 1
            else:
                x += 2

        prime_list = []
        for x in range(2, 400):
            if p[x] == x:
                prime_list.append(x)

        cnt = {}
        for v in nums:
            if v not in cnt:
                x = v
                cnt[v] = 0
                for y in prime_list:
                    if y > x:
                        break
                    if x % y == 0:
                        while x % y == 0:
                            x /= y
                        cnt[v] += 1

                if x > 1:
                    cnt[v] += 1
                

        n = len(nums)
        right = [n] * n
        stack = []
        for index in range(n):
            v = nums[index]
            while stack and cnt[nums[stack[-1]]] < cnt[v]:
                right[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        left = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            while stack and cnt[nums[stack[-1]]] <= cnt[v]:
                left[stack[-1]] = index
                stack.pop()
            
            stack.append(index)

        mod = 10 ** 9 + 7
        res = 1
        
        def quickPow(base, x):
            if x == 1:
                return base
            
            tmp = quickPow(base, x / 2)
            tmp *= tmp
            tmp %= mod

            if x % 2 == 1:
                tmp *= base
                tmp %= mod
            
            return tmp

        for v, freq in sorted([[nums[index], (right[index] - index) * (index - left[index])] for index in range(n)], reverse=True):
            if k > freq:
                res *= quickPow(v, freq)
                res %= mod
                k -= freq
            else:
                res *= quickPow(v, k)
                res %= mod
                break
            
        return res
```
