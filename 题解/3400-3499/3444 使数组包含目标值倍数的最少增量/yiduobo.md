---
title: "3444. 使数组包含目标值倍数的最少增量"
aliases: ["yiduobo的每日leetcode 3444.使数组包含目标值倍数的最少增量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/heap-priority-queue", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1892377750179914397"
zhihu_id: "1892377750179914397"
zhihu_title: "yiduobo的每日leetcode 3444.使数组包含目标值倍数的最少增量"
question_id: "3444"
question: "使数组包含目标值倍数的最少增量"
problem_url: "https://leetcode.cn/problems/minimum-increments-for-target-multiples-in-an-array/"
difficulty: "Hard"
rating: 2337
created: "2025-04-07T00:59:27+08:00"
updated: "2025-04-07T00:59:27+08:00"
upvotes: 1
comments: 0
---

# 3444. 使数组包含目标值倍数的最少增量

> **[yiduobo的每日leetcode 3444.使数组包含目标值倍数的最少增量](https://zhuanlan.zhihu.com/p/1892377750179914397) · 知乎 · 2025-04-07 · 赞同 1**
> 力扣：[3444. 使数组包含目标值倍数的最少增量](https://leetcode.cn/problems/minimum-increments-for-target-multiples-in-an-array/) · Hard · 灵茶山艾府：[子集状压 DP：记忆化搜索 / 递推 / 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3444.使数组包含目标值倍数的最少增量

[3444. 使数组包含目标值倍数的最少增量 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-increments-for-target-multiples-in-an-array/)

题目给出两个数组nums和target，其中nums的长度可达50000，而target的长度则不超过nums的长度，且最大为4。在单次操作中，可以将nums中的任意一个元素增加1。问最少需要多少次操作，才能使得target中的每个元素在nums中都至少存在一个倍数。

由于target的长度很小，那么在这里就可以尝试使用状态压缩来表示当前已经覆盖住的target中的元素，接下来就可以使用动态规划求解了。令f[index][state]表示nums[0]到nums[index]覆盖住target中的state表示的元素所需的最少操作次数，那么对于f[index][state]：

1、可以先假设最后这个元素nums[index]没有发挥任何作用：

那么就有f[index][state] \= f[index - 1][state]

2、如果最后这个元素发挥了作用，那么在这里可以枚举state的所有子状态sub_state，让nums[index]通过操作覆盖住sub_state中的元素：

为了覆盖住sub_state中的元素，那么就需要将nums[index]变为sub_state中所有元素的最小公倍数。这个最小公倍数可以在最开始遍历target中所有的元素组合预处理出来，方便起见，在这里记sub_state中所有元素的最小公倍数为lcm[sub_state]。

为了将nums[index]变为lcm[sub_state]的倍数，那么当nums[index]本身就是lcm[sub_state]倍数时，无需额外操作，否则需要lcm[sub_state] - nums[index] % lcm[sub_state]次操作，于是就有

f[index][state] \= f[index - 1][state ^ sub_state] + cost

其中cost是上面计算的操作次数。当然，这里有个前提是f[index - 1][state ^ sub_state]必须存在。

另外注意到f的每一轮状态只与上一轮有关，在这里可以使用滚动数组来优化掉index这一维。

最后附上python代码：

```python
class Solution(object):
    def minimumIncrements(self, nums, target):
        """
        :type nums: List[int]
        :type target: List[int]
        :rtype: int
        """
        
        n = len(nums)
        m = len(target)
        max_state = (1 << m)
        lcm = [0] * max_state
        lcm[0] = 1

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        for state in range(1, max_state):
            for index, v in enumerate(target):
                if state & (1 << index) == (1 << index):
                    pre_state = state ^ (1 << index)
                    lcm[state] = lcm[pre_state] * v // gcd(lcm[pre_state], v)
                    break

        f = [None] * max_state
        f[0] = 0
        for v in nums:
            g = f[:]
            f = [None] * max_state
            f[0] = 0
            for state in range(max_state):
                if g[state] is not None:
                    f[state] = g[state]
                sub_state = state
                while sub_state:
                    cost = v % lcm[sub_state]
                    if cost != 0:
                        cost = lcm[sub_state] - cost

                    if g[state ^ sub_state] is not None:
                        cost += g[state ^ sub_state]
                        if f[state] is None or f[state] > cost:
                            f[state] = cost

                    sub_state = (sub_state - 1) & state

        return f[-1]
```
