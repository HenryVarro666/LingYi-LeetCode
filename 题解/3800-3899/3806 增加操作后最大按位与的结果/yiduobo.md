---
title: "3806. 增加操作后最大按位与的结果"
aliases: ["yiduobo的每日leetcode 3806.增加操作后最大按位与的结果"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/quickselect", "leetcode/sorting", "题单/位运算", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1993786403063079208"
zhihu_id: "1993786403063079208"
zhihu_title: "yiduobo的每日leetcode 3806.增加操作后最大按位与的结果"
question_id: "3806"
question: "增加操作后最大按位与的结果"
problem_url: "https://leetcode.cn/problems/maximum-bitwise-and-after-increment-operations/"
difficulty: "Hard"
rating: 2259
created: "2026-01-13T23:00:50+08:00"
updated: "2026-01-13T23:00:50+08:00"
upvotes: 2
comments: 0
---

# 3806. 增加操作后最大按位与的结果

> **[yiduobo的每日leetcode 3806.增加操作后最大按位与的结果](https://zhuanlan.zhihu.com/p/1993786403063079208) · 知乎 · 2026-01-13 · 赞同 2**
> 力扣：[3806. 增加操作后最大按位与的结果](https://leetcode.cn/problems/maximum-bitwise-and-after-increment-operations/) · Hard · 灵茶山艾府：[试填法 + 排序/快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3806.增加操作后最大按位与的结果

[3806. 增加操作后最大按位与的结果 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-bitwise-and-after-increment-operations/description/)

题目给出一个整数数组nums和两个整数k和m。

现在可以执行一系列操作，每次操作中，可以选择任意下标index，并将nums[index]加上1。

问执行至多k次操作后，任意大小为m的子集中，按位与的结果的最大可能值是多少。

题目的描述有点绕，实际上就是要求在修改后，从数组中选出m个元素，这些元素的按位与最大。

对于这个问题，直接计算是不太方便的，不过本题是要求按位与的结果最大，因此可以考虑从高位往低位遍历，计算将数组中的每个元素的这一位变为1所需的代价，若前m小的代价之和小于等于k，那么答案的这一位就为1，否则为0。

对于以上的算法，还有两点需要注意的地方。

首先是答案的最高位应该如何确定：

不妨设p为大于nums中最大值的2的幂次，那么对于nums中的任意元素v，要将v在p唯一的这一个1变为1所需的代价，实际上就是将v变为p的代价，即p - v。更进一步的，最小的m个代价，就是p \* m，再减去nums中最大的m个元素之和。

若这个代价小于等于k，那么就可以进一步尝试p \* 2、p \* 4、...，以此类推，直到无法满足为止。这样以来，就确定了答案的最高位是什么。

另外就是如何计算每一位所需的代价：

对于当前遍历到的位index，不妨设v \= 2^index，接下来对于nums中的某个元素x

- 若x & v非0，说明x在index这一位上为1，不需要进行额外操作
- 反之，则需要先将x的所有更低位都提取出来，然后在此基础上加上一个值，使其变为v，因此所需的代价就是v减去低位对应的值。其中x的所有更低位，可以通过x & (v - 1)提取出来，那么代价就是v - (x & (v - 1))

在这里需要特别注意的是，低位变1是在高位变1的基础上进行的，例如1011，如果想要让次高位变为1，那么首次计算的代价为1，但是这个低位上的11就被消耗掉了。在之后如果想让下一位变为1，那么此时应该针对1100展开计算，而不是1011。

对于这个问题，一种可行的处理方案是对于数组中的每个元素，都记录下将该元素的高位变为答案的高位所需的代价之和，记为cost，那么在计算后续的位时，就可以让数组中的元素先加上对应的cost，然后针对这个新的元素计算当前位所需的代价，记为delta。接下来，将delta叠加到cost中，若cost中最小的m个代价之和小于等于k，那么答案的这一位就为1，否则答案的这一位为0，同时需要将当前这一位的代价从cost中删去，也就是将delta的值从cost中减去。

最后附上python代码：

```python
class Solution(object):
    def maximumAND(self, nums, k, m):
        """
        :type nums: List[int]
        :type k: int
        :type m: int
        :rtype: int
        """
        
        p2 = [1]
        nums.sort(reverse=True)
        s = sum(nums[:m])
        while p2[-1] <= nums[0]:
            p2.append(p2[-1] + p2[-1])
        
        while p2[-1] * m - s <= k:
            p2.append(p2[-1] + p2[-1])

        p2.pop()

        cost = [0] * len(nums)
        res = 0
        for v in p2[::-1]:
            delta = [0] * len(nums)
            for index in range(len(nums)):
                x = nums[index] + cost[index]
                if x & v:
                    continue
                else:
                    delta[index] = v - (x & (v - 1))
                    cost[index] += delta[index]
            
            sorted_cost = sorted(cost)
            if sum(sorted_cost[:m]) <= k:
                res |= v
            else:
                for index in range(len(nums)):
                    cost[index] -= delta[index]
        
        return res
```
