---
title: "4041. 构造子集和的最少操作次数II"
aliases: ["yiduobo的每日leetcode 4041.构造子集和的最少操作次数II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2079332385297114152"
zhihu_id: "2079332385297114152"
zhihu_title: "yiduobo的每日leetcode 4041.构造子集和的最少操作次数II"
question_id: "4041"
question: "构造子集和的最少操作次数 II"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-ii/"
difficulty: "Hard"
created: "2026-09-04T22:41:37+08:00"
updated: "2026-09-04T22:41:41+08:00"
upvotes: 0
comments: 0
---

# 4041. 构造子集和的最少操作次数II

> **[yiduobo的每日leetcode 4041.构造子集和的最少操作次数II](https://zhuanlan.zhihu.com/p/2079332385297114152) · 知乎 · 2026-09-04 · 赞同 0**
> 力扣：[4041. 构造子集和的最少操作次数 II](https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-ii/) · Hard · 灵茶山艾府：[分组背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4041.构造子集和的最少操作次数II

<https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-ii/description/>

题目给出一个整数数组nums，其长度不超过100，其中元素的大小不超过500。另外给出一个整数sum，其大小不超过5000。

在一次操作中，可以选择一个值为x的元素，将其替换为x \* 2或者x // 2，这里的除法为整除。

问最少需要多少次操作，可以使得操作后的数组中存在一个子集，其中的元素之和恰好等于sum。若无法达成，则返回-1。

之前4040题的加强版。

[yiduobo的每日leetcode 4040.构造子集和的最少操作次数I](https://zhuanlan.zhihu.com/p/2078981720406226021)

本题中不再有乘法必须发生在除法之前的限制，但是数据规模没变，因此依然是考虑使用动态规划求解，不同的是每个元素的使用方式将发生一些变化。

首先可以明确的是，依然不会出现先乘法后除法的操作，而之前4040题中的所有构造方案依然成立，那么在这里需要额外考虑的就是先除法后乘法的操作。

更进一步的，如果除法先与乘法执行，那么就意味着后面这次乘法无法抵消前面这次除法的影响，也就是说，只有当x为奇数时，连续两步执行除法乘法才有意义。

基于这一点，就可以将生成构造方案分成两个步骤执行。使用数组usage收集所有可行的方案，数组base记录所有有必要执行乘法的基底，那么对于当前的x：

1、不断对x执行除法操作，直到x为0为止。若当前的x为偶数，那么将x // 2加入usage，否则将x // 2加入base。理由如上面所述，只有当x为奇数时，对其执行除法操作后才有必要接着执行乘法操作

2、对于base中的所有元素，先将其加入到usage，然后不断执行乘法操作并将乘法结果加入usage，直到乘法结果大于sum为止

这样一来，就收集到了所有可行的方案。这里base的长度不超过logx，而每种base扩展得到的元素数量不超过log(sum)，因此在这里无需担心时间或者空间复杂度。

接下来，按背包问题的处理方法执行动态规划即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, sum):
        """
        :type nums: List[int]
        :type sum: int
        :rtype: int
        """
        
        f = [-1] * (sum + 1)
        f[0] = 0
        for v in nums:
            base = [(v, 0)]
            usage = []
            x = v
            cost = 0
            while x > 1:
                cost += 1
                if x & 1:
                    x >>= 1
                    base.append((x, cost))
                else:
                    x >>= 1
                    usage.append((x, cost))
                    
            for x, cost in base:
                while x <= sum:
                    usage.append((x, cost))
                    x <<= 1
                    cost += 1
            
            usage.sort(key=lambda d:d[0])

            for s in range(sum, -1, -1):
                for x, cost in usage:
                    if s < x:
                        break
                    if f[s - x] != -1 and (f[s] == -1 or f[s] > f[s - x] + cost):
                        f[s] = f[s - x] + cost

        return f[-1]
```
