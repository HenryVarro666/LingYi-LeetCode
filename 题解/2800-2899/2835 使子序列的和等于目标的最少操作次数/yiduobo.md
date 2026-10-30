---
title: "2835. 使子序列的和等于目标的最少操作数"
aliases: ["yiduobo的每日leetcode 2835.使子序列的和等于目标的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659572983"
zhihu_id: "659572983"
zhihu_title: "yiduobo的每日leetcode 2835.使子序列的和等于目标的最少操作数"
question_id: "2835"
question: "使子序列的和等于目标的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-form-subsequence-with-target-sum/"
difficulty: "Hard"
rating: 2207
created: "2023-10-05T02:36:18+08:00"
updated: "2023-10-05T02:36:18+08:00"
upvotes: 0
comments: 0
---

# 2835. 使子序列的和等于目标的最少操作数

> **[yiduobo的每日leetcode 2835.使子序列的和等于目标的最少操作数](https://zhuanlan.zhihu.com/p/659572983) · 知乎 · 2023-10-05 · 赞同 0**
> 力扣：[2835. 使子序列的和等于目标的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-form-subsequence-with-target-sum/) · Hard · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

昨日外出漏更，今天补上

2835.使子序列的和等于目标的最少操作数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-operations-to-form-subsequence-with-target-sum/)

本题基于2的幂次进行操作，因此在这里可以先将target中的2的幂先分离出来，然后逐个去适配这些幂次。

本题中的对数组元素的修改相当于将一个2^k拆分成了两个2^(k - 1)，如果是通过不断拆分某个数来适配某个幂次v的话，其拆分剩余的部分则可以涵盖住所有大于v但小于2^k的数。

例如16，二进制下是10000，拆分的方法可以是

10000 \= 1000 + 1000

10000 \= 1100 + 100

10000 \= 1110 + 10

10000 \= 1111 + 1

其中右侧的数v是适配的目标，可以发现左侧的数中1的位置就已经覆盖住了所有大于v但小于2^k的数。

除此之外，也可以通过若干个较小的值之和来适配某个幂次。由于这里是二进制的加法且参与加法的都是2的幂，因此在这里不会有越级进位的情况出现，也就是说若当前所有小于等于v的数之和s大于v，那么一定存在一种方法从中选出部分数，使得这些数之和恰好等于v。

综合上面两点，就得到了一种做法：

1、首先将target从低位到高位将2的幂分离出来得到num_list，同时将nums从小到大进行排序。

2、接下来遍历num_list逐个进行适配。对于当前适配的目标target，先将nums中所有没有使用且小于等于target的值都累加到s中。

若此时的s大于等于target，那么直接可以通过某些数的和来适配target，此时只需将s减去target然后继续向后适配就行了。

反之，若此时的s不够大，那么就必须拆分掉nums中的下一个数。又由于拆分后的结果具备连续的前导1，因此在这里可以直接将剩余数累加到s当中去，这是因为当下一个target不够大时，这里剩余的值的连续前导1可以覆盖住target，避免1 + 4 \= 5 > 2但实际上5里面没有直接的2的这种情况出现，而下一个target够大的话，则回到了较小值之和来凑target的情况。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        if sum(nums) < target:
            return -1

        v = target
        num_list = []
        while v:
            num_list.append(v & -v)
            v -= num_list[-1]
        
        nums.sort()
        p = 0
        res = 0
        s = 0
        for target in num_list:
            while p < len(nums) and nums[p] <= target:
                s += nums[p]
                p += 1

            if s >= target:
                s -= target
            else:
                x = nums[p]
                while x != target:
                    res += 1
                    x >>= 1
                s += nums[p] - target
                p += 1
        
        return res
```
