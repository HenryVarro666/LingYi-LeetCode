---
title: "4040. 构造子集和的最少操作次数I"
aliases: ["yiduobo的每日leetcode 4040.构造子集和的最少操作次数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078981720406226021"
zhihu_id: "2078981720406226021"
zhihu_title: "yiduobo的每日leetcode 4040.构造子集和的最少操作次数I"
question_id: "4040"
question: "构造子集和的最少操作次数 I"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-i/"
difficulty: "Medium"
created: "2026-09-03T23:18:15+08:00"
updated: "2026-09-03T23:18:15+08:00"
upvotes: 2
comments: 0
---

# 4040. 构造子集和的最少操作次数I

> **[yiduobo的每日leetcode 4040.构造子集和的最少操作次数I](https://zhuanlan.zhihu.com/p/2078981720406226021) · 知乎 · 2026-09-03 · 赞同 2**
> 力扣：[4040. 构造子集和的最少操作次数 I](https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-i/) · Medium · 灵茶山艾府：[分组背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4040.构造子集和的最少操作次数I

<https://leetcode.cn/problems/minimum-operations-to-form-subset-sum-i/description/>

题目给出一个整数数组nums，其长度不超过100，其中元素的大小不超过500。另外给出一个整数sum，其大小不超过5000。

在一次操作中，可以选择一个值为x的元素，将其替换为x \* 2或者x // 2，这里的除法为整除。

另外规定，对于每个元素，对其执行的所有乘法操作必须发生在任意除法操作之前。

问最少需要多少次操作，可以使得操作后的数组中存在一个子集，其中的元素之和恰好等于sum。若无法达成，则返回-1。

可以发现，题目最终的要求是从一个集合中选出某些元素，在这些元素和为sum的前提下，使得这些元素的代价之和最小，是一个非常标准的背包问题。基于本题的数据规模，只要能确定下来nums中每个元素可能进行的变换结果，就能通过动态规划轻松求解了。

接下来考虑每个元素可能进行的操作。由于题目要求所有的乘法操作都发生在除法操作之前，那么当一个操作序列中既有乘法操作，又有除法操作时，最后一次乘法操作与第一次除法操作就是相邻执行的，可以发现，这两个操作实际上完全抵消掉了。更进一步的，只要这个操作序列中还同时存在乘法与除法操作，那么就可以不断进行抵消，直到整个操作序列中仅剩一种操作位置，因此对于一个元素x：

- 要么不操作，此时得到的结果就是x自身，代价为0
- 要么做k次乘法，此时得到的结果就是x \<\< k，代价为k。需要注意，这里的x \<\< k不应该超过sum
- 要么做k次除法操作，此时得到的结果就是x >> k，代价为k。需要注意，这里的x >> k不应该等于0

基于这个结论，就可以先构造出x的所有可用变换，并将其最终的值与代价记录在数组usage中，然后再使用usage更新动态规划的数组即可。

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
            usage = []
            x = v
            cost = 0
            while x > 1:
                x >>= 1
                cost += 1
                usage.append((x, cost))
            
            usage.reverse()

            x = v
            cost = 0
            while x <= sum:
                usage.append((x, cost))
                x <<= 1
                cost += 1
            
            for s in range(sum, -1, -1):
                for x, cost in usage:
                    if s < x:
                        break
                    if f[s - x] != -1 and (f[s] == -1 or f[s] > f[s - x] + cost):
                        f[s] = f[s - x] + cost
            

        return f[-1]
```
